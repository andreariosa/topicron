"""Minimal Supabase REST (PostgREST) client for the scheduled jobs.

Standard library only (CURSOR_RULES.md, section 3). The jobs use Supabase's
secret key, which bypasses row-level security, so it must exist only as a
GitHub Actions secret and never in the repository, the logs or the frontend.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from typing import Any

# (method, url, headers, body) -> (status, body). Replaced by a fake in tests.
HttpRequest = Callable[[str, str, dict[str, str], bytes | None], tuple[int, bytes]]


def _urllib_request(
    method: str, url: str, headers: dict[str, str], body: bytes | None
) -> tuple[int, bytes]:
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return int(response.status), bytes(response.read())
    except urllib.error.HTTPError as error:
        return error.code, error.read()


class SupabaseRest:
    def __init__(self, base_url: str, secret_key: str, http: HttpRequest = _urllib_request) -> None:
        if not base_url.startswith("https://"):
            raise ValueError("SUPABASE_URL must start with https://")
        self._base = base_url.rstrip("/")
        self._key = secret_key
        self._http = http

    def _headers(self) -> dict[str, str]:
        # New secret keys (sb_secret_...) go in `apikey` only; Supabase says a
        # non-JWT key sent as a bearer token is wrong. The legacy service_role
        # key is a JWT and is still sent both ways.
        headers = {"apikey": self._key, "Content-Type": "application/json"}
        if self._key.startswith("eyJ"):
            headers["Authorization"] = f"Bearer {self._key}"
        return headers

    def _check(self, status: int, body: bytes, action: str) -> bytes:
        if status not in (200, 201):
            detail = body.decode("utf-8", errors="replace")[:300].replace(self._key, "***")
            raise RuntimeError(f"Supabase {action} failed with HTTP {status}: {detail}")
        return body

    def upsert(
        self, table: str, rows: list[dict[str, Any]], on_conflict: str
    ) -> list[dict[str, Any]]:
        """Insert rows, or update them when the conflict columns already exist."""
        query = urllib.parse.urlencode({"on_conflict": on_conflict})
        headers = {
            **self._headers(),
            "Prefer": "resolution=merge-duplicates,return=representation",
        }
        status, body = self._http(
            "POST", f"{self._base}/rest/v1/{table}?{query}", headers, json.dumps(rows).encode()
        )
        result: list[dict[str, Any]] = json.loads(self._check(status, body, f"upsert into {table}"))
        return result

    def select(self, table: str, query: dict[str, str]) -> list[dict[str, Any]]:
        url = f"{self._base}/rest/v1/{table}?{urllib.parse.urlencode(query)}"
        status, body = self._http("GET", url, self._headers(), None)
        result: list[dict[str, Any]] = json.loads(self._check(status, body, f"select from {table}"))
        return result
