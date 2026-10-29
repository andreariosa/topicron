"""Hourly extraction job (M1b, ADR-0004 D-34).

Reads the content items stored in the last few hours and records which of the companies in
the `companies` table each one mentions (docs/AI_SYSTEM.md, Agent 1; rules in matching.py).
Zero LLM cost (ADR-0002). Cases the rules cannot settle are listed in the log, not decided.

There is no "processed" flag on content_items: every run looks again at a window of recent
items and the primary key of the join table makes a repeat harmless. The window is wide
(48 hours) because GitHub's schedule is best effort and has run hours late. A longer outage
is repaired by running by hand with a longer window.

The log is public (the repository is), so it carries item ids and tickers, never headlines.
"""

from __future__ import annotations

import argparse
import logging
import os
from collections import Counter
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol

from common.supabase_rest import SupabaseRest
from extract.aliases import ALIASES
from extract.matching import NAME_IN_BODY, NAME_IN_TITLE, SYMBOL_IN_TEXT, TAG, Target, extract

log = logging.getLogger("extract")

DEFAULT_HOURS = 48
PAGE_SIZE = 500  # PostgREST returns at most 1000 rows per request
BATCH_SIZE = 100
TOP_UNKNOWN = 10
TABLE = "content_item_company_mentions"
LEVELS = {
    TAG: "tag",
    SYMBOL_IN_TEXT: "symbol",
    NAME_IN_TITLE: "title",
    NAME_IN_BODY: "description",
}


class Db(Protocol):
    def select(self, table: str, query: dict[str, str]) -> list[dict[str, Any]]: ...

    def insert_new(
        self, table: str, rows: list[dict[str, Any]], on_conflict: str
    ) -> list[dict[str, Any]]: ...


@dataclass
class Report:
    since: datetime
    hours: int
    scanned: int = 0
    levels: dict[str, Counter[float]] = field(default_factory=dict)
    inserted: dict[str, int] = field(default_factory=dict)
    flagged: list[str] = field(default_factory=list)
    unknown: Counter[str] = field(default_factory=Counter)
    problems: list[str] = field(default_factory=list)

    def lines(self, *, wrote: bool) -> list[str]:
        out = [
            f"scanned {self.scanned} items ingested since {self.since.isoformat()} ({self.hours} h)"
        ]
        for ticker in sorted(self.levels):
            counts = self.levels[ticker]
            detail = ", ".join(f"{name} {counts[level]}" for level, name in LEVELS.items())
            tail = f", {self.inserted.get(ticker, 0)} new" if wrote else ""
            out.append(f"{ticker}: {sum(counts.values())} items ({detail}){tail}")
        if not wrote:
            out.append("dry run: nothing was written")
        out.append(f"ambiguous, logged and not resolved: {len(self.flagged)}")
        out.extend(f"  {line}" for line in self.flagged)
        top = ", ".join(f"{tag} {count}" for tag, count in self.unknown.most_common(TOP_UNKNOWN))
        out.append(f"tagged tickers that match no company (top {TOP_UNKNOWN}): {top or 'none'}")
        return out


def _load_targets(db: Db) -> list[Target]:
    rows = db.select("companies", {"select": "id,ticker,exchange"})
    return [
        Target(str(r["id"]), r["ticker"], r["exchange"], ALIASES.get(r["ticker"], ())) for r in rows
    ]


def _recent_items(db: Db, since: datetime) -> Iterator[dict[str, Any]]:
    offset = 0
    while True:
        page = db.select(
            "content_items",
            {
                "select": "id,source,external_id,title,body,raw_metadata",
                "ingested_at": f"gte.{since.isoformat()}",
                # A stable order is what makes paging by offset safe.
                "order": "ingested_at.asc,id.asc",
                "limit": str(PAGE_SIZE),
                "offset": str(offset),
            },
        )
        yield from page
        if len(page) < PAGE_SIZE:
            return
        offset += PAGE_SIZE


def _categories(raw_metadata: object) -> list[str]:
    if not isinstance(raw_metadata, dict):
        return []
    categories = raw_metadata.get("categories")
    if not isinstance(categories, list):
        return []
    return [c for c in categories if isinstance(c, str)]


def run(*, now: datetime, hours: int, db: Db, write: bool) -> Report:
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    if hours < 1:
        raise ValueError("hours must be at least 1")
    report = Report(since=now - timedelta(hours=hours), hours=hours)
    targets = _load_targets(db)
    if not targets:
        report.problems.append("the companies table is empty, so there is nothing to match")
        return report

    pending: list[dict[str, Any]] = []
    tickers = {t.company_id: t.ticker for t in targets}
    for item in _recent_items(db, report.since):
        report.scanned += 1
        result = extract(
            item["title"] or "", item["body"] or "", _categories(item["raw_metadata"]), targets
        )
        for mention in result.mentions:
            report.levels.setdefault(mention.ticker, Counter())[mention.confidence] += 1
            pending.append(
                {
                    "content_item_id": item["id"],
                    "company_id": mention.company_id,
                    "confidence": mention.confidence,
                }
            )
        for flag in sorted(set((f.ticker, f.reason) for f in result.flags)):
            ref = f"{item['source']}/{item['external_id']}"[:100]
            report.flagged.append(f"{ref}: {flag[0]} ({flag[1]})")
        report.unknown.update(result.unknown_tags)

    if write:
        for start in range(0, len(pending), BATCH_SIZE):
            batch = pending[start : start + BATCH_SIZE]
            for row in db.insert_new(TABLE, batch, "content_item_id,company_id"):
                ticker = tickers[str(row["company_id"])]
                report.inserted[ticker] = report.inserted.get(ticker, 0) + 1
    return report


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is not set")
    return value


def main(argv: Sequence[str] | None = None, *, now: datetime | None = None) -> int:
    """Entrypoint for the scheduler. `now` exists so tests do not depend on the clock."""
    parser = argparse.ArgumentParser(
        prog="extract", description="Match companies in content items."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="read and match, write nothing to the database"
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=int(os.environ.get("EXTRACT_HOURS") or DEFAULT_HOURS),
        help=f"look at items ingested in the last N hours (default {DEFAULT_HOURS})",
    )
    args = parser.parse_args(argv)
    write = not (args.dry_run or os.environ.get("EXTRACT_DRY_RUN") == "true")

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Reading needs the key too, so a dry run is not secret-free like the ingest one.
    db = SupabaseRest(_require("SUPABASE_URL"), _require("SUPABASE_SECRET_KEY"))
    report = run(now=now or datetime.now(UTC), hours=args.hours, db=db, write=write)
    for line in report.lines(wrote=write):
        log.info(line)
    if report.problems:
        raise RuntimeError("; ".join(report.problems))
    return 0
