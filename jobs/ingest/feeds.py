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
    # CNBC and MarketWatch were switched on by the founder's decision of 2026-10-29, before their
    # robots.txt or terms had been read (Claude's tool could not load them). The founder then read
    # the robots.txt files (m0/rss-feeds.md); the terms of both publishers are still unread. The
    # rule for news items applies: headline, link and short description stored, never the
    # article page, never shown on a public page beyond headline and link.
    Feed(
        source="cnbc-top",
        name="CNBC Top News",
        url="https://www.cnbc.com/id/100003114/device/rss/rss.html",
        note="robots.txt read 2026-10-29: the rules for every robot do not cover the feed path and "
        "Topicron is not named, but AI and finance bots are blocked by name; terms unread; kept "
        "on by the founder's decision of 2026-10-29",
    ),
    Feed(
        source="marketwatch-top",
        name="MarketWatch Top Stories",
        url="https://feeds.content.dowjones.io/public/rss/mw_topstories",
        # Holds only the latest ten stories (about 90 minutes at midday), so an hourly run that
        # GitHub delays by a few hours misses some. Fine for narratives; not a complete record.
        note="probe 2026-10-29: 10 items, fresh; the robots.txt URL of its host answers "
        "AccessDenied (read as no file); terms unread",
    ),
    # Verizon's newsroom feed, switched on by the founder's decision of 2026-10-29 after the
    # robots.txt file and the terms were read (m0/rss-feeds.md). robots.txt does not cover it, but
    # the terms ban robots and automated scripts in plain words (they do not mention RSS) while the
    # company advertises the feed itself; the founder chose to switch it on for consistency with
    # CNBC and did not ask the press office. The first dry run on GitHub read it right (10 items,
    # 09:12:17 AM EDT as 13:12:17 UTC) and the hourly runs stored all ten. If the company
    # objects, set active=False and delete its rows.
    Feed(
        source="verizon-financial",
        name="Verizon financial news releases",
        url="https://www.verizon.com/about/news/financial-news.xml",
        # 10 items spanning 24 Jul to 29 Oct 2026: about one a week, and quieter some weeks.
        max_age_hours=720,
        note="RSS 2.0, 10 items, newest 29 Oct 2026; "
        "pubDate is written 'h:mm:ss AM EDT' and 'Sept' (read by ingest.rss since 2026-10-29); "
        "robots.txt of www.verizon.com does not cover /about/news/*.xml; the Website Terms of "
        "Use ban automated scripts, bots and offline readers and data-gathering tools and do "
        "not mention RSS; on by the founder's decision of 2026-10-29; the guid is the headline "
        "(seen in the stored rows, 2026-10-29), so a repeated headline would be dropped as "
        "already stored; "
        "verizon-news-releases.xml overlaps it and is not listed until cross-feed dedupe exists",
    ),
    # Switched off.
    Feed(
        source="att-newsroom",
        name="AT&T newsroom",
        url="https://about.att.com/aboutus/rss/rssfeed.html?category=all",
        max_age_hours=336,
        active=False,
        note="switched on by the founder's decision of 2026-10-29 and off again the same day: "
        "its server answered HTTP 403 to the job's own user agent from GitHub's runner (dry run, "
        "15:26 UTC), which the job takes as the publisher saying no and does not retry; it had "
        "answered a page-reading tool earlier that day; robots.txt of about.att.com only "
        "disallows /system/; the Web Services Terms of Use ban any robot, spider or automatic "
        "device (section 14) and do not mention RSS; the founder decided on 2026-10-29 not to ask "
        "the press office, so it stays off",
    ),
    Feed(
        source="yahoo-tickers",
        name="Yahoo Finance, VZ T TMUS",
        url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=VZ,T,TMUS&region=US&lang=en-US",
        active=False,
        note="robots.txt of this host read 2026-10-29: User-agent * Disallow /, so no robot may "
        "fetch it; the 17 rows stored before the reading were deleted",
    ),
    Feed(
        source="nasdaq-markets",
        name="Nasdaq Markets",
        url="https://www.nasdaq.com/feed/rssoutbound?category=Markets",
        active=False,
        note="timed out in the 2026-10-29 probe; robots.txt has no rule against /feed/; terms "
        "unread",
    ),
)
