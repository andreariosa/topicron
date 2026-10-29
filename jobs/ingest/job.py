"""Hourly ingestion job (M1b, ADR-0004 D-34).

Reads the curated RSS feeds in feeds.py and stores each item once in content_items.
Zero LLM cost (ADR-0002); ticker extraction is a separate, later step.

Dedupe: the key is (source, external_id). The first copy of an item is kept as it
was ingested, so a later edit by the publisher never changes what a thesis cited,
and a re-run adds nothing.

Like the prices job, it fails loudly instead of staying green: a feed that errors,
parses to nothing, or has gone quiet is a problem. Everything that could be written is
written first, then the run raises, so one bad feed does not hide the others.
"""

from __future__ import annotations

import argparse
import http.client
import logging
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol

from common.supabase_rest import SupabaseRest
from ingest.feeds import FEEDS, Feed
from ingest.rss import Item, fetch_feed, parse_feed

log = logging.getLogger("ingest")

# An item dated further ahead than this is a broken date, not news. It would also
# make a dead feed look fresh, so it is skipped instead of trusted.
FUTURE_TOLERANCE = timedelta(hours=1)
# PostgREST takes a whole array in one request; this keeps each request small.
BATCH_SIZE = 100
DRY_RUN_SAMPLE = 3


class Db(Protocol):
    def insert_new(
        self, table: str, rows: list[dict[str, Any]], on_conflict: str
    ) -> list[dict[str, Any]]: ...


@dataclass
class FeedReport:
    source: str
    parsed: int = 0
    skipped: list[str] = field(default_factory=list)
    inserted: int = 0
    newest: datetime | None = None
    oldest: datetime | None = None
    sample: list[Item] = field(default_factory=list)


@dataclass
class Report:
    feeds: list[FeedReport] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)


def build_row(source: str, item: Item) -> dict[str, Any]:
    # `ingested_at` is left to the database default, so it is the real insertion time.
    return {
        "source": source,
        "external_id": item.external_id,
        "title": item.title,
        "body": item.body,
        "author": item.author,
        "url": item.url,
        "published_at": item.published_at.isoformat(),
        "raw_metadata": {"categories": list(item.categories)},
    }


def _ingest_feed(
    feed: Feed,
    now: datetime,
    fetch: Callable[[str], bytes],
    db: Db | None,
    report: Report,
) -> None:
    feed_report = FeedReport(source=feed.source)
    report.feeds.append(feed_report)
    try:
        result = parse_feed(fetch(feed.url))
    except (OSError, http.client.HTTPException, RuntimeError, ValueError) as error:
        report.problems.append(f"{feed.source}: {error}")
        return

    feed_report.skipped = list(result.skipped)
    items: list[Item] = []
    for item in result.items:
        if item.published_at > now + FUTURE_TOLERANCE:
            feed_report.skipped.append(
                f"{item.external_id}: pubDate is in the future ({item.published_at.isoformat()})"
            )
        else:
            items.append(item)
    feed_report.parsed = len(items)
    log.info("%s: %d items parsed, %d skipped", feed.source, len(items), len(feed_report.skipped))
    for reason in feed_report.skipped[:5]:
        log.warning("%s skipped %s", feed.source, reason)
    if not items:
        report.problems.append(
            f"{feed.source}: no usable items ({len(feed_report.skipped)} skipped)"
        )
        return

    dates = [item.published_at for item in items]
    feed_report.newest, feed_report.oldest = max(dates), min(dates)
    age = now - feed_report.newest
    log.info(
        "%s: newest %s (%.1f h ago), oldest %s",
        feed.source,
        feed_report.newest.isoformat(),
        age.total_seconds() / 3600,
        feed_report.oldest.isoformat(),
    )

    if db is None:
        feed_report.sample = items[:DRY_RUN_SAMPLE]
        for item in feed_report.sample:
            log.info("  dry run: %s | %s | %s", item.published_at, item.title, item.categories)
    else:
        rows = [build_row(feed.source, item) for item in items]
        for start in range(0, len(rows), BATCH_SIZE):
            inserted = db.insert_new(
                "content_items", rows[start : start + BATCH_SIZE], "source,external_id"
            )
            feed_report.inserted += len(inserted)
        log.info(
            "%s: %d new, %d already stored",
            feed.source,
            feed_report.inserted,
            len(rows) - feed_report.inserted,
        )

    if age > timedelta(hours=feed.max_age_hours):
        report.problems.append(
            f"{feed.source}: the newest item is {age.total_seconds() / 3600:.0f} hours old "
            f"(limit {feed.max_age_hours}); the feed may have stopped"
        )


def run(
    *,
    now: datetime,
    feeds: Sequence[Feed],
    fetch: Callable[[str], bytes],
    db: Db | None,
) -> Report:
    """Ingest every active feed. With `db=None` it fetches and parses but writes nothing."""
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    report = Report()
    for feed in feeds:
        if feed.active:
            _ingest_feed(feed, now, fetch, db, report)

    return report


def _require(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise RuntimeError(f"{name} is not set")
    return value


def main(argv: Sequence[str] | None = None, *, now: datetime | None = None) -> int:
    """Entrypoint for the scheduler. `now` exists so tests do not depend on the clock."""
    parser = argparse.ArgumentParser(prog="ingest", description="Ingest RSS feeds.")
    parser.add_argument(
        "--dry-run", action="store_true", help="fetch and print, write nothing to the database"
    )
    args = parser.parse_args(argv)
    dry_run = args.dry_run or os.environ.get("INGEST_DRY_RUN") == "true"

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    db = (
        None if dry_run else SupabaseRest(_require("SUPABASE_URL"), _require("SUPABASE_SECRET_KEY"))
    )

    report = run(now=now or datetime.now(UTC), feeds=FEEDS, fetch=fetch_feed, db=db)
    if report.problems:
        raise RuntimeError("; ".join(report.problems))
    return 0
