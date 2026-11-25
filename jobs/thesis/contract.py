"""Validator for the Agent 3 output contract (docs/AI_SYSTEM.md, Agent 3; ADR-0003, ADR-0004).

Checks what a schema can check, and nothing else. Whether a hypothesis is falsifiable, whether a
risk restates the bear case and whether a claim is backed by a primary source are reads for the
founder and for the golden set, not checks here.

Pure functions, standard library only, no network and no database. Two optional inputs let the
caller add the checks that need the database: the ids of the stored content items (so a citation
cannot point at an item that does not exist) and the bodies of those items (so a paraphrase
cannot be a near-verbatim copy, ADR-0001 D-15). The validator never raises on bad input: every
problem comes back as an `Issue`, so a caller can show all of them at once.
"""

from __future__ import annotations

import re
from collections.abc import Collection, Mapping
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any
from urllib.parse import urlparse
from uuid import UUID

TOP_LEVEL_KEYS = (
    "title",
    "as_of",
    "hypothesis",
    "why_now",
    "market_missing",
    "bull_case",
    "bear_case",
    "valuation",
    "catalysts",
    "invalidation_conditions",
    "risks",
    "benchmark",
    "suggested_basket",
    "basket_weighting",
    "confidence",
    "citations",
    "caveat",
)
TEXT_KEYS = (
    "title",
    "hypothesis",
    "why_now",
    "market_missing",
    "bull_case",
    "bear_case",
    "valuation",
)
# Fields whose text may carry [n] markers. `title` and `caveat` do not.
MARKER_TEXT_KEYS = (
    "hypothesis",
    "why_now",
    "market_missing",
    "bull_case",
    "bear_case",
    "valuation",
)
BENCHMARK_KEYS = ("ticker", "sector_ticker", "outperformance_pct_points", "reason")
BASKET_KEYS = ("ticker", "weight", "rationale")
CITATION_KEYS = (
    "n",
    "content_item_id",
    "source_url",
    "publisher",
    "headline",
    "published_at",
    "retrieved_at",
    "paraphrase",
    "source_type",
    "unverified",
)
WEIGHTINGS = ("equal", "conviction")
CONFIDENCES = ("low", "medium", "high")
SOURCE_TYPES = ("primary", "secondary")

WEIGHT_TOLERANCE = 1e-6
# A paraphrase that shares a run of this many consecutive words with the stored body is read as a
# copy. A starting value, to be tuned against the golden set (docs/AI_SYSTEM.md).
VERBATIM_RUN_WORDS = 8
DEFAULT_HOLDING_PERIOD_DAYS = 90

_MARKER = re.compile(r"\[(\d+)\]")
_WORD = re.compile(r"[a-z0-9$%][a-z0-9$%.,'’-]*")
# A sentence ends at ., ! or ? followed by space and a capital letter, a digit or an opening
# bracket or quote. Decimals ("5.24%") have no space after the point, and the abbreviations
# below are skipped.
_SENTENCE_END = re.compile(r"[.!?][\"')\]]*\s+(?=[A-Z0-9\"'(\[])")
_ABBREVIATIONS = (
    "u.s.",
    "u.k.",
    "e.g.",
    "i.e.",
    "vs.",
    "inc.",
    "corp.",
    "co.",
    "ltd.",
    "no.",
    "st.",
)


@dataclass(frozen=True)
class Issue:
    """One problem, with the path of the field it was found in (for example `citations[3].n`)."""

    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def validate_thesis(
    data: object,
    *,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
    known_content_item_ids: Collection[str] | None = None,
    source_bodies: Mapping[str, str] | None = None,
) -> list[Issue]:
    """Return every contract violation found in `data`, an empty list when there is none.

    `holding_period_days` is the fixed system parameter (docs/DATA_MODEL.md), used to place the
    dated catalyst. `known_content_item_ids`, when given, must hold every `content_item_id` the
    citations use. `source_bodies` maps a content item id to its stored body, for the
    near-verbatim check.
    """
    issues: list[Issue] = []
    if not isinstance(data, dict):
        return [Issue("$", "the thesis must be a JSON object")]
    thesis: dict[str, Any] = data

    for key in sorted(set(thesis) - set(TOP_LEVEL_KEYS)):
        issues.append(Issue(key, "not a field of the contract"))
    for key in TOP_LEVEL_KEYS:
        if key not in thesis:
            issues.append(Issue(key, "missing"))

    for key in TEXT_KEYS:
        if key in thesis:
            _check_text(issues, key, thesis[key])
    if isinstance(thesis.get("hypothesis"), str):
        _check_one_sentence(issues, thesis["hypothesis"])

    as_of = (
        _check_date(issues, "as_of", thesis.get("as_of"), required=True)
        if "as_of" in thesis
        else None
    )

    if "catalysts" in thesis:
        _check_catalysts(issues, thesis["catalysts"], as_of, holding_period_days)
    if "invalidation_conditions" in thesis:
        _check_invalidations(issues, thesis["invalidation_conditions"])
    if "risks" in thesis:
        _check_risks(issues, thesis["risks"])
    if "benchmark" in thesis:
        _check_benchmark(issues, thesis["benchmark"])
    if "suggested_basket" in thesis:
        _check_basket(issues, thesis["suggested_basket"], thesis.get("basket_weighting"))
    if "basket_weighting" in thesis and thesis["basket_weighting"] not in WEIGHTINGS:
        issues.append(Issue("basket_weighting", f"must be one of {', '.join(WEIGHTINGS)}"))
    if "confidence" in thesis and thesis["confidence"] not in CONFIDENCES:
        issues.append(Issue("confidence", f"must be one of {', '.join(CONFIDENCES)}"))
    if "caveat" in thesis:
        _check_text(issues, "caveat", thesis["caveat"])

    numbers: set[int] = set()
    if "citations" in thesis:
        numbers = _check_citations(
            issues, thesis["citations"], known_content_item_ids, source_bodies
        )
    _check_markers(issues, thesis, numbers)
    return issues


def _check_text(issues: list[Issue], path: str, value: object) -> bool:
    if not isinstance(value, str):
        issues.append(Issue(path, "must be a string"))
        return False
    if not value.strip():
        issues.append(Issue(path, "must not be empty"))
        return False
    return True


def _check_one_sentence(issues: list[Issue], text: str) -> None:
    """The hypothesis is one sentence (ADR-0003 D-26)."""
    body = text.strip()
    if not body:
        return
    if "\n" in body:
        issues.append(Issue("hypothesis", "must be one sentence on one line"))
        return
    if body[-1] not in ".!?":
        issues.append(Issue("hypothesis", "must end with a full stop"))
    for match in _SENTENCE_END.finditer(body):
        before = body[: match.start() + 1].split()[-1].lower()
        if before in _ABBREVIATIONS or re.fullmatch(r"(?:[a-z]\.){2,}", before):
            continue
        issues.append(Issue("hypothesis", "must be one sentence, found a second one"))
        return


def _parse_date(value: str) -> date | None:
    """An ISO 8601 date or datetime; the date part is returned."""
    try:
        return date.fromisoformat(value)
    except ValueError:
        pass
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


def _check_date(issues: list[Issue], path: str, value: object, *, required: bool) -> date | None:
    if value is None and not required:
        return None
    if not isinstance(value, str):
        issues.append(Issue(path, "must be an ISO 8601 date or timestamp string"))
        return None
    parsed = _parse_date(value)
    if parsed is None:
        issues.append(Issue(path, f"not an ISO 8601 date or timestamp: {value!r}"))
    return parsed


def _check_catalysts(
    issues: list[Issue], value: object, as_of: date | None, holding_period_days: int
) -> None:
    """At least one catalyst, and one with a date inside the holding window (D-29)."""
    if not isinstance(value, list) or not value:
        issues.append(Issue("catalysts", "must be a list with at least one catalyst"))
        return
    inside_window = False
    for i, item in enumerate(value):
        path = f"catalysts[{i}]"
        if not isinstance(item, dict):
            issues.append(Issue(path, "must be an object with date and event"))
            continue
        _check_keys(issues, path, item, ("date", "event"))
        _check_text(issues, f"{path}.event", item.get("event"))
        when = item.get("date")
        if when == "undated":
            continue
        if not isinstance(when, str) or len(when) != 10:
            issues.append(Issue(f"{path}.date", "must be YYYY-MM-DD or 'undated'"))
            continue
        parsed = _parse_date(when)
        if parsed is None:
            issues.append(Issue(f"{path}.date", f"not a valid date: {when!r}"))
        elif as_of is not None and as_of <= parsed <= as_of + timedelta(days=holding_period_days):
            inside_window = True
    if as_of is not None and not inside_window:
        issues.append(
            Issue(
                "catalysts",
                f"at least one catalyst must be dated within {holding_period_days} days of as_of",
            )
        )


def _check_invalidations(issues: list[Issue], value: object) -> None:
    """At least one observable condition with a threshold (D-30)."""
    if not isinstance(value, list) or not value:
        issues.append(Issue("invalidation_conditions", "must be a list with at least one item"))
        return
    for i, item in enumerate(value):
        path = f"invalidation_conditions[{i}]"
        if not isinstance(item, dict):
            issues.append(Issue(path, "must be an object with condition and threshold"))
            continue
        _check_keys(issues, path, item, ("condition", "threshold"))
        _check_text(issues, f"{path}.condition", item.get("condition"))
        _check_text(issues, f"{path}.threshold", item.get("threshold"))


def _check_risks(issues: list[Issue], value: object) -> None:
    if not isinstance(value, list) or not value:
        issues.append(Issue("risks", "must be a list with at least one risk"))
        return
    for i, item in enumerate(value):
        _check_text(issues, f"risks[{i}]", item)


def _check_benchmark(issues: list[Issue], value: object) -> None:
    """A named benchmark, a threshold in points stated in advance and a reason (D-27)."""
    if not isinstance(value, dict):
        issues.append(Issue("benchmark", "must be an object"))
        return
    _check_keys(issues, "benchmark", value, BENCHMARK_KEYS)
    _check_ticker(issues, "benchmark.ticker", value.get("ticker"))
    sector = value.get("sector_ticker")
    if sector is not None:
        _check_ticker(issues, "benchmark.sector_ticker", sector)
    points = value.get("outperformance_pct_points")
    if isinstance(points, bool) or not isinstance(points, int | float) or points <= 0:
        issues.append(
            Issue("benchmark.outperformance_pct_points", "must be a number greater than zero")
        )
    _check_text(issues, "benchmark.reason", value.get("reason"))


def _check_ticker(issues: list[Issue], path: str, value: object) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Z][A-Z0-9.\-]{0,9}", value):
        issues.append(Issue(path, f"must be an upper-case ticker symbol, got {value!r}"))


def _check_basket(issues: list[Issue], value: object, weighting: object) -> None:
    """Weights sum to 1; `equal` means equal weights (D-32)."""
    if not isinstance(value, list) or not value:
        issues.append(Issue("suggested_basket", "must be a list with at least one holding"))
        return
    weights: list[float] = []
    seen: set[str] = set()
    for i, item in enumerate(value):
        path = f"suggested_basket[{i}]"
        if not isinstance(item, dict):
            issues.append(Issue(path, "must be an object with ticker, weight and rationale"))
            continue
        _check_keys(issues, path, item, BASKET_KEYS)
        ticker = item.get("ticker")
        _check_ticker(issues, f"{path}.ticker", ticker)
        if isinstance(ticker, str):
            if ticker in seen:
                issues.append(Issue(f"{path}.ticker", f"{ticker} appears twice"))
            seen.add(ticker)
        weight = item.get("weight")
        if isinstance(weight, bool) or not isinstance(weight, int | float) or not 0 < weight <= 1:
            issues.append(Issue(f"{path}.weight", "must be a number above 0 and at most 1"))
        else:
            weights.append(float(weight))
        _check_text(issues, f"{path}.rationale", item.get("rationale"))
    if len(weights) == len(value) and abs(sum(weights) - 1) > WEIGHT_TOLERANCE:
        issues.append(Issue("suggested_basket", f"weights sum to {sum(weights):.6g}, not 1"))
    if (
        weighting == "equal"
        and len(weights) == len(value)
        and max(weights) - min(weights) > WEIGHT_TOLERANCE
    ):
        issues.append(Issue("basket_weighting", "is 'equal' but the weights differ"))


def _check_keys(
    issues: list[Issue], path: str, item: Mapping[str, Any], expected: tuple[str, ...]
) -> None:
    for key in sorted(set(item) - set(expected)):
        issues.append(Issue(f"{path}.{key}", "not a field of the contract"))
    for key in expected:
        if key not in item:
            issues.append(Issue(f"{path}.{key}", "missing"))


def _check_citations(
    issues: list[Issue],
    value: object,
    known_ids: Collection[str] | None,
    bodies: Mapping[str, str] | None,
) -> set[int]:
    """Citation fields, numbering, provenance and paraphrase (D-33, D-35, ADR-0001 D-15)."""
    if not isinstance(value, list) or not value:
        issues.append(Issue("citations", "must be a list with at least one citation"))
        return set()
    numbers: list[int] = []
    for i, item in enumerate(value):
        path = f"citations[{i}]"
        if not isinstance(item, dict):
            issues.append(Issue(path, "must be an object"))
            continue
        _check_keys(issues, path, item, CITATION_KEYS)
        n = item.get("n")
        if isinstance(n, bool) or not isinstance(n, int) or n < 1:
            issues.append(Issue(f"{path}.n", "must be an integer from 1"))
        else:
            numbers.append(n)
        for key in ("source_url", "publisher", "headline", "paraphrase"):
            _check_text(issues, f"{path}.{key}", item.get(key))
        _check_url(issues, f"{path}.source_url", item.get("source_url"))
        _check_date(issues, f"{path}.published_at", item.get("published_at"), required=True)
        _check_date(issues, f"{path}.retrieved_at", item.get("retrieved_at"), required=False)
        if item.get("source_type") not in SOURCE_TYPES:
            issues.append(Issue(f"{path}.source_type", f"must be one of {', '.join(SOURCE_TYPES)}"))
        if not isinstance(item.get("unverified"), bool):
            issues.append(Issue(f"{path}.unverified", "must be true or false"))
        _check_provenance(issues, path, item, known_ids, bodies)
    if sorted(numbers) != list(range(1, len(numbers) + 1)) and len(numbers) == len(value):
        issues.append(Issue("citations", "n must run 1, 2, 3, ... once each"))
    return set(numbers)


def _check_url(issues: list[Issue], path: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        return
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        issues.append(Issue(path, f"must be an http(s) URL, got {value!r}"))


def _check_provenance(
    issues: list[Issue],
    path: str,
    item: Mapping[str, Any],
    known_ids: Collection[str] | None,
    bodies: Mapping[str, str] | None,
) -> None:
    """A stored item is named by id; a source the session fetched itself has no id (D-35)."""
    item_id = item.get("content_item_id")
    if item_id is None:
        if item.get("retrieved_at") is None:
            issues.append(
                Issue(
                    f"{path}.retrieved_at",
                    "is required when content_item_id is null: the session fetched the source",
                )
            )
        return
    if not isinstance(item_id, str):
        issues.append(Issue(f"{path}.content_item_id", "must be a uuid string or null"))
        return
    try:
        UUID(item_id)
    except ValueError:
        issues.append(Issue(f"{path}.content_item_id", f"not a uuid: {item_id!r}"))
        return
    if known_ids is not None and item_id not in known_ids:
        issues.append(Issue(f"{path}.content_item_id", "is not a stored content item"))
    body = bodies.get(item_id) if bodies is not None else None
    paraphrase = item.get("paraphrase")
    if body and isinstance(paraphrase, str) and _shares_run(paraphrase, body):
        issues.append(
            Issue(
                f"{path}.paraphrase",
                f"shares a run of {VERBATIM_RUN_WORDS} or more words with the stored body: "
                "restate it, do not copy it",
            )
        )


def _words(text: str) -> list[str]:
    return [w.strip(".,'’-") for w in _WORD.findall(text.lower())]


def _shares_run(paraphrase: str, body: str) -> bool:
    mine = _words(paraphrase)
    if len(mine) < VERBATIM_RUN_WORDS:
        return False
    theirs = _words(body)
    runs = {
        tuple(theirs[i : i + VERBATIM_RUN_WORDS])
        for i in range(len(theirs) - VERBATIM_RUN_WORDS + 1)
    }
    return any(
        tuple(mine[i : i + VERBATIM_RUN_WORDS]) in runs
        for i in range(len(mine) - VERBATIM_RUN_WORDS + 1)
    )


def _marker_texts(thesis: Mapping[str, Any]) -> list[tuple[str, str]]:
    """Every (path, text) that may carry [n] markers, skipping what is malformed."""
    found: list[tuple[str, str]] = []
    for key in MARKER_TEXT_KEYS:
        if isinstance(thesis.get(key), str):
            found.append((key, thesis[key]))

    def add(path: str, text: object) -> None:
        if isinstance(text, str):
            found.append((path, text))

    for i, item in enumerate(_as_list(thesis.get("catalysts"))):
        if isinstance(item, dict):
            add(f"catalysts[{i}].event", item.get("event"))
    for i, item in enumerate(_as_list(thesis.get("invalidation_conditions"))):
        if isinstance(item, dict):
            add(f"invalidation_conditions[{i}].condition", item.get("condition"))
            add(f"invalidation_conditions[{i}].threshold", item.get("threshold"))
    for i, risk in enumerate(_as_list(thesis.get("risks"))):
        add(f"risks[{i}]", risk)
    benchmark = thesis.get("benchmark")
    if isinstance(benchmark, dict):
        add("benchmark.reason", benchmark.get("reason"))
    for i, item in enumerate(_as_list(thesis.get("suggested_basket"))):
        if isinstance(item, dict):
            add(f"suggested_basket[{i}].rationale", item.get("rationale"))
    return found


def _as_list(value: object) -> list[Any]:
    return value if isinstance(value, list) else []


def _check_markers(issues: list[Issue], thesis: Mapping[str, Any], numbers: set[int]) -> None:
    """Every [n] resolves to a citation and every citation is used (D-33)."""
    if not isinstance(thesis.get("citations"), list):
        return
    used: set[int] = set()
    for path, text in _marker_texts(thesis):
        for match in _MARKER.finditer(text):
            n = int(match.group(1))
            used.add(n)
            if n not in numbers:
                issues.append(Issue(path, f"marker [{n}] has no citation"))
    for n in sorted(numbers - used):
        issues.append(Issue("citations", f"citation {n} is never used in the text"))
