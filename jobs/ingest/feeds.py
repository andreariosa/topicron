"""The feed list: a reviewed, version-controlled config, not a table (docs/DATA_MODEL.md).

Adding a feed is a pull request, and it comes after reading the publisher's
robots.txt and terms (m0/rss-feeds.md records what was found for each one, and the feeds
that were tried and dropped). A feed with
`active=False` is never fetched by the hourly job; `python -m ingest --dry-run
--include-inactive` tries every feed once and prints one line each.
`source` is stored in content_items.source and is part of the dedupe key, so it
must never be renamed once rows exist.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Feed:
    source: str
    name: str
    url: str
    # Why: a feed that goes quiet should fail the run, not feed the pipeline stale news.
    # 72 hours covers a long weekend; MarketBeat publishes on weekends too.
    max_age_hours: int = 72
    active: bool = True
    # Why it is on or off, shown in probe mode and kept next to the URL.
    note: str = ""


FEEDS: tuple[Feed, ...] = (
    Feed(
        source="marketbeat",
        name="MarketBeat",
        url="https://www.marketbeat.com/feed/",
        note="robots.txt and terms read 2026-10-29 (m0/rss-feeds.md); the probe found 100 items, "
        "newest 5 h old; it timed out and answered 503 earlier that day, hence the retries",
    ),
    Feed(
        source="fed-press",
        name="Federal Reserve press releases",
        url="https://www.federalreserve.gov/feeds/press_all.xml",
        # Official and public, but it can go quiet for days.
        max_age_hours=336,
        note="the Board's site is public domain, cite the Board (disclaimer page, 2026-10-29)",
    ),
    # Switched on by the founder's decision of 2026-10-29. Claude could not read the robots.txt
    # or the terms of these three publishers (its tool could not load them), so the founder reads
    # them (m0/rss-feeds.md); the rule for news items applies: headline, link and short description
    # stored, never the article page, never shown on a public page beyond headline and link.
    Feed(
        source="cnbc-top",
        name="CNBC Top News",
        url="https://www.cnbc.com/id/100003114/device/rss/rss.html",
        note="probe 2026-10-29: 30 items, fresh; robots.txt and terms not read by Claude",
    ),
    Feed(
        source="yahoo-tickers",
        name="Yahoo Finance, VZ T TMUS",
        url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=VZ,T,TMUS&region=US&lang=en-US",
        note="probe 2026-10-29: 19 items, fresh, about the thesis 13 companies; robots.txt of "
        "this host and terms not read by Claude",
    ),
    Feed(
        source="marketwatch-top",
        name="MarketWatch Top Stories",
        url="https://feeds.content.dowjones.io/public/rss/mw_topstories",
        # Holds only the latest ten stories (about 90 minutes at midday), so an hourly run that
        # GitHub delays by a few hours misses some. Fine for narratives; not a complete record.
        note="probe 2026-10-29: 10 items, fresh; robots.txt and terms not read by Claude",
    ),
    # Switched off.
    Feed(
        source="nasdaq-markets",
        name="Nasdaq Markets",
        url="https://www.nasdaq.com/feed/rssoutbound?category=Markets",
        active=False,
        note="timed out in the 2026-10-29 probe; robots.txt has no rule against /feed/; terms "
        "unread",
    ),
)
