"""Finnhub /quote client.

Why only /quote: Finnhub's free plan does not include daily candles
(/stock/candle), so the daily bar is built from the quote's open, high, low,
current price and previous close. The quote carries no volume.
"""

from __future__ import annotations

import json
import math
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

QUOTE_URL = "https://finnhub.io/api/v1/quote"

# (url, headers) -> (status, body). Replaced by a fake in tests.
HttpGet = Callable[[str, dict[str, str]], tuple[int, bytes]]

_FIELDS = ("c", "o", "h", "l", "pc", "t")


@dataclass(frozen=True)
class Quote:
    ticker: str
    current: float
    open: float
    high: float
    low: float
    previous_close: float
    timestamp: int  # unix seconds of the last trade


def _urllib_get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return int(response.status), bytes(response.read())
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def parse_quote(ticker: str, payload: object) -> Quote:
    """Turn a /quote payload into a Quote, or raise ValueError.

    Finnhub answers an unknown symbol with HTTP 200 and all zeros, so a zero
    price is an error here and not a price.
    """
    if not isinstance(payload, dict):
        raise ValueError(f"{ticker}: unexpected quote payload")
    missing = [name for name in _FIELDS if name not in payload]
    if missing:
        raise ValueError(f"{ticker}: quote has no {', '.join(missing)}")
    try:
        current = float(payload["c"])
        open_ = float(payload["o"])
        high = float(payload["h"])
        low = float(payload["l"])
        previous_close = float(payload["pc"])
        timestamp = int(payload["t"])
    except (TypeError, ValueError) as error:
        raise ValueError(f"{ticker}: quote has a non-numeric field") from error
    numbers = (current, open_, high, low, previous_close)
    if not all(math.isfinite(value) for value in numbers):
        raise ValueError(f"{ticker}: quote has a non-finite number")
    if current <= 0 or timestamp <= 0:
        raise ValueError(f"{ticker}: Finnhub returned no price (unknown symbol or no data)")
    return Quote(ticker, current, open_, high, low, previous_close, timestamp)


def fetch_quote(ticker: str, api_key: str, http_get: HttpGet = _urllib_get) -> Quote:
    """Fetch and parse one quote. The key travels in a header, never in the URL."""
    url = f"{QUOTE_URL}?{urllib.parse.urlencode({'symbol': ticker})}"
    status, body = http_get(url, {"X-Finnhub-Token": api_key})
    if status != 200:
        detail = body.decode("utf-8", errors="replace")[:200].replace(api_key, "***")
        raise RuntimeError(f"{ticker}: Finnhub answered HTTP {status}: {detail}")
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as error:
        raise ValueError(f"{ticker}: Finnhub answer is not JSON") from error
    return parse_quote(ticker, payload)
