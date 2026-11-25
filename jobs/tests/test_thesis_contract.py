import copy
import json
from pathlib import Path
from typing import Any

import pytest

from thesis.__main__ import main
from thesis.contract import VERBATIM_RUN_WORDS, Issue, validate_thesis

FIXTURE = Path(__file__).parent / "fixtures" / "thesis_13.json"
UUID_A = "11111111-2222-3333-4444-555555555555"


def load() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return data


def paths(issues: list[Issue]) -> list[str]:
    return [i.path for i in issues]


def messages(issues: list[Issue]) -> str:
    return "\n".join(str(i) for i in issues)


# The first fixture: write-up 13, converted by hand from its Markdown into the contract.


def test_thesis_13_meets_the_contract() -> None:
    assert validate_thesis(load()) == []


def test_thesis_13_keeps_what_the_write_up_says() -> None:
    thesis = load()
    assert [h["weight"] for h in thesis["suggested_basket"]] == [0.4, 0.4, 0.2]
    assert thesis["basket_weighting"] == "conviction"
    assert thesis["benchmark"]["sector_ticker"] is None
    assert len(thesis["citations"]) == 20
    assert [c["unverified"] for c in thesis["citations"]].count(True) == 1
    assert thesis["citations"][12]["unverified"] is True  # the $8 billion, WSJ via Forbes


def test_main_reports_ok_for_the_fixture(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(FIXTURE)]) == 0
    assert "ok" in capsys.readouterr().out


def test_main_reports_problems_with_exit_code_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    thesis = load()
    del thesis["caveat"]
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(thesis), encoding="utf-8")
    assert main([str(bad)]) == 1
    assert "caveat: missing" in capsys.readouterr().out


def test_main_rejects_wrong_usage_and_unreadable_files(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([]) == 2
    assert main([str(tmp_path / "missing.json")]) == 2
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    assert main([str(broken)]) == 2
    assert capsys.readouterr().err


# Shape.


def test_not_an_object() -> None:
    assert paths(validate_thesis([1, 2])) == ["$"]
    assert paths(validate_thesis(None)) == ["$"]


@pytest.mark.parametrize(
    "key",
    [
        "title", "as_of", "hypothesis", "why_now", "market_missing", "bull_case", "bear_case",
        "valuation", "catalysts", "invalidation_conditions", "risks", "benchmark",
        "suggested_basket", "basket_weighting", "confidence", "citations", "caveat",
    ],
)  # fmt: skip
def test_every_field_is_required(key: str) -> None:
    thesis = load()
    del thesis[key]
    assert f"{key}: missing" in messages(validate_thesis(thesis))


@pytest.mark.parametrize("extra", ["starting_value", "holding_period_days", "reader_risk_profile"])
def test_fields_outside_the_contract_are_rejected(extra: str) -> None:
    # Fixed system parameters are attached by the application, and nothing about a reader goes in
    # (ADR-0003 D-32; docs/RISKS.md).
    thesis = load()
    thesis[extra] = 1
    assert f"{extra}: not a field of the contract" in messages(validate_thesis(thesis))


@pytest.mark.parametrize("key", ["title", "why_now", "bull_case", "valuation", "caveat"])
def test_text_fields_must_be_non_empty_strings(key: str) -> None:
    for bad in ("", "   ", 7, None):
        thesis = load()
        thesis[key] = bad
        assert key in paths(validate_thesis(thesis))


# Hypothesis (D-26).


def test_hypothesis_must_be_one_sentence() -> None:
    thesis = load()
    thesis["hypothesis"] = "The basket will beat SPY by 5 points. It will do so because of rates."
    assert "found a second one" in messages(validate_thesis(thesis))


def test_hypothesis_on_two_lines_is_rejected() -> None:
    thesis = load()
    thesis["hypothesis"] = "The basket will beat SPY\nby 5 points."
    assert "one line" in messages(validate_thesis(thesis))


def test_hypothesis_must_end_with_a_full_stop() -> None:
    thesis = load()
    thesis["hypothesis"] = "The basket will beat SPY by 5 points"
    assert "full stop" in messages(validate_thesis(thesis))


@pytest.mark.parametrize(
    "text",
    [
        "A basket of U.S. carriers will beat SPY by 5.5 percentage points over 90 days.",
        "AT&T, Verizon Inc. and T-Mobile will beat the S&P 500 (SPY) by 5 points, e.g. on price.",
        'The basket will beat SPY by at least 5 points if "the market" re-rates it.',
    ],
)
def test_abbreviations_and_decimals_do_not_split_a_hypothesis(text: str) -> None:
    thesis = load()
    thesis["hypothesis"] = text
    assert "hypothesis" not in paths(validate_thesis(thesis))


# Dates, catalysts (D-29).


def test_as_of_must_be_a_date() -> None:
    thesis = load()
    thesis["as_of"] = "9 October 2026"
    assert "as_of" in paths(validate_thesis(thesis))


def test_a_catalyst_must_be_dated_inside_the_window() -> None:
    thesis = load()
    thesis["catalysts"] = [{"date": "undated", "event": "FCC action."}]
    assert "dated within 90 days" in messages(validate_thesis(thesis))
    thesis["catalysts"] = [{"date": "2027-03-01", "event": "Too late."}]
    assert "dated within 90 days" in messages(validate_thesis(thesis))
    thesis["catalysts"] = [{"date": "2026-10-01", "event": "Before as_of."}]
    assert "dated within 90 days" in messages(validate_thesis(thesis))


def test_the_window_is_a_parameter() -> None:
    thesis = load()
    assert validate_thesis(thesis, holding_period_days=90) == []
    # The first dated catalyst is 12 days after as_of, so a 10-day window leaves none inside.
    assert "dated within 10 days" in messages(validate_thesis(thesis, holding_period_days=10))


@pytest.mark.parametrize("bad", ["soon", "2026-13-01", "2026-10-1", 20261021, None])
def test_catalyst_date_must_be_a_date_or_undated(bad: object) -> None:
    thesis = load()
    thesis["catalysts"].append({"date": bad, "event": "Something."})
    assert "catalysts[7].date" in paths(validate_thesis(thesis))


def test_catalysts_must_not_be_empty_and_need_an_event() -> None:
    thesis = load()
    thesis["catalysts"] = []
    assert "catalysts" in paths(validate_thesis(thesis))
    thesis = load()
    thesis["catalysts"][0]["event"] = ""
    assert "catalysts[0].event" in paths(validate_thesis(thesis))
    thesis = load()
    thesis["catalysts"][0]["extra"] = 1
    assert "catalysts[0].extra" in paths(validate_thesis(thesis))


# Invalidation conditions (D-30) and risks (D-31).


def test_at_least_one_invalidation_condition_with_a_threshold() -> None:
    thesis = load()
    thesis["invalidation_conditions"] = []
    assert "invalidation_conditions" in paths(validate_thesis(thesis))
    thesis = load()
    thesis["invalidation_conditions"][0]["threshold"] = ""
    assert "invalidation_conditions[0].threshold" in paths(validate_thesis(thesis))
    thesis = load()
    del thesis["invalidation_conditions"][1]["condition"]
    assert "invalidation_conditions[1].condition" in paths(validate_thesis(thesis))


def test_risks_must_be_a_list_of_text() -> None:
    thesis = load()
    thesis["risks"] = []
    assert "risks" in paths(validate_thesis(thesis))
    thesis["risks"] = ["Fine.", 3]
    assert "risks[1]" in paths(validate_thesis(thesis))


# Benchmark (D-27).


def test_benchmark_needs_a_threshold_above_zero_and_a_reason() -> None:
    for bad in (0, -5, "5", True, None):
        thesis = load()
        thesis["benchmark"]["outperformance_pct_points"] = bad
        assert "benchmark.outperformance_pct_points" in paths(validate_thesis(thesis))
    thesis = load()
    thesis["benchmark"]["reason"] = " "
    assert "benchmark.reason" in paths(validate_thesis(thesis))


def test_benchmark_tickers() -> None:
    thesis = load()
    thesis["benchmark"]["ticker"] = "spy"
    assert "benchmark.ticker" in paths(validate_thesis(thesis))
    thesis = load()
    thesis["benchmark"]["sector_ticker"] = "IYZ"
    assert validate_thesis(thesis) == []
    thesis["benchmark"]["sector_ticker"] = ""
    assert "benchmark.sector_ticker" in paths(validate_thesis(thesis))


def test_benchmark_must_be_an_object() -> None:
    thesis = load()
    thesis["benchmark"] = "SPY"
    assert paths(validate_thesis(thesis)) == ["benchmark"]


# Basket (D-32).


def test_weights_must_sum_to_one() -> None:
    thesis = load()
    thesis["suggested_basket"][2]["weight"] = 0.3
    assert "sum to 1.1" in messages(validate_thesis(thesis))
    thesis = load()
    thesis["suggested_basket"].pop()
    assert "sum to 0.8" in messages(validate_thesis(thesis))


def test_three_thirds_sum_to_one() -> None:
    thesis = load()
    thesis["basket_weighting"] = "equal"
    for holding in thesis["suggested_basket"]:
        holding["weight"] = 1 / 3
    assert validate_thesis(thesis) == []


def test_equal_weighting_needs_equal_weights() -> None:
    thesis = load()
    thesis["basket_weighting"] = "equal"
    assert "is 'equal' but the weights differ" in messages(validate_thesis(thesis))


@pytest.mark.parametrize("bad", [0, -0.1, 1.5, "0.4", True, None])
def test_each_weight_is_a_fraction(bad: object) -> None:
    thesis = load()
    thesis["suggested_basket"][0]["weight"] = bad
    assert "suggested_basket[0].weight" in paths(validate_thesis(thesis))


def test_every_holding_needs_a_rationale_and_a_distinct_ticker() -> None:
    thesis = load()
    thesis["suggested_basket"][1]["rationale"] = ""
    assert "suggested_basket[1].rationale" in paths(validate_thesis(thesis))
    thesis = load()
    thesis["suggested_basket"][1]["ticker"] = "VZ"
    assert "VZ appears twice" in messages(validate_thesis(thesis))


def test_a_name_may_be_left_out_under_conviction_weighting() -> None:
    thesis = load()
    thesis["suggested_basket"].pop()
    thesis["suggested_basket"][0]["weight"] = 0.5
    thesis["suggested_basket"][1]["weight"] = 0.5
    # Dropping the T-Mobile rationale also drops the only [1], [13] and [18] markers it carried.
    issues = validate_thesis(thesis)
    assert all("sum" not in i.message for i in issues)


def test_weighting_and_confidence_values() -> None:
    thesis = load()
    thesis["basket_weighting"] = "naive"
    thesis["confidence"] = "very high"
    assert {"basket_weighting", "confidence"} <= set(paths(validate_thesis(thesis)))


# Citations (D-33, D-35).


def test_markers_must_resolve() -> None:
    thesis = load()
    thesis["bull_case"] += " Another fact [21]."
    assert "marker [21] has no citation" in messages(validate_thesis(thesis))


def test_markers_in_every_text_field_count() -> None:
    for where in ("hypothesis", "why_now", "valuation"):
        thesis = load()
        thesis[where] = thesis[where].rstrip(".") + " [99]."
        assert f"{where}: marker [99]" in messages(validate_thesis(thesis))
    thesis = load()
    thesis["risks"][0] += " [99]"
    assert "risks[0]: marker [99]" in messages(validate_thesis(thesis))
    thesis = load()
    thesis["suggested_basket"][0]["rationale"] += " [99]"
    assert "suggested_basket[0].rationale: marker [99]" in messages(validate_thesis(thesis))
    thesis = load()
    thesis["invalidation_conditions"][0]["threshold"] += " [99]"
    assert "invalidation_conditions[0].threshold: marker [99]" in messages(validate_thesis(thesis))
    thesis = load()
    thesis["catalysts"][0]["event"] += " [99]"
    assert "catalysts[0].event: marker [99]" in messages(validate_thesis(thesis))
    thesis = load()
    thesis["benchmark"]["reason"] += " [99]"
    assert "benchmark.reason: marker [99]" in messages(validate_thesis(thesis))


def test_every_citation_must_be_used() -> None:
    thesis = load()
    thesis["citations"].append(copy.deepcopy(thesis["citations"][0]) | {"n": 21})
    assert "citation 21 is never used" in messages(validate_thesis(thesis))


def test_citation_numbers_run_from_one_without_gaps_or_repeats() -> None:
    thesis = load()
    thesis["citations"][4]["n"] = 4
    assert "n must run 1, 2, 3" in messages(validate_thesis(thesis))
    thesis = load()
    thesis["citations"][0]["n"] = 0
    assert "citations[0].n" in paths(validate_thesis(thesis))
    thesis = load()
    thesis["citations"][0]["n"] = "1"
    assert "citations[0].n" in paths(validate_thesis(thesis))


def test_citations_must_not_be_empty() -> None:
    thesis = load()
    thesis["citations"] = []
    assert "citations" in paths(validate_thesis(thesis))


def test_citation_fields() -> None:
    thesis = load()
    c = thesis["citations"][0]
    c["source_url"] = "ftp://example.com/x"
    c["publisher"] = ""
    c["published_at"] = "July 2026"
    c["retrieved_at"] = "yesterday"
    c["source_type"] = "tertiary"
    c["unverified"] = "no"
    c["paraphrase"] = " "
    c["extra"] = 1
    found = set(paths(validate_thesis(thesis)))
    assert {f"citations[0].{k}" for k in (
        "source_url", "publisher", "published_at", "retrieved_at", "source_type",
        "unverified", "paraphrase", "extra",
    )} <= found  # fmt: skip


def test_timestamps_are_accepted_with_a_time() -> None:
    thesis = load()
    thesis["citations"][0]["published_at"] = "2026-07-01T08:30:00Z"
    thesis["citations"][0]["retrieved_at"] = "2026-10-12T07:15:00+02:00"
    assert validate_thesis(thesis) == []


def test_a_source_the_session_fetched_itself_needs_retrieved_at() -> None:
    thesis = load()
    thesis["citations"][0]["retrieved_at"] = None
    assert "citations[0].retrieved_at" in paths(validate_thesis(thesis))


def test_a_stored_item_is_named_by_a_uuid() -> None:
    thesis = load()
    thesis["citations"][10]["content_item_id"] = UUID_A
    thesis["citations"][10]["retrieved_at"] = None
    assert validate_thesis(thesis) == []
    thesis["citations"][10]["content_item_id"] = "not-a-uuid"
    assert "citations[10].content_item_id" in paths(validate_thesis(thesis))
    thesis["citations"][10]["content_item_id"] = 5
    assert "citations[10].content_item_id" in paths(validate_thesis(thesis))


def test_a_stored_item_must_exist_when_the_ids_are_given() -> None:
    thesis = load()
    thesis["citations"][10]["content_item_id"] = UUID_A
    assert validate_thesis(thesis, known_content_item_ids={UUID_A}) == []
    issues = validate_thesis(thesis, known_content_item_ids=set())
    assert "citations[10].content_item_id: is not a stored content item" in messages(issues)


def test_a_paraphrase_that_copies_the_stored_body_is_rejected() -> None:
    body = (
        "SpaceX agreed to buy one hundred percent of Grain Management's nationwide 800 MHz "
        "portfolio, terms undisclosed, subject to FCC approval, the company said on Thursday."
    )
    thesis = load()
    thesis["citations"][10]["content_item_id"] = UUID_A
    thesis["citations"][10]["paraphrase"] = (
        "Per the report, SpaceX agreed to buy one hundred percent of Grain Management's "
        "nationwide 800 MHz portfolio on Thursday."
    )
    issues = validate_thesis(thesis, source_bodies={UUID_A: body})
    assert "citations[10].paraphrase" in paths(issues)
    thesis["citations"][10]["paraphrase"] = (
        "SpaceX will acquire Grain's low-band licences; the price was not stated and the "
        "FCC still has to approve the sale."
    )
    assert validate_thesis(thesis, source_bodies={UUID_A: body}) == []


def test_a_short_shared_phrase_is_not_a_copy() -> None:
    assert VERBATIM_RUN_WORDS > 4
    body = "Verizon raised its 2026 free cash flow guidance and its buyback target in July."
    thesis = load()
    thesis["citations"][10]["content_item_id"] = UUID_A
    thesis["citations"][10]["paraphrase"] = "Verizon raised its 2026 free cash flow outlook."
    assert validate_thesis(thesis, source_bodies={UUID_A: body}) == []


def test_the_check_runs_without_bodies() -> None:
    thesis = load()
    thesis["citations"][10]["content_item_id"] = UUID_A
    assert validate_thesis(thesis) == []


def test_the_validator_does_not_change_its_input() -> None:
    thesis = load()
    before = copy.deepcopy(thesis)
    validate_thesis(thesis)
    assert thesis == before


def test_all_problems_come_back_at_once() -> None:
    thesis = load()
    del thesis["caveat"]
    thesis["confidence"] = "sure"
    thesis["suggested_basket"][0]["weight"] = 0.9
    assert len(validate_thesis(thesis)) >= 3


def test_issue_prints_path_and_message() -> None:
    assert str(Issue("risks[1]", "must be a string")) == "risks[1]: must be a string"
