from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from extract import job
from extract.aliases import ALIASES
from extract.job import run
from prices.universe import UNIVERSE

NOW = datetime(2026, 10, 29, 15, 0, tzinfo=UTC)
COMPANIES = [
    {"id": "c-vz", "ticker": "VZ", "exchange": "NYSE", "name": "Verizon Communications Inc."},
    {"id": "c-t", "ticker": "T", "exchange": "NYSE", "name": "AT&T Inc."},
    {"id": "c-tmus", "ticker": "TMUS", "exchange": "NASDAQ", "name": "T-Mobile US, Inc."},
]


def item(
    key: str,
    title: str = "A headline",
    body: str = "",
    tags: list[str] | None = None,
    age_hours: float = 1.0,
) -> dict[str, Any]:
    return {
        "id": f"id-{key}",
        "source": "example",
        "external_id": key,
        "title": title,
        "body": body,
        "raw_metadata": {"categories": tags or []},
        "ingested_at": (NOW - timedelta(hours=age_hours)).isoformat(),
    }


class FakeDb:
    """Applies the filters, order and paging the job sends, and keeps the join table's key."""

    def __init__(self, items: list[dict[str, Any]], companies: list[dict[str, Any]] | None = None):
        self.items = items
        self.companies = COMPANIES if companies is None else companies
        self.selects: list[dict[str, str]] = []
        self.inserts: list[int] = []
        self.stored: dict[tuple[str, str], dict[str, Any]] = {}

    def select(self, table: str, query: dict[str, str]) -> list[dict[str, Any]]:
        if table == "companies":
            return list(self.companies)
        self.selects.append(query)
        since = datetime.fromisoformat(query["ingested_at"].removeprefix("gte."))
        rows = [r for r in self.items if datetime.fromisoformat(r["ingested_at"]) >= since]
        rows.sort(key=lambda r: (r["ingested_at"], r["id"]))
        start = int(query["offset"])
        return rows[start : start + int(query["limit"])]

    def insert_new(
        self, table: str, rows: list[dict[str, Any]], on_conflict: str
    ) -> list[dict[str, Any]]:
        assert table == "content_item_company_mentions"
        assert on_conflict == "content_item_id,company_id"
        self.inserts.append(len(rows))
        fresh = []
        for row in rows:
            key = (row["content_item_id"], row["company_id"])
            if key not in self.stored:
                self.stored[key] = row
                fresh.append(row)
        return fresh


def test_mentions_are_written_with_their_confidence() -> None:
    db = FakeDb(
        [
            item("1", tags=["NYSE:VZ"]),
            item("2", title="T-Mobile lifts its outlook"),
            item("3", title="Nothing about a carrier"),
        ]
    )

    report = run(now=NOW, hours=48, db=db, write=True)

    assert report.problems == [] and report.scanned == 3
    assert db.stored == {
        ("id-1", "c-vz"): {"content_item_id": "id-1", "company_id": "c-vz", "confidence": 1.0},
        ("id-2", "c-tmus"): {"content_item_id": "id-2", "company_id": "c-tmus", "confidence": 0.8},
    }
    assert report.inserted == {"VZ": 1, "TMUS": 1}


def test_a_second_run_adds_nothing() -> None:
    db = FakeDb([item("1", tags=["NYSE:VZ"])])
    run(now=NOW, hours=48, db=db, write=True)

    again = run(now=NOW + timedelta(hours=1), hours=48, db=db, write=True)

    assert again.inserted == {} and len(db.stored) == 1
    assert again.levels["VZ"][1.0] == 1  # still found, just not new


def test_only_items_inside_the_window_are_read() -> None:
    db = FakeDb([item("new", tags=["NYSE:VZ"], age_hours=2), item("old", age_hours=60)])

    report = run(now=NOW, hours=48, db=db, write=True)

    assert report.scanned == 1
    assert db.selects[0]["ingested_at"] == "gte." + (NOW - timedelta(hours=48)).isoformat()


def test_paging_reads_every_item(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(job, "PAGE_SIZE", 2)
    db = FakeDb([item(str(n), tags=["NYSE:VZ"], age_hours=n + 1) for n in range(5)])

    report = run(now=NOW, hours=48, db=db, write=True)

    assert report.scanned == 5 and len(db.stored) == 5
    assert [q["offset"] for q in db.selects] == ["0", "2", "4"]


def test_a_page_that_is_exactly_full_is_followed_by_one_more_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(job, "PAGE_SIZE", 2)
    db = FakeDb([item("1"), item("2")])

    run(now=NOW, hours=48, db=db, write=True)

    assert [q["offset"] for q in db.selects] == ["0", "2"]


def test_inserts_are_sent_in_batches(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(job, "BATCH_SIZE", 2)
    db = FakeDb([item(str(n), tags=["NYSE:VZ"]) for n in range(5)])

    run(now=NOW, hours=48, db=db, write=True)

    assert db.inserts == [2, 2, 1]


def test_a_dry_run_matches_but_writes_nothing() -> None:
    db = FakeDb([item("1", tags=["NYSE:VZ"])])

    report = run(now=NOW, hours=48, db=db, write=False)

    assert db.inserts == [] and report.inserted == {}
    assert report.levels["VZ"][1.0] == 1
    assert "dry run: nothing was written" in report.lines(wrote=False)


def test_ambiguous_cases_are_listed_by_item_id_and_never_by_headline() -> None:
    db = FakeDb(
        [
            item("a1", title="SECRET-HEADLINE Plan T rollout", body="SECRET-BODY text"),
            item("a2", tags=["NASDAQ:NVDA", "NASDAQ:NVDA", "NYSE:LMT"]),
        ]
    )

    report = run(now=NOW, hours=48, db=db, write=True)
    lines = report.lines(wrote=True)

    assert report.flagged == ["example/a1: T (bare symbol in the text)"]
    assert "tagged tickers that match no company (top 10): NASDAQ:NVDA 2, NYSE:LMT 1" in lines
    assert not any("SECRET" in line for line in lines)  # the log is public
    assert db.stored == {}


def test_the_report_counts_each_rule_per_company() -> None:
    db = FakeDb(
        [
            item("1", tags=["NYSE:VZ"]),
            item("2", title="Verizon outlook"),
            item("3", body="Verizon said"),
            item("4", title="(NYSE: VZ) moves"),
        ]
    )

    report = run(now=NOW, hours=48, db=db, write=True)

    assert "VZ: 4 items (tag 1, symbol 1, title 1, description 1), 4 new" in report.lines(
        wrote=True
    )


def test_an_empty_companies_table_is_a_problem() -> None:
    report = run(now=NOW, hours=48, db=FakeDb([item("1")], companies=[]), write=True)

    assert len(report.problems) == 1 and "companies table is empty" in report.problems[0]


@pytest.mark.parametrize(
    "raw", [None, "text", {"categories": "NYSE:VZ"}, {"categories": [1, None]}]
)
def test_odd_metadata_means_no_tags_not_a_crash(raw: object) -> None:
    broken = item("1")
    broken["raw_metadata"] = raw

    report = run(now=NOW, hours=48, db=FakeDb([broken]), write=True)

    assert report.scanned == 1 and report.problems == []


def test_a_naive_clock_and_a_zero_window_are_refused() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        run(now=datetime(2026, 10, 29, 12, 0), hours=48, db=FakeDb([]), write=True)
    with pytest.raises(ValueError, match="at least 1"):
        run(now=NOW, hours=0, db=FakeDb([]), write=True)


def test_every_company_in_the_prices_universe_has_names_here() -> None:
    # A ticker added to the prices universe and not to ALIASES would be found by symbol only.
    assert {company.ticker for company in UNIVERSE} == set(ALIASES)
    assert all(names for names in ALIASES.values())


def test_main_needs_the_database_secrets_even_for_a_dry_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="SUPABASE_URL"):
        job.main(["--dry-run"], now=NOW)


def test_main_dry_run_and_real_run(monkeypatch: pytest.MonkeyPatch) -> None:
    db = FakeDb([item("1", tags=["NYSE:VZ"])])
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SECRET_KEY", "secret")
    monkeypatch.setattr(job, "SupabaseRest", lambda url, key: db)
    monkeypatch.delenv("EXTRACT_DRY_RUN", raising=False)

    assert job.main(["--dry-run"], now=NOW) == 0
    assert db.stored == {}
    assert job.main([], now=NOW) == 0
    assert len(db.stored) == 1


def test_the_environment_selects_the_dry_run_and_the_window(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db = FakeDb([item("1", tags=["NYSE:VZ"], age_hours=100)])
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SECRET_KEY", "secret")
    monkeypatch.setattr(job, "SupabaseRest", lambda url, key: db)
    monkeypatch.setenv("EXTRACT_DRY_RUN", "true")
    monkeypatch.setenv("EXTRACT_HOURS", "120")

    assert job.main([], now=NOW) == 0
    assert db.stored == {} and db.selects[0]["ingested_at"].startswith("gte.2026-10-24")


def test_main_raises_when_there_is_a_problem(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SECRET_KEY", "secret")
    monkeypatch.setattr(job, "SupabaseRest", lambda url, key: FakeDb([], companies=[]))
    monkeypatch.delenv("EXTRACT_DRY_RUN", raising=False)

    with pytest.raises(RuntimeError, match="companies table is empty"):
        job.main([], now=NOW)
