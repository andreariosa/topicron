import json

import pytest

from common.supabase_rest import SupabaseRest

NEW_KEY = "sb_secret_fake_for_tests"
LEGACY_KEY = "eyJ-fake-legacy-key-for-tests"


class Recorder:
    def __init__(self, status: int = 200, body: bytes = b"[]") -> None:
        self.status = status
        self.body = body
        self.calls: list[tuple[str, str, dict[str, str], bytes | None]] = []

    def __call__(
        self, method: str, url: str, headers: dict[str, str], body: bytes | None
    ) -> tuple[int, bytes]:
        self.calls.append((method, url, headers, body))
        return self.status, self.body


def test_requires_https() -> None:
    with pytest.raises(ValueError, match="https"):
        SupabaseRest("http://example.supabase.co", NEW_KEY)


def test_new_secret_key_goes_in_apikey_only() -> None:
    recorder = Recorder()
    SupabaseRest("https://x.supabase.co", NEW_KEY, recorder).select("companies", {})

    headers = recorder.calls[0][2]
    assert headers["apikey"] == NEW_KEY
    assert "Authorization" not in headers


def test_legacy_jwt_key_is_also_sent_as_bearer() -> None:
    recorder = Recorder()
    SupabaseRest("https://x.supabase.co", LEGACY_KEY, recorder).select("companies", {})

    headers = recorder.calls[0][2]
    assert headers["apikey"] == LEGACY_KEY
    assert headers["Authorization"] == f"Bearer {LEGACY_KEY}"


def test_upsert_builds_the_postgrest_request() -> None:
    rows = [{"ticker": "VZ", "exchange": "NYSE"}]
    recorder = Recorder(201, json.dumps([{"id": "1", **rows[0]}]).encode())

    result = SupabaseRest("https://x.supabase.co/", NEW_KEY, recorder).upsert(
        "companies", rows, "ticker,exchange"
    )

    method, url, headers, body = recorder.calls[0]
    assert method == "POST"
    assert url == "https://x.supabase.co/rest/v1/companies?on_conflict=ticker%2Cexchange"
    assert headers["Prefer"] == "resolution=merge-duplicates,return=representation"
    assert body is not None and json.loads(body) == rows
    assert result[0]["id"] == "1"


def test_select_encodes_the_query() -> None:
    recorder = Recorder()
    SupabaseRest("https://x.supabase.co", NEW_KEY, recorder).select(
        "price_snapshots", {"date": "lt.2026-10-27", "limit": "1"}
    )

    method, url, _, body = recorder.calls[0]
    assert method == "GET"
    assert url == "https://x.supabase.co/rest/v1/price_snapshots?date=lt.2026-10-27&limit=1"
    assert body is None


def test_errors_raise_and_do_not_leak_the_key() -> None:
    recorder = Recorder(401, f"bad key {NEW_KEY}".encode())

    with pytest.raises(RuntimeError) as error:
        SupabaseRest("https://x.supabase.co", NEW_KEY, recorder).upsert("t", [], "id")

    assert "HTTP 401" in str(error.value)
    assert NEW_KEY not in str(error.value)


def test_insert_new_ignores_duplicates_and_returns_only_new_rows() -> None:
    rows = [{"source": "s", "external_id": "1"}, {"source": "s", "external_id": "2"}]
    recorder = Recorder(201, json.dumps([rows[1]]).encode())

    result = SupabaseRest("https://x.supabase.co", NEW_KEY, recorder).insert_new(
        "content_items", rows, "source,external_id"
    )

    method, url, headers, body = recorder.calls[0]
    assert method == "POST"
    assert url == "https://x.supabase.co/rest/v1/content_items?on_conflict=source%2Cexternal_id"
    assert headers["Prefer"] == "resolution=ignore-duplicates,return=representation"
    assert body is not None and json.loads(body) == rows
    assert result == [rows[1]]


def test_insert_new_errors_do_not_leak_the_key() -> None:
    recorder = Recorder(400, f"bad {NEW_KEY}".encode())

    with pytest.raises(RuntimeError) as error:
        SupabaseRest("https://x.supabase.co", NEW_KEY, recorder).insert_new("t", [], "id")

    assert "insert into t failed with HTTP 400" in str(error.value)
    assert NEW_KEY not in str(error.value)


@pytest.mark.parametrize(("status", "body"), [(201, b"[]"), (201, b""), (204, b""), (200, b"[]")])
def test_insert_new_with_nothing_inserted_returns_an_empty_list(status: int, body: bytes) -> None:
    recorder = Recorder(status, body)

    result = SupabaseRest("https://x.supabase.co", NEW_KEY, recorder).insert_new(
        "content_items", [{"source": "s", "external_id": "1"}], "source,external_id"
    )

    assert result == []
