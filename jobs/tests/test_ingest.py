from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from ingest import job
from ingest.feeds import FEEDS, Feed
from ingest.job import build_row, run
from ingest.rss import parse_feed

NOW = datetime(2026, 10, 29, 12, 17, tzinfo=UTC)
FEED = Feed(source="example", name="Example", url="https://news.example.com/feed/")


def rfc822(when: datetime) -> str:
    return when.strftime("%a, %d %b %Y %H:%M:%S GMT")


def make_feed(count: int = 3, newest_age_hours: float = 2.0, start: int = 0) -> bytes:
    items = "".join(
        f"<item><title>Story {n}</title><link>https://news.example.com/{n}</link>"
        f'<guid isPermaLink="false">id{n}</guid>'
        f"<pubDate>{rfc822(NOW - timedelta(hours=newest_age_hours + n))}</pubDate>"
        f"<description>Summary {n}</description><category>NYSE:VZ</category></item>"
        for n in range(start, start + count)
    )
    return f'<rss version="2.0"><channel>{items}</channel></rss>'.encode()


class FakeDb:
    """Keeps (source, external_id) like the real unique key and returns only new rows."""

    def __init__(self) -> None:
        self.stored: dict[tuple[str, str], dict[str, Any]] = {}
        self.calls: list[tuple[str, int, str]] = []

    def insert_new(
        self, table: str, rows: list[dict[str, Any]], on_conflict: str
    ) -> list[dict[str, Any]]:
        self.calls.append((table, len(rows), on_conflict))
        fresh = []
        for row in rows:
            key = (row["source"], row["external_id"])
            if key not in self.stored:
                self.stored[key] = row
                fresh.append(row)
        return fresh


def test_inserts_new_items_and_reports_the_counts() -> None:
    db = FakeDb()

    report = run(now=NOW, feeds=[FEED], fetch=lambda url: make_feed(3), db=db)

    assert report.problems == []
    assert report.feeds[0].parsed == 3 and report.feeds[0].inserted == 3
    assert db.calls == [("content_items", 3, "source,external_id")]
    assert len(db.stored) == 3


def test_the_row_matches_the_content_items_columns() -> None:
    item = parse_feed(make_feed(1)).items[0]

    row = build_row("example", item)

    assert row == {
        "source": "example",
        "external_id": "id0",
        "title": "Story 0",
        "body": "Summary 0",
        "author": None,
        "url": "https://news.example.com/0",
        "published_at": (NOW - timedelta(hours=2)).isoformat(),
        "raw_metadata": {"categories": ["NYSE:VZ"]},
    }
    # ingested_at is the database's now(), and id its own default.
    assert "ingested_at" not in row and "id" not in row


def test_a_second_run_adds_nothing() -> None:
    db = FakeDb()
    run(now=NOW, feeds=[FEED], fetch=lambda url: make_feed(3), db=db)

    again = run(now=NOW + timedelta(hours=1), feeds=[FEED], fetch=lambda url: make_feed(3), db=db)

    assert again.problems == []
    assert again.feeds[0].parsed == 3 and again.feeds[0].inserted == 0
    assert len(db.stored) == 3


def test_a_changed_item_keeps_the_first_copy() -> None:
    db = FakeDb()
    run(now=NOW, feeds=[FEED], fetch=lambda url: make_feed(1), db=db)
    edited = make_feed(1).replace(b"Story 0", b"Story 0 (edited)")

    run(now=NOW, feeds=[FEED], fetch=lambda url: edited, db=db)

    assert db.stored[("example", "id0")]["title"] == "Story 0"


def test_only_the_new_items_count_as_inserted() -> None:
    db = FakeDb()
    run(now=NOW, feeds=[FEED], fetch=lambda url: make_feed(3), db=db)

    # Next hour: one new story on top of the three already stored.
    second = run(
        now=NOW + timedelta(hours=1),
        feeds=[FEED],
        fetch=lambda url: make_feed(4, newest_age_hours=1.0),
        db=db,
    )

    # Story ids id0..id3 : id0..id2 exist, id3 is new.
    assert second.feeds[0].parsed == 4 and second.feeds[0].inserted == 1


def test_large_feeds_are_sent_in_batches() -> None:
    db = FakeDb()

    run(now=NOW, feeds=[FEED], fetch=lambda url: make_feed(250), db=db)

    assert [size for _, size, _ in db.calls] == [100, 100, 50]


def test_dry_run_fetches_and_parses_but_writes_nothing() -> None:
    report = run(now=NOW, feeds=[FEED], fetch=lambda url: make_feed(5), db=None)

    assert report.problems == []
    assert report.feeds[0].parsed == 5 and report.feeds[0].inserted == 0
    assert len(report.feeds[0].sample) == job.DRY_RUN_SAMPLE


def test_inactive_feeds_are_not_fetched() -> None:
    fetched: list[str] = []
    off = Feed(source="off", name="Off", url="https://off.example.com/", active=False)

    def fetch(url: str) -> bytes:
        fetched.append(url)
        return make_feed(1)

    report = run(now=NOW, feeds=[off, FEED], fetch=fetch, db=FakeDb())

    assert fetched == [FEED.url]
    assert [feed.source for feed in report.feeds] == ["example"]


def test_a_stale_feed_is_written_and_then_flagged() -> None:
    db = FakeDb()

    report = run(now=NOW, feeds=[FEED], fetch=lambda url: make_feed(2, newest_age_hours=100), db=db)

    assert len(db.stored) == 2
    assert len(report.problems) == 1
    assert "example" in report.problems[0] and "hours old" in report.problems[0]


def test_a_feed_just_inside_its_age_limit_is_fine() -> None:
    report = run(
        now=NOW, feeds=[FEED], fetch=lambda url: make_feed(2, newest_age_hours=71), db=None
    )

    assert report.problems == []


def test_a_feed_with_no_usable_items_is_a_problem() -> None:
    empty = b'<rss version="2.0"><channel></channel></rss>'

    report = run(now=NOW, feeds=[FEED], fetch=lambda url: empty, db=FakeDb())

    assert report.problems == ["example: no usable items (0 skipped)"]


def test_future_dated_items_are_skipped_not_trusted() -> None:
    future = NOW + timedelta(days=30)
    xml = (
        f"<rss><channel><item><title>T</title><link>https://a.example/x</link>"
        f"<pubDate>{rfc822(future)}</pubDate></item></channel></rss>"
    ).encode()
    db = FakeDb()

    report = run(now=NOW, feeds=[FEED], fetch=lambda url: xml, db=db)

    assert db.stored == {}
    assert len(report.problems) == 1 and "no usable items (1 skipped)" in report.problems[0]


@pytest.mark.parametrize(
    "failure",
    [
        OSError("connection reset"),
        RuntimeError("https://news.example.com/feed/ answered HTTP 403"),
        ValueError("feed is not valid XML"),
    ],
)
def test_a_failing_feed_is_reported_and_the_others_still_run(failure: Exception) -> None:
    broken = Feed(source="broken", name="Broken", url="https://broken.example.com/")

    def fetch(url: str) -> bytes:
        if url == broken.url:
            raise failure
        return make_feed(2)

    db = FakeDb()
    report = run(now=NOW, feeds=[broken, FEED], fetch=fetch, db=db)

    assert len(report.problems) == 1 and report.problems[0].startswith("broken: ")
    assert len(db.stored) == 2


def test_naive_now_is_refused() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        run(now=datetime(2026, 10, 29, 12, 0), feeds=[FEED], fetch=lambda url: b"", db=None)


def test_the_feed_list_is_sane() -> None:
    sources = [feed.source for feed in FEEDS]

    assert len(sources) == len(set(sources))
    assert all(feed.url.startswith("https://") for feed in FEEDS)
    assert all(feed.max_age_hours > 0 for feed in FEEDS)
    assert all(feed.note for feed in FEEDS)  # every entry says why it is on or off
    # The feeds the founder switched on (m0/rss-feeds.md). Adding a name here is the review
    # step, so it should never happen by accident.
    assert {feed.source for feed in FEEDS if feed.active} == {
        "marketbeat",
        "fed-press",
        "cnbc-top",
        "marketwatch-top",
    }


def test_no_active_feed_is_a_problem_not_a_silent_green() -> None:
    off = Feed(source="off", name="Off", url="https://off.example.com/", active=False)

    report = run(now=NOW, feeds=[off], fetch=lambda url: make_feed(1), db=FakeDb())

    assert report.feeds == []
    assert report.problems == ["no feed is active, so there is nothing to ingest"]


def test_probe_mode_fetches_the_switched_off_feeds_too() -> None:
    off = Feed(
        source="off", name="Off", url="https://off.example.com/", active=False, note="try me"
    )
    fetched: list[str] = []

    def fetch(url: str) -> bytes:
        fetched.append(url)
        return make_feed(2)

    report = run(now=NOW, feeds=[off, FEED], fetch=fetch, db=None, include_inactive=True)

    assert fetched == [off.url, FEED.url]
    assert report.problems == []
    lines = job.probe_lines(report, [off, FEED], NOW)
    assert (
        lines[0].startswith("probe off: answered, 2 items, newest 2.0 h ago")
        and "[try me]" in lines[0]
    )
    assert lines[1].startswith("probe example: answered")


def test_probe_mode_names_each_failure() -> None:
    blocked = Feed(source="blocked", name="Blocked", url="https://blocked.example.com/")

    def fetch(url: str) -> bytes:
        if url == blocked.url:
            raise OSError("The read operation timed out")
        return make_feed(1, newest_age_hours=100)

    feeds = [blocked, FEED]
    report = run(now=NOW, feeds=feeds, fetch=fetch, db=None, include_inactive=True)

    lines = job.probe_lines(report, feeds, NOW)
    assert lines[0] == "probe blocked: FAILED  The read operation timed out"
    assert "answered, 1 items" in lines[1] and "hours old" in lines[1]


def test_probe_mode_never_writes() -> None:
    with pytest.raises(ValueError, match="dry run"):
        run(
            now=NOW,
            feeds=[FEED],
            fetch=lambda url: make_feed(1),
            db=FakeDb(),
            include_inactive=True,
        )


def test_main_dry_run_needs_no_database_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SECRET_KEY", raising=False)
    monkeypatch.setattr(job, "FEEDS", (FEED,))
    monkeypatch.setattr(job, "fetch_feed", lambda url: make_feed(2))

    assert job.main(["--dry-run"], now=NOW) == 0


def test_main_requires_the_database_secrets_for_a_real_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SECRET_KEY", raising=False)
    monkeypatch.delenv("INGEST_DRY_RUN", raising=False)

    with pytest.raises(RuntimeError, match="SUPABASE_URL"):
        job.main([], now=NOW)


def test_main_raises_when_a_feed_has_a_problem(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(job, "FEEDS", (FEED,))
    monkeypatch.setattr(job, "fetch_feed", lambda url: make_feed(2, newest_age_hours=200))

    with pytest.raises(RuntimeError, match="hours old"):
        job.main(["--dry-run"], now=NOW)


def test_main_raises_when_no_feed_is_active(monkeypatch: pytest.MonkeyPatch) -> None:
    off = Feed(source="off", name="Off", url="https://off.example.com/", active=False)
    monkeypatch.setattr(job, "FEEDS", (off,))

    with pytest.raises(RuntimeError, match="no feed is active"):
        job.main(["--dry-run"], now=NOW)


def test_main_probe_reports_failures_without_failing(monkeypatch: pytest.MonkeyPatch) -> None:
    off = Feed(source="off", name="Off", url="https://off.example.com/", active=False)

    def fetch(url: str) -> bytes:
        raise OSError("connection closed")

    monkeypatch.setattr(job, "FEEDS", (off, FEED))
    monkeypatch.setattr(job, "fetch_feed", fetch)

    assert job.main(["--dry-run", "--include-inactive"], now=NOW) == 0


def test_main_refuses_probe_mode_without_dry_run(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("INGEST_DRY_RUN", raising=False)

    with pytest.raises(RuntimeError, match="only allowed on a dry run"):
        job.main(["--include-inactive"], now=NOW)


def test_the_environment_variables_also_select_probe_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    off = Feed(source="off", name="Off", url="https://off.example.com/", active=False)
    monkeypatch.setenv("INGEST_DRY_RUN", "true")
    monkeypatch.setenv("INGEST_INCLUDE_INACTIVE", "true")
    monkeypatch.setattr(job, "FEEDS", (off,))
    monkeypatch.setattr(job, "fetch_feed", lambda url: make_feed(1))

    assert job.main([], now=NOW) == 0


def test_the_environment_variable_also_selects_a_dry_run(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.setenv("INGEST_DRY_RUN", "true")
    monkeypatch.delenv("INGEST_INCLUDE_INACTIVE", raising=False)
    monkeypatch.setattr(job, "FEEDS", (FEED,))
    monkeypatch.setattr(job, "fetch_feed", lambda url: make_feed(1))

    assert job.main([], now=NOW) == 0
