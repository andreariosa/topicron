"""The feed list: a reviewed, version-controlled config, not a table (docs/DATA_MODEL.md).

Adding a feed is a pull request, and it comes after reading the publisher's
robots.txt and terms (m0/rss-feeds.md records what was found for each one). A feed with
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
        active=False,
        note="robots.txt and terms read 2026-10-29 (m0/rss-feeds.md); but the feed answered 503 in "
        "the founder's browser and timed out from GitHub that day. Switch on if it recovers",
    ),
    Feed(
        source="benzinga",
        name="Benzinga",
        url="https://feeds.benzinga.com/benzinga",
        active=False,
        note="server closed the connection in the founder's browser 2026-10-29; robots.txt unread",
    ),
    # Candidates below are probe-only. Each is one plain GET, as any feed reader does. None is
    # switched on before its robots.txt and terms have been read (m0/rss-feeds.md).
    Feed(
        source="cnbc-top",
        name="CNBC Top News",
        url="https://www.cnbc.com/id/100003114/device/rss/rss.html",
        active=False,
        note="candidate; robots.txt not readable by Claude's tool; terms unread",
    ),
    Feed(
        source="cnbc-finance",
        name="CNBC Finance",
        url="https://www.cnbc.com/id/10000664/device/rss/rss.html",
        active=False,
        note="candidate; robots.txt not readable by Claude's tool; terms unread",
    ),
    Feed(
        source="yahoo-finance",
        name="Yahoo Finance",
        url="https://finance.yahoo.com/news/rssindex",
        active=False,
        note="candidate; robots.txt has no rule against /news/rssindex (2026-10-29); terms unread",
    ),
    Feed(
        source="yahoo-tickers",
        name="Yahoo Finance, VZ T TMUS",
        url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=VZ,T,TMUS&region=US&lang=en-US",
        active=False,
        note="candidate; headlines for the thesis 13 tickers; robots.txt of this host unread",
    ),
    Feed(
        source="nasdaq-markets",
        name="Nasdaq Markets",
        url="https://www.nasdaq.com/feed/rssoutbound?category=Markets",
        active=False,
        note="candidate; robots.txt has no rule against /feed/ (read 2026-10-29); terms unread",
    ),
    Feed(
        source="marketwatch-top",
        name="MarketWatch Top Stories",
        url="https://feeds.content.dowjones.io/public/rss/mw_topstories",
        active=False,
        note="candidate; robots.txt and terms unread",
    ),
    Feed(
        source="fed-press",
        name="Federal Reserve press releases",
        url="https://www.federalreserve.gov/feeds/press_all.xml",
        # Official and public, but it can go quiet for days.
        max_age_hours=336,
        active=False,
        note="candidate; official source; robots.txt not readable by Claude's tool",
    ),
)
