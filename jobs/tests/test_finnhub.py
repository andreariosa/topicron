import json

import pytest

from common.finnhub import Quote, fetch_quote, parse_quote

GOOD = {"c": 40.5, "o": 40.0, "h": 41.0, "l": 39.5, "pc": 39.8, "t": 1_793_000_000}


def test_parse_quote_reads_every_field() -> None:
    assert parse_quote("VZ", GOOD) == Quote("VZ", 40.5, 40.0, 41.0, 39.5, 39.8, 1_793_000_000)


def test_parse_quote_rejects_a_non_object() -> None:
    with pytest.raises(ValueError, match="unexpected"):
        parse_quote("VZ", [1, 2, 3])


def test_parse_quote_names_the_missing_fields() -> None:
    with pytest.raises(ValueError, match="no h, l"):
        parse_quote("VZ", {"c": 1, "o": 1, "pc": 1, "t": 1})


def test_parse_quote_treats_the_unknown_symbol_answer_as_an_error() -> None:
    zeros = {"c": 0, "d": None, "dp": None, "h": 0, "l": 0, "o": 0, "pc": 0, "t": 0}
    with pytest.raises(ValueError, match="no price"):
        parse_quote("NOPE", zeros)


def test_parse_quote_rejects_text_and_null_numbers() -> None:
    with pytest.raises(ValueError, match="non-numeric"):
        parse_quote("VZ", {**GOOD, "c": "abc"})
    with pytest.raises(ValueError, match="non-numeric"):
        parse_quote("VZ", {**GOOD, "pc": None})


def test_parse_quote_rejects_nan_and_infinity() -> None:
    with pytest.raises(ValueError, match="non-finite"):
        parse_quote("VZ", {**GOOD, "h": float("nan")})
    with pytest.raises(ValueError, match="non-finite"):
        parse_quote("VZ", {**GOOD, "l": float("inf")})


def test_fetch_quote_sends_the_key_in_a_header_and_not_in_the_url() -> None:
    seen: dict[str, object] = {}

    def http_get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
        seen["url"] = url
        seen["headers"] = headers
        return 200, json.dumps(GOOD).encode()

    quote = fetch_quote("VZ", "secret-key", http_get)

    assert quote.ticker == "VZ"
    assert seen["headers"] == {"X-Finnhub-Token": "secret-key"}
    assert str(seen["url"]).endswith("/quote?symbol=VZ")
    assert "secret-key" not in str(seen["url"])


def test_fetch_quote_error_does_not_leak_the_key() -> None:
    def http_get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
        return 401, b'{"error":"Invalid API key secret-key"}'

    with pytest.raises(RuntimeError) as error:
        fetch_quote("VZ", "secret-key", http_get)

    assert "HTTP 401" in str(error.value)
    assert "secret-key" not in str(error.value)


def test_fetch_quote_rejects_an_answer_that_is_not_json() -> None:
    def http_get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
        return 200, b"<html>maintenance</html>"

    with pytest.raises(ValueError, match="not JSON"):
        fetch_quote("VZ", "k", http_get)
