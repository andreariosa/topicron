import http.client
from datetime import UTC, datetime

import pytest

from ingest import rss
from ingest.rss import clean_text, fetch_feed, parse_feed

# Shaped like MarketBeat's feed (no namespaces, guid with isPermaLink="false", several tickers
# in one category separated by a line break), written by hand: the shell cannot reach the site.
FEED = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>Example news</title>
    <lastBuildDate>Mon, 21 Sep 2026 00:00:00 GMT</lastBuildDate>
    <item>
      <title>Acme Corp&#39;s shares rise &amp; analysts agree</title>
      <link>https://news.example.com/acme-rises</link>
      <guid isPermaLink="false">news8995415</guid>
      <pubDate>Mon, 21 Sep 2026 12:50:00 GMT</pubDate>
      <description>Acme Corp (NYSE:ACM) rose 4% on Monday. AT&amp;T said nothing.</description>
      <category>NYSE:ACM</category>
      <category>NYSE:ACM
NYSE:GNRC</category>
    </item>
    <item>
      <title>Second item</title>
      <link>https://news.example.com/second</link>
      <pubDate>Sun, 13 Sep 2026 07:35:00 GMT</pubDate>
      <description></description>
    </item>
  </channel>
</rss>
"""


def feed_with(item: str) -> bytes:
    return f'<rss version="2.0"><channel>{item}</channel></rss>'.encode()


def item(**parts: str) -> str:
    fields = {
        "title": "A title",
        "link": "https://news.example.com/a",
        "guid": "g1",
        "pubDate": "Mon, 21 Sep 2026 12:50:00 GMT",
        **parts,
    }
    inner = "".join(f"<{tag}>{value}</{tag}>" for tag, value in fields.items() if value != "")
    return f"<item>{inner}</item>"


def test_parses_the_fields_of_an_item() -> None:
    result = parse_feed(FEED)

    first = result.items[0]
    assert first.external_id == "news8995415"
    assert first.title == "Acme Corp's shares rise & analysts agree"
    assert first.url == "https://news.example.com/acme-rises"
    assert first.published_at == datetime(2026, 9, 21, 12, 50, tzinfo=UTC)
    assert first.body == "Acme Corp (NYSE:ACM) rose 4% on Monday. AT&T said nothing."
    assert first.author is None
    # The second category holds two tickers; whitespace is normalised, repeats are dropped.
    assert first.categories == ("NYSE:ACM", "NYSE:ACM NYSE:GNRC")
    assert result.skipped == []


def test_guid_falls_back_to_the_link() -> None:
    second = parse_feed(FEED).items[1]

    assert second.external_id == "https://news.example.com/second"
    assert second.body == ""
    assert second.categories == ()


def test_the_author_comes_from_dc_creator_or_author() -> None:
    xml = (
        b'<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel>'
        b"<item><title>T</title><link>https://a.example/x</link>"
        b"<pubDate>Mon, 21 Sep 2026 12:50:00 GMT</pubDate><dc:creator>Jane Doe</dc:creator></item>"
        b"</channel></rss>"
    )

    assert parse_feed(xml).items[0].author == "Jane Doe"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("plain text", "plain text"),
        ("  spaced \n out\t text ", "spaced out text"),
        ("<p>Hello <b>world</b></p>", "Hello world"),
        ("It&#39;s fine &amp; good", "It's fine & good"),  # a second level of escaping
        ("AT&T and S&P 500", "AT&T and S&P 500"),  # bare ampersands stay
        ("growth <5% this year", "growth <5% this year"),  # a "<" that starts no tag stays
        ("before<script>alert(1)</script>after", "beforeafter"),
        (None, ""),
    ],
)
def test_clean_text(raw: str | None, expected: str) -> None:
    assert clean_text(raw) == expected


def test_a_long_description_is_cut() -> None:
    xml = feed_with(item(description="x" * (rss.MAX_BODY_CHARS + 50)))

    assert len(parse_feed(xml).items[0].body) == rss.MAX_BODY_CHARS


@pytest.mark.parametrize(
    ("parts", "reason"),
    [
        ({"title": ""}, "no title"),
        ({"title": "<b></b>"}, "no title"),
        ({"link": ""}, "link is not an http(s) URL"),
        ({"link": "javascript:alert(1)"}, "link is not an http(s) URL"),
        ({"pubDate": ""}, "no pubDate"),
        ({"pubDate": "yesterday-ish"}, "unreadable pubDate"),
    ],
)
def test_unusable_items_are_skipped_with_a_reason(parts: dict[str, str], reason: str) -> None:
    result = parse_feed(feed_with(item(**parts) + item(guid="g2")))

    assert [entry.external_id for entry in result.items] == ["g2"]
    assert len(result.skipped) == 1
    assert result.skipped[0].startswith("item 1: ") and reason in result.skipped[0]


def test_a_date_without_a_zone_is_read_as_utc() -> None:
    result = parse_feed(feed_with(item(pubDate="Mon, 21 Sep 2026 12:50:00 -0000")))

    assert result.items[0].published_at == datetime(2026, 9, 21, 12, 50, tzinfo=UTC)


def test_a_date_with_an_offset_is_converted_to_utc() -> None:
    result = parse_feed(feed_with(item(pubDate="Mon, 21 Sep 2026 14:50:00 +0200")))

    assert result.items[0].published_at == datetime(2026, 9, 21, 12, 50, tzinfo=UTC)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        # Verizon's form: 12-hour clock, a US zone name. EDT is UTC-4.
        ("Thu, 29 Oct 2026 09:12:17 AM EDT", datetime(2026, 10, 29, 13, 12, 17, tzinfo=UTC)),
        ("Thu, 29 Oct 2026 04:26:25 PM EDT", datetime(2026, 10, 29, 20, 26, 25, tzinfo=UTC)),
        ("Fri, 16 Oct 2026 12:00:00 AM EDT", datetime(2026, 10, 16, 4, 0, tzinfo=UTC)),
        ("Fri, 16 Oct 2026 12:30:00 PM EDT", datetime(2026, 10, 16, 16, 30, tzinfo=UTC)),
        ("Mon, 02 Nov 2026 07:00:09 am EST", datetime(2026, 11, 2, 12, 0, 9, tzinfo=UTC)),
        # "Sept" is not an RFC 2822 month name.
        ("Tue, 29 Sept 2026 04:26:25 PM EDT", datetime(2026, 9, 29, 20, 26, 25, tzinfo=UTC)),
    ],
)
def test_a_twelve_hour_date_is_read_with_its_am_or_pm(raw: str, expected: datetime) -> None:
    result = parse_feed(feed_with(item(pubDate=raw)))

    assert result.items[0].published_at == expected


@pytest.mark.parametrize(
    "raw",
    [
        "Thu, 29 Oct 2026 13:12:17 PM EDT",  # 13 o'clock with PM is not a time
        "Thu, 29 Oct 2026 00:12:17 AM EDT",
        "Thu, 29 Oct 2026 9:12 AM EDT",  # no seconds: a form this parser does not read
    ],
)
def test_an_am_pm_date_in_another_form_is_skipped_not_guessed(raw: str) -> None:
    result = parse_feed(feed_with(item(pubDate=raw) + item(guid="g2")))

    assert [entry.external_id for entry in result.items] == ["g2"]
    assert "unreadable pubDate" in result.skipped[0]


def test_the_same_item_twice_is_kept_once() -> None:
    result = parse_feed(feed_with(item() + item(title="Edited title")))

    assert [entry.title for entry in result.items] == ["A title"]


def test_a_feed_with_no_items_parses_to_an_empty_result() -> None:
    result = parse_feed(feed_with(""))

    assert result.items == [] and result.skipped == []


@pytest.mark.parametrize(
    ("xml", "message"),
    [
        (b"<rss", "not valid XML"),
        (b"<html><body>Please enable JavaScript</body></html>", "not valid XML|not an RSS"),
        (b'<feed xmlns="http://www.w3.org/2005/Atom"></feed>', "not an RSS 2.0 feed"),
        (b'<rss version="2.0"></rss>', "no <channel>"),
        (
            b'<?xml version="1.0"?><!DOCTYPE rss [<!ENTITY a "aaaa">]><rss><channel/></rss>',
            "DTD",
        ),
        (b'<!DocType rss><rss version="2.0"><channel/></rss>', "DTD"),
    ],
)
def test_a_feed_that_is_not_rss_is_refused(xml: bytes, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        parse_feed(xml)


def test_an_oversized_document_is_refused() -> None:
    with pytest.raises(ValueError, match="larger than"):
        parse_feed(b"x" * (rss.MAX_BYTES + 1))


def test_fetch_sends_an_identifying_user_agent() -> None:
    calls: list[tuple[str, dict[str, str]]] = []

    def fake_get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
        calls.append((url, headers))
        return 200, b"<rss/>"

    assert fetch_feed("https://news.example.com/feed/", fake_get) == b"<rss/>"
    assert calls[0][0] == "https://news.example.com/feed/"
    assert "topicron.vercel.app" in calls[0][1]["User-Agent"]


def test_fetch_fails_loudly_on_a_non_200_answer() -> None:
    with pytest.raises(RuntimeError, match="HTTP 403"):
        fetch_feed("https://news.example.com/feed/", lambda url, headers: (403, b"blocked"))


def test_fetch_refuses_an_oversized_answer() -> None:
    with pytest.raises(ValueError, match="larger than"):
        fetch_feed(
            "https://news.example.com/feed/",
            lambda url, headers: (200, b"x" * (rss.MAX_BYTES + 1)),
        )


def test_an_html_block_page_shows_how_it_starts() -> None:
    page = b"<!DOCTYPE html><html><head><title>Just a moment...</title></head></html>"
    # A DTD is refused before parsing, so use a page without one, as most block pages are.
    page = page.replace(b"<!DOCTYPE html>", b"")

    with pytest.raises(ValueError, match="not an RSS 2.0 feed.*Just a moment"):
        parse_feed(page)


def test_broken_xml_shows_how_it_starts() -> None:
    with pytest.raises(ValueError, match="not valid XML.*starts with 'Service Unavailable"):
        parse_feed(b"Service Unavailable. Please try again later.")


class Flaky:
    """An http_get that follows a script, one entry per call: (status, body) or an exception."""

    def __init__(self, *script: tuple[int, bytes] | Exception) -> None:
        self.script = list(script)
        self.calls = 0

    def __call__(self, url: str, headers: dict[str, str]) -> tuple[int, bytes]:
        self.calls += 1
        step = self.script.pop(0)
        if isinstance(step, Exception):
            raise step
        return step


def test_a_server_error_is_retried_and_the_second_try_can_succeed() -> None:
    waits: list[float] = []
    http_get = Flaky((503, b"busy"), (200, b"<rss/>"))

    assert fetch_feed("https://f.example/feed/", http_get, waits.append) == b"<rss/>"
    assert http_get.calls == 2 and waits == [5]


def test_a_network_failure_is_retried_up_to_three_tries() -> None:
    waits: list[float] = []
    http_get = Flaky(
        TimeoutError("The read operation timed out"),
        http.client.IncompleteRead(b""),
        TimeoutError("The read operation timed out"),
    )

    with pytest.raises(RuntimeError, match="failed after 3 tries, last: TimeoutError"):
        fetch_feed("https://f.example/feed/", http_get, waits.append)

    assert http_get.calls == 3 and waits == [5, 15]


def test_three_server_errors_end_in_a_loud_failure() -> None:
    http_get = Flaky((503, b""), (502, b""), (503, b""))

    with pytest.raises(RuntimeError, match="failed after 3 tries, last: HTTP 503"):
        fetch_feed("https://f.example/feed/", http_get, lambda seconds: None)


@pytest.mark.parametrize("status", [403, 404, 429])
def test_a_client_error_is_not_retried(status: int) -> None:
    waits: list[float] = []
    http_get = Flaky((status, b"no"))

    with pytest.raises(RuntimeError, match=f"HTTP {status}"):
        fetch_feed("https://f.example/feed/", http_get, waits.append)

    assert http_get.calls == 1 and waits == []
