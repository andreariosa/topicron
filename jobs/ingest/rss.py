"""Fetch and parse an RSS 2.0 feed with the standard library only.

Why hand-rolled: the feeds are a handful of curated URLs and the fields needed are
few, so a feed-parsing package would be a dependency for ten lines of ElementTree.
The price of that is that the guards below are ours to keep.
"""

from __future__ import annotations

import http.client
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from urllib.parse import urlparse

USER_AGENT = "Topicron/0.1 (+https://topicron.vercel.app)"
# A feed of 100 short items is about 100 KB; anything near this size is not the feed we expect.
MAX_BYTES = 5_000_000
# Descriptions are a sentence or two. The cap only protects the database from a runaway item.
MAX_BODY_CHARS = 5_000

# (url, headers) -> (status, body). Replaced by a fake in tests.
HttpGet = Callable[[str, dict[str, str]], tuple[int, bytes]]

# Seconds to wait before the second and third try. Why: on 2026-10-29 MarketBeat timed out and
# answered 503 and, hours later, answered fine; one bad moment should not be a red run.
# A 4xx answer is not retried: 403 and 404 mean the publisher said no.
RETRY_DELAYS = (5, 15)

_DC_CREATOR = "{http://purl.org/dc/elements/1.1/}creator"


@dataclass(frozen=True)
class Item:
    external_id: str
    title: str
    url: str
    published_at: datetime
    body: str
    author: str | None
    categories: tuple[str, ...]


@dataclass
class ParseResult:
    items: list[Item] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def _urllib_get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return int(response.status), bytes(response.read(MAX_BYTES + 1))
    except urllib.error.HTTPError as error:
        return error.code, error.read(1000)


def fetch_feed(
    url: str,
    http_get: HttpGet = _urllib_get,
    sleep: Callable[[float], None] = time.sleep,
) -> bytes:
    """GET a feed, trying up to three times when the server or the network fails."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/rss+xml, application/xml;q=0.9, text/xml;q=0.8",
    }
    tries = len(RETRY_DELAYS) + 1
    for attempt in range(1, tries + 1):
        try:
            status, body = http_get(url, headers)
        except (OSError, http.client.HTTPException) as error:
            reason = f"{type(error).__name__}: {error}"
        else:
            if status == 200:
                if len(body) > MAX_BYTES:
                    raise ValueError(f"{url} is larger than {MAX_BYTES} bytes")
                return body
            if status < 500:
                raise RuntimeError(f"{url} answered HTTP {status}")
            reason = f"HTTP {status}"
        if attempt == tries:
            raise RuntimeError(f"{url} failed after {tries} tries, last: {reason}")
        sleep(RETRY_DELAYS[attempt - 1])
    raise AssertionError("unreachable")  # pragma: no cover


class _TextExtractor(HTMLParser):
    """Keeps the text of a fragment: tags go, entities are decoded, script and style are dropped."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._hidden = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self._hidden += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self._hidden:
            self._hidden -= 1

    def handle_data(self, data: str) -> None:
        if not self._hidden:
            self.parts.append(data)


def clean_text(value: str | None) -> str:
    """Plain text from a title or description: tags stripped, entities decoded, blanks collapsed.

    The XML parser has already decoded one level of entities. Some publishers escape twice
    (`&amp;#39;`), which leaves a literal `&#39;` here, so a second decoding pass is needed.
    A bare `<` that does not start a tag (`growth <5%`) is kept as text.
    """
    if not value:
        return ""
    extractor = _TextExtractor()
    extractor.feed(value)
    extractor.close()
    return " ".join("".join(extractor.parts).split())


def _child_text(element: ET.Element, tag: str) -> str:
    child = element.find(tag)
    return (child.text or "").strip() if child is not None else ""


def _parse_date(value: str) -> datetime:
    parsed = parsedate_to_datetime(value)  # raises ValueError (or TypeError) on junk
    # A date written "-0000" or without a zone comes back naive; RSS dates are UTC by convention.
    return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)


def _parse_item(element: ET.Element) -> Item:
    """One <item> into an Item, or raise ValueError with the reason it cannot be used."""
    title = clean_text(_child_text(element, "title"))
    if not title:
        raise ValueError("no title")
    link = _child_text(element, "link")
    if urlparse(link).scheme not in ("http", "https"):
        raise ValueError(f"link is not an http(s) URL: {link[:60]!r}")
    external_id = _child_text(element, "guid") or link
    raw_date = _child_text(element, "pubDate")
    if not raw_date:
        raise ValueError("no pubDate")
    try:
        published_at = _parse_date(raw_date)
    except (TypeError, ValueError):
        raise ValueError(f"unreadable pubDate: {raw_date[:40]!r}") from None

    author = clean_text(_child_text(element, _DC_CREATOR) or _child_text(element, "author"))
    categories: list[str] = []
    for category in element.findall("category"):
        # MarketBeat puts several tickers in one category, separated by a line break.
        text = " ".join((category.text or "").split())
        if text and text not in categories:
            categories.append(text)
    return Item(
        external_id=external_id,
        title=title,
        url=link,
        published_at=published_at,
        body=clean_text(_child_text(element, "description"))[:MAX_BODY_CHARS],
        author=author or None,
        categories=tuple(categories),
    )


def _snippet(xml: bytes) -> str:
    """The first characters of a document, for an error message (a block page shows up here)."""
    return repr(" ".join(xml[:120].decode("utf-8", errors="replace").split())[:100])


def parse_feed(xml: bytes) -> ParseResult:
    """Parse an RSS 2.0 document. Items that cannot be used are listed in `skipped`, not hidden."""
    if len(xml) > MAX_BYTES:
        raise ValueError(f"feed is larger than {MAX_BYTES} bytes")
    lowered = xml.lower()
    # ElementTree expands entities, so a hostile or broken DTD could blow up memory.
    # RSS 2.0 has no use for a DTD; refuse it instead of trusting the parser's limits.
    if b"<!doctype" in lowered or b"<!entity" in lowered:
        raise ValueError("feed contains a DTD, which RSS 2.0 does not need")
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as error:
        raise ValueError(
            f"feed is not valid XML: {error}; it starts with {_snippet(xml)}"
        ) from None
    if root.tag != "rss":
        raise ValueError(
            f"not an RSS 2.0 feed (root element <{root.tag}>); it starts with {_snippet(xml)}"
        )
    channel = root.find("channel")
    if channel is None:
        raise ValueError("RSS feed has no <channel>")

    result = ParseResult()
    seen: set[str] = set()
    for index, element in enumerate(channel.findall("item"), start=1):
        try:
            item = _parse_item(element)
        except ValueError as error:
            result.skipped.append(f"item {index}: {error}")
            continue
        if item.external_id in seen:
            continue
        seen.add(item.external_id)
        result.items.append(item)
    return result
