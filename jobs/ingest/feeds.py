"""The feed list: a reviewed, version-controlled config, not a table (docs/DATA_MODEL.md).

Adding a feed is a pull request, and it comes after reading the publisher's
robots.txt and terms (m0/rss-feeds.md records what was found for each one).
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


FEEDS: tuple[Feed, ...] = (
    Feed(source="marketbeat", name="MarketBeat", url="https://www.marketbeat.com/feed/"),
    # Off until the founder has read https://feeds.benzinga.com/robots.txt in a browser.
    Feed(
        source="benzinga",
        name="Benzinga",
        url="https://feeds.benzinga.com/benzinga",
        active=False,
    ),
)
