"""Daily prices job (M1a, ADR-0004 D-34).

Records one daily bar per tracked company in price_snapshots, built from
Finnhub's free /quote. Every performance figure in the product derives from
this table (ARCHITECTURE.md, invariant 2), so the job refuses to write what it
cannot trust and fails loudly instead of "staying green" (CURSOR_RULES.md,
section 3).

How the date is chosen: the bar's date is the New York date of the quote's own
timestamp, not the date the job runs. That makes the job idempotent and needs no
market calendar: a run on a weekend, on a holiday or the next morning sees the
last session's quote again.

Which quote is kept: the first bar written for a session. A later run inserts only the
bars that are missing (that is what the 06:30 UTC run is for) and leaves a stored bar as
it is, printing a line when the new quote differs. Why: on 2026-10-29, one minute before the
open, Finnhub returned the previous session's figures restated (open +0.01, close +0.01 to
+0.04, same high, low and last-trade time), and an upsert wrote that over the evening bar,
which had matched the official close. The next-day check below caught it.
"""

from __future__ import annotations

import argparse
import logging
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta
from typing import Any, Protocol
from zoneinfo import ZoneInfo

from common.finnhub import Quote, fetch_quote
from common.supabase_rest import SupabaseRest
from prices.universe import UNIVERSE, Company

log = logging.getLogger("prices")

NEW_YORK = ZoneInfo("America/New_York")
SESSION_OPEN = time(9, 30)
SESSION_CLOSE = time(16, 0)
# Dollars. Finnhub's previous close and our stored close are both rounded by the source.
CLOSE_TOLERANCE = 0.005


class Db(Protocol):
    def upsert(
        self, table: str, rows: list[dict[str, Any]], on_conflict: str
    ) -> list[dict[str, Any]]: ...

    def insert_new(
        self, table: str, rows: list[dict[str, Any]], on_conflict: str
    ) -> list[dict[str, Any]]: ...

    def select(self, table: str, query: dict[str, str]) -> list[dict[str, Any]]: ...


@dataclass
class Report:
    rows: list[dict[str, Any]] = field(default_factory=list)
    written: bool = False
    skipped_session_open: bool = False
    problems: list[str] = field(default_factory=list)


def session_is_open(now: datetime) -> bool:
    """True while the US regular session is on (weekday, 09:30 to 16:00 New York).

    Why: a quote taken during the session is not a close, and writing it would
    put a half-day bar in the track record. Holidays are not modelled; a manual
    run inside the window on a holiday is refused, which is harmless.
    """
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    local = now.astimezone(NEW_YORK)
    return local.weekday() < 5 and SESSION_OPEN <= local.time() < SESSION_CLOSE


def trading_date(quote: Quote) -> date:
    """The New York date of the last trade (the UTC date is wrong after 20:00 New York)."""
    return datetime.fromtimestamp(quote.timestamp, tz=NEW_YORK).date()


def previous_weekday(day: date) -> date:
    """The weekday before `day` (Monday and the weekend go back to Friday).

    Holidays are not modelled, so a holiday gap is not detected by this alone.
    """
    step = 3 if day.weekday() == 0 else 2 if day.weekday() == 6 else 1
    return day - timedelta(days=step)


def check_quote(quote: Quote) -> list[str]:
    """Reasons not to trust a quote as a closing bar (empty list means it is fine).

    A close outside the day's range, or a zero open, high or low, is the sign of
    an extended-hours or pre-market price; a gap is better than a wrong close.
    """
    problems: list[str] = []
    if min(quote.open, quote.high, quote.low) <= 0:
        problems.append(f"{quote.ticker}: open, high or low is zero")
    elif not quote.low <= quote.current <= quote.high:
        problems.append(
            f"{quote.ticker}: close {quote.current} is outside the day's range "
            f"{quote.low}-{quote.high}"
        )
    elif not quote.low <= quote.open <= quote.high:
        problems.append(
            f"{quote.ticker}: open {quote.open} is outside the day's range {quote.low}-{quote.high}"
        )
    return problems


def build_row(company_id: str, day: date, quote: Quote) -> dict[str, Any]:
    """A price_snapshots row. `volume` is left out: the free /quote has none."""
    return {
        "company_id": company_id,
        "date": day.isoformat(),
        "open": quote.open,
        "high": quote.high,
        "low": quote.low,
        "close": quote.current,
    }


def run(
    *,
    now: datetime,
    fetch: Callable[[str], Quote],
    db: Db | None,
    universe: Sequence[Company] = UNIVERSE,
) -> Report:
    """Fetch every quote and record the bars not yet stored. `db=None` is a dry run."""
    report = Report()
    if session_is_open(now):
        report.skipped_session_open = True
        log.info("US session is open: a quote now is not a close, nothing written.")
        return report

    quotes: list[tuple[Company, Quote, date]] = []
    for company in universe:
        try:
            quote = fetch(company.ticker)
        except (RuntimeError, ValueError) as error:
            report.problems.append(str(error))
            continue
        issues = check_quote(quote)
        if issues:
            report.problems.extend(issues)
            continue
        quotes.append((company, quote, trading_date(quote)))

    days = sorted({day for _, _, day in quotes})
    if len(days) > 1:
        report.problems.append(
            f"quotes belong to different sessions: {[d.isoformat() for d in days]}"
        )

    ids: dict[str, str] = {}
    if db is not None and quotes:
        stored = db.upsert(
            "companies",
            [
                {
                    "ticker": c.ticker,
                    "name": c.name,
                    "exchange": c.exchange,
                    "sector": c.sector,
                }
                for c, _, _ in quotes
            ],
            "ticker,exchange",
        )
        ids = {row["ticker"]: str(row["id"]) for row in stored}

    for company, quote, day in quotes:
        company_id = ids.get(company.ticker, f"dry-run:{company.ticker}")
        report.rows.append(build_row(company_id, day, quote))
        log.info(
            "%s %s open=%s high=%s low=%s close=%s previous_close=%s last_trade=%s",
            company.ticker,
            day.isoformat(),
            quote.open,
            quote.high,
            quote.low,
            quote.current,
            quote.previous_close,
            datetime.fromtimestamp(quote.timestamp, tz=NEW_YORK).isoformat(),
        )
        if db is not None:
            report.problems.extend(_check_previous_close(db, company_id, day, quote))

    if db is not None and report.rows:
        inserted = db.insert_new("price_snapshots", report.rows, "company_id,date")
        report.written = True
        log.info(
            "Wrote %d new rows, %d already stored.", len(inserted), len(report.rows) - len(inserted)
        )
        new_ids = {str(row["company_id"]) for row in inserted}
        tickers = {company_id: ticker for ticker, company_id in ids.items()}
        for row in report.rows:
            if str(row["company_id"]) not in new_ids:
                _note_if_different(db, tickers.get(str(row["company_id"]), "?"), row)
    elif db is None:
        log.info("Dry run: nothing written to the database.")
    return report


def _note_if_different(db: Db, ticker: str, row: dict[str, Any]) -> None:
    """Print a line when the bar already stored differs from the quote just read.

    The stored bar is kept either way. The line is the only trace that the source restated
    a session, and the next day's previous-close check decides whether the stored bar is
    right."""
    stored = db.select(
        "price_snapshots",
        {
            "select": "open,high,low,close",
            "company_id": f"eq.{row['company_id']}",
            "date": f"eq.{row['date']}",
            "limit": "1",
        },
    )
    if not stored:
        return
    changes = [
        f"{field} {stored[0][field]} -> {row[field]}"
        for field in ("open", "high", "low", "close")
        if abs(float(stored[0][field]) - float(row[field])) > 1e-6
    ]
    if changes:
        log.warning(
            "%s %s: kept the stored bar; this quote differs: %s",
            ticker,
            row["date"],
            ", ".join(changes),
        )


def _check_previous_close(db: Db, company_id: str, day: date, quote: Quote) -> list[str]:
    """Compare Finnhub's previous close with the close we stored for that session.

    Why: the stored close is a last-trade price taken after the session; the
    next day's previous close is the official one. If they differ, the track
    record is off and someone must look. Only checked when the stored row is the
    immediately preceding weekday, so a missing session is not mistaken for a
    mismatch.
    """
    prior = db.select(
        "price_snapshots",
        {
            "select": "date,close",
            "company_id": f"eq.{company_id}",
            "date": f"lt.{day.isoformat()}",
            "order": "date.desc",
            "limit": "1",
        },
    )
    if not prior or date.fromisoformat(str(prior[0]["date"])) != previous_weekday(day):
        return []
    stored = float(prior[0]["close"])
    if abs(stored - quote.previous_close) > CLOSE_TOLERANCE:
        return [
            f"{quote.ticker}: stored close {stored} for {prior[0]['date']} differs from "
            f"Finnhub's previous close {quote.previous_close}"
        ]
    return []


def _require(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise RuntimeError(f"{name} is not set")
    return value


def main(argv: Sequence[str] | None = None, *, now: datetime | None = None) -> int:
    """Entrypoint for the scheduler. `now` exists so tests do not depend on the clock."""
    parser = argparse.ArgumentParser(prog="prices", description="Record daily prices.")
    parser.add_argument(
        "--dry-run", action="store_true", help="fetch and print, write nothing to the database"
    )
    args = parser.parse_args(argv)
    dry_run = args.dry_run or os.environ.get("PRICES_DRY_RUN") == "true"

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    finnhub_key = _require("FINNHUB_API_KEY")
    db = (
        None if dry_run else SupabaseRest(_require("SUPABASE_URL"), _require("SUPABASE_SECRET_KEY"))
    )

    report = run(
        now=now or datetime.now(UTC),
        fetch=lambda ticker: fetch_quote(ticker, finnhub_key),
        db=db,
    )
    if report.problems:
        raise RuntimeError("; ".join(report.problems))
    return 0
