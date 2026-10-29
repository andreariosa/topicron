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
