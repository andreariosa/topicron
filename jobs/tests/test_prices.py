from datetime import UTC, date, datetime
from typing import Any

import pytest

from common.finnhub import Quote
from prices import job
from prices.job import (
    check_quote,
    previous_weekday,
    run,
    session_is_open,
    trading_date,
)
from prices.universe import UNIVERSE

# New York is UTC-4 until Sunday 2026-11-01 and UTC-5 after it.
CLOSED_EVENING = datetime(2026, 10, 27, 22, 0, tzinfo=UTC)  # Tuesday 18:00 New York


def at(year: int, month: int, day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=UTC)


def make_quote(
    ticker: str,
    close: float = 40.0,
    when: datetime | None = None,
    previous_close: float = 39.0,
) -> Quote:
    when = when or at(2026, 10, 26, 20, 0)  # Monday 16:00 New York
    return Quote(
        ticker=ticker,
        current=close,
        open=close - 0.5,
        high=close + 1.0,
        low=close - 1.0,
        previous_close=previous_close,
        timestamp=int(when.timestamp()),
    )


class FakeDb:
    """In-memory stand-in with the same upsert and select behaviour as the REST client."""

    def __init__(self) -> None:
        self.companies: dict[tuple[str, str], dict[str, Any]] = {}
        self.snapshots: dict[tuple[str, str], dict[str, Any]] = {}

    def upsert(
        self, table: str, rows: list[dict[str, Any]], on_conflict: str
    ) -> list[dict[str, Any]]:
        if table == "companies":
            out = []
            for row in rows:
                stored = self.companies.setdefault(
                    (row["ticker"], row["exchange"]), {"id": f"id-{row['ticker']}"}
                )
                stored.update(row)
                out.append(dict(stored))
            return out
        if table == "price_snapshots":
            for row in rows:
                key = (row["company_id"], row["date"])
                self.snapshots[key] = {**self.snapshots.get(key, {}), **row}
            return rows
        raise AssertionError(f"unexpected table {table}")

    def select(self, table: str, query: dict[str, str]) -> list[dict[str, Any]]:
        assert table == "price_snapshots"
        company_id = query["company_id"].removeprefix("eq.")
        before = query["date"].removeprefix("lt.")
        earlier = sorted(
            (
                row
                for (cid, day), row in self.snapshots.items()
                if cid == company_id and day < before
            ),
            key=lambda row: str(row["date"]),
            reverse=True,
        )
        return [{"date": row["date"], "close": row["close"]} for row in earlier[:1]]


def fetch_all(
    when: datetime | None = None, previous_close: float = 39.0, **overrides: Quote
) -> Any:
    """A fetch that returns one quote per ticker, all for the session of `when`."""

    def fetch(ticker: str) -> Quote:
        return overrides.get(ticker) or make_quote(ticker, when=when, previous_close=previous_close)

    return fetch


# --- session_is_open -------------------------------------------------------


def test_session_is_open_during_regular_hours_in_summer_time() -> None:
    assert session_is_open(at(2026, 10, 27, 13, 30))  # 09:30 EDT
    assert session_is_open(at(2026, 10, 27, 19, 59))  # 15:59 EDT


def test_session_is_closed_before_the_open_and_from_the_close() -> None:
    assert not session_is_open(at(2026, 10, 27, 13, 29))
    assert not session_is_open(at(2026, 10, 27, 20, 0))  # 16:00 EDT


def test_session_hours_follow_the_clock_change_on_1_november() -> None:
    assert not session_is_open(at(2026, 11, 3, 14, 29))  # 09:29 EST
    assert session_is_open(at(2026, 11, 3, 14, 30))  # 09:30 EST
    assert not session_is_open(at(2026, 11, 3, 21, 0))  # 16:00 EST


def test_session_is_closed_on_weekends() -> None:
    assert not session_is_open(at(2026, 10, 31, 15, 0))  # Saturday


def test_session_check_needs_an_aware_datetime() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        session_is_open(datetime(2026, 10, 27, 15, 0))


# --- dates -----------------------------------------------------------------


def test_trading_date_is_the_new_york_date() -> None:
    assert trading_date(make_quote("VZ", when=at(2026, 10, 26, 20, 0))) == date(2026, 10, 26)
    # 00:30 UTC on the 27th is still the evening of the 26th in New York.
    assert trading_date(make_quote("VZ", when=at(2026, 10, 27, 0, 30))) == date(2026, 10, 26)


def test_previous_weekday_skips_the_weekend() -> None:
    assert previous_weekday(date(2026, 10, 27)) == date(2026, 10, 26)  # Tuesday
    assert previous_weekday(date(2026, 11, 2)) == date(2026, 10, 30)  # Monday
    assert previous_weekday(date(2026, 11, 1)) == date(2026, 10, 30)  # Sunday


# --- check_quote -----------------------------------------------------------


def test_a_consistent_quote_has_no_problems() -> None:
    assert check_quote(make_quote("VZ")) == []


def test_a_close_outside_the_days_range_is_refused() -> None:
    quote = Quote("VZ", 45.0, 40.0, 41.0, 39.0, 39.5, 1_793_000_000)
    assert "outside the day's range" in check_quote(quote)[0]


def test_an_open_outside_the_days_range_is_refused() -> None:
    quote = Quote("VZ", 40.0, 42.0, 41.0, 39.0, 39.5, 1_793_000_000)
    assert "open" in check_quote(quote)[0]


def test_a_zero_high_low_or_open_is_refused() -> None:
    quote = Quote("VZ", 40.0, 0.0, 41.0, 39.0, 39.5, 1_793_000_000)
    assert "zero" in check_quote(quote)[0]


# --- run -------------------------------------------------------------------


def test_dry_run_builds_every_row_and_writes_nothing() -> None:
    report = run(now=CLOSED_EVENING, fetch=fetch_all(), db=None)

    assert report.problems == []
    assert not report.written
    assert [row["company_id"] for row in report.rows] == [f"dry-run:{c.ticker}" for c in UNIVERSE]
    assert {row["date"] for row in report.rows} == {"2026-10-26"}


def test_nothing_is_fetched_or_written_while_the_session_is_open() -> None:
    def fetch(ticker: str) -> Quote:
        raise AssertionError("must not fetch during the session")

    db = FakeDb()
    report = run(now=at(2026, 10, 27, 15, 0), fetch=fetch, db=db)

    assert report.skipped_session_open
    assert report.rows == [] and db.snapshots == {} and db.companies == {}


def test_rows_and_companies_are_written() -> None:
    db = FakeDb()
    report = run(now=CLOSED_EVENING, fetch=fetch_all(), db=db)

    assert report.written and report.problems == []
    assert len(db.companies) == 4
    assert len(db.snapshots) == 4
    row = db.snapshots[("id-VZ", "2026-10-26")]
    assert row["close"] == 40.0
    assert "volume" not in row  # the free quote has no volume


def test_running_twice_does_not_duplicate_rows() -> None:
    db = FakeDb()
    run(now=CLOSED_EVENING, fetch=fetch_all(), db=db)
    run(now=at(2026, 10, 28, 6, 30), fetch=fetch_all(), db=db)  # the catch-up run

    assert len(db.snapshots) == 4
    assert len(db.companies) == 4


def test_a_matching_previous_close_the_next_day_is_fine() -> None:
    db = FakeDb()
    run(now=CLOSED_EVENING, fetch=fetch_all(), db=db)  # stores Monday 26: close 40.0

    tuesday = at(2026, 10, 27, 20, 0)
    report = run(
        now=at(2026, 10, 27, 22, 0),
        fetch=fetch_all(tuesday, 40.0, VZ=make_quote("VZ", 41.0, tuesday, previous_close=40.0)),
        db=db,
    )

    assert report.problems == []


def test_a_different_previous_close_is_reported_after_the_rows_are_written() -> None:
    db = FakeDb()
    run(now=CLOSED_EVENING, fetch=fetch_all(), db=db)

    tuesday = at(2026, 10, 27, 20, 0)
    report = run(
        now=at(2026, 10, 27, 22, 0),
        fetch=fetch_all(tuesday, 40.0, VZ=make_quote("VZ", 41.0, tuesday, previous_close=39.0)),
        db=db,
    )

    assert len(report.problems) == 1
    assert "VZ" in report.problems[0] and "previous close" in report.problems[0]
    assert report.written
    assert ("id-VZ", "2026-10-27") in db.snapshots


def test_a_missing_session_is_not_mistaken_for_a_mismatch() -> None:
    db = FakeDb()
    run(now=CLOSED_EVENING, fetch=fetch_all(), db=db)  # stores Monday 26

    thursday = at(2026, 10, 29, 20, 0)  # Tuesday and Wednesday are missing
    report = run(
        now=at(2026, 10, 29, 22, 0),
        fetch=fetch_all(thursday, VZ=make_quote("VZ", 41.0, thursday, previous_close=99.0)),
        db=db,
    )

    assert report.problems == []


def test_a_failed_fetch_is_reported_and_the_others_are_still_written() -> None:
    def fetch(ticker: str) -> Quote:
        if ticker == "T":
            raise RuntimeError("T: Finnhub answered HTTP 429")
        return make_quote(ticker)

    db = FakeDb()
    report = run(now=CLOSED_EVENING, fetch=fetch, db=db)

    assert report.problems == ["T: Finnhub answered HTTP 429"]
    assert len(db.snapshots) == 3
    assert report.written


def test_an_untrustworthy_quote_is_left_out_and_reported() -> None:
    bad = Quote("TMUS", 99.0, 40.0, 41.0, 39.0, 39.0, int(at(2026, 10, 26, 20, 0).timestamp()))
    db = FakeDb()
    report = run(now=CLOSED_EVENING, fetch=fetch_all(TMUS=bad), db=db)

    assert len(report.problems) == 1 and "TMUS" in report.problems[0]
    assert ("id-TMUS", "2026-10-26") not in db.snapshots
    assert len(db.snapshots) == 3


def test_quotes_from_different_sessions_are_reported() -> None:
    stale = make_quote("T", when=at(2026, 10, 23, 20, 0))  # the Friday before
    report = run(now=CLOSED_EVENING, fetch=fetch_all(T=stale), db=None)

    assert any("different sessions" in problem for problem in report.problems)


# --- main ------------------------------------------------------------------


def _patch_fetch(monkeypatch: pytest.MonkeyPatch, **overrides: Quote) -> None:
    def fake(ticker: str, api_key: str) -> Quote:
        return overrides.get(ticker) or make_quote(ticker)

    monkeypatch.setattr(job, "fetch_quote", fake)


def test_main_dry_run_needs_only_the_finnhub_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "k")
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SECRET_KEY", raising=False)
    _patch_fetch(monkeypatch)

    assert job.main(["--dry-run"], now=CLOSED_EVENING) == 0


def test_main_dry_run_can_be_set_by_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "k")
    monkeypatch.setenv("PRICES_DRY_RUN", "true")
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    _patch_fetch(monkeypatch)

    assert job.main([], now=CLOSED_EVENING) == 0


def test_main_names_a_missing_variable_without_printing_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("FINNHUB_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="FINNHUB_API_KEY is not set"):
        job.main(["--dry-run"])

    monkeypatch.setenv("FINNHUB_API_KEY", "super-secret")
    monkeypatch.delenv("PRICES_DRY_RUN", raising=False)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="SUPABASE_URL is not set") as error:
        job.main([])
    assert "super-secret" not in str(error.value)


def test_main_fails_loudly_when_there_are_problems(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINNHUB_API_KEY", "k")
    _patch_fetch(monkeypatch, VZ=Quote("VZ", 50.0, 40.0, 41.0, 39.0, 39.0, 1_793_000_000))

    with pytest.raises(RuntimeError, match="VZ"):
        job.main(["--dry-run"], now=CLOSED_EVENING)
