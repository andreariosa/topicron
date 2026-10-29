import pytest

from extract.matching import (
    NAME_IN_BODY,
    NAME_IN_TITLE,
    SYMBOL_IN_TEXT,
    TAG,
    Result,
    Target,
    exchange_key,
    extract,
)

VZ = Target("c-vz", "VZ", "NYSE", ("Verizon",))
T = Target("c-t", "T", "NYSE", ("AT&T",))
TMUS = Target("c-tmus", "TMUS", "NASDAQ", ("T-Mobile",))
SPY = Target("c-spy", "SPY", "NYSE Arca", ("SPDR S&P 500",))
# A real ticker that is also an English word: the collision the rules are built around.
ALL = Target("c-all", "ALL", "NYSE", ("Allstate",))
TARGETS = [VZ, T, TMUS, SPY, ALL]


def run(title: str = "", body: str = "", *tags: str) -> Result:
    return extract(title, body, list(tags), TARGETS)


def seen(result: Result) -> dict[str, float]:
    return {m.ticker: m.confidence for m in result.mentions}


def test_a_publisher_tag_is_the_strongest_match() -> None:
    assert seen(run("Quarterly update", "", "NYSE:VZ")) == {"VZ": TAG}


def test_several_tickers_in_one_category_are_all_read() -> None:
    assert seen(run("x", "", "NASDAQ:TMUS NYSE:T")) == {"TMUS": TAG, "T": TAG}


def test_the_exchange_is_compared_without_spaces_or_case() -> None:
    assert exchange_key("NYSE Arca") == exchange_key("nysearca") == "NYSEARCA"
    assert seen(run("x", "", "NYSEARCA:SPY")) == {"SPY": TAG}


def test_the_same_symbol_on_another_exchange_is_another_company() -> None:
    result = run("x", "", "TSE:T")

    assert result.mentions == [] and result.flags == []
    assert result.unknown_tags == ["TSE:T"]


def test_the_key_is_symbol_and_exchange_together() -> None:
    toronto = Target("c-t-tse", "T", "TSE")
    result = extract("x", "", ["TSE:T"], [T, toronto])

    assert [m.company_id for m in result.mentions] == ["c-t-tse"]


def test_a_tag_without_an_exchange_is_reported_not_trusted() -> None:
    for tag in (":T", "T"):
        result = run("x", "", tag)
        assert result.mentions == []
        assert [(f.ticker, f.reason) for f in result.flags] == [("T", "tag without an exchange")]


def test_a_tag_without_an_exchange_for_an_unknown_symbol_is_ignored() -> None:
    result = run("x", "", ":QBKV", "QBKV", "XX")

    assert result.mentions == [] and result.flags == [] and result.unknown_tags == []


def test_tickers_that_match_no_company_are_counted_as_they_were_written() -> None:
    assert run("x", "", "NASDAQ:NVDA NYSE:LMT").unknown_tags == ["NASDAQ:NVDA", "NYSE:LMT"]


def test_a_section_name_is_not_a_ticker() -> None:
    result = run("x", "", "Monetary Policy", "Enforcement Actions")

    assert result.mentions == [] and result.flags == [] and result.unknown_tags == []


@pytest.mark.parametrize(
    "text", ["shares of NYSE: VZ rose", "(NYSE:VZ)", "nyse : VZ.", "Shares (Nyse: VZ), up"]
)
def test_a_symbol_with_its_exchange_in_the_text(text: str) -> None:
    assert seen(run(text)) == {"VZ": SYMBOL_IN_TEXT}


def test_the_wrong_exchange_in_the_text_is_no_match() -> None:
    assert run("NASDAQ: VZ climbs").mentions == []


def test_nyse_arca_is_read_with_or_without_a_space() -> None:
    assert seen(run("NYSE Arca: SPY and NYSEARCA:SPY")) == {"SPY": SYMBOL_IN_TEXT}


def test_cashtags() -> None:
    assert seen(run("watching $TMUS and $T today")) == {"TMUS": SYMBOL_IN_TEXT, "T": SYMBOL_IN_TEXT}


def test_a_dollar_amount_is_not_a_cashtag() -> None:
    assert run("a $5T market, $TB of data").mentions == []


def test_a_symbol_in_parentheses() -> None:
    assert seen(run("Earnings preview (TMUS)")) == {"TMUS": SYMBOL_IN_TEXT}


def test_a_single_letter_in_parentheses_is_not_enough() -> None:
    result = run("see note (T) below")

    assert result.mentions == [] and result.flags == []


def test_a_name_in_the_title_beats_a_name_in_the_description() -> None:
    assert seen(run("Verizon raises its outlook", "x")) == {"VZ": NAME_IN_TITLE}
    assert seen(run("Outlook raised", "Verizon said on Thursday")) == {"VZ": NAME_IN_BODY}
    assert seen(run("Verizon raises", "Verizon said")) == {"VZ": NAME_IN_TITLE}


def test_names_ignore_case_and_accept_a_possessive() -> None:
    assert seen(run("T-MOBILE beats, AT&T's guidance holds")) == {
        "TMUS": NAME_IN_TITLE,
        "T": NAME_IN_TITLE,
    }


def test_a_name_inside_a_longer_word_is_not_a_match() -> None:
    assert run("Verizonia opens a plant").mentions == []


def test_the_index_is_not_the_fund() -> None:
    assert run("The S&P 500 closed higher").mentions == []
    assert seen(run("flows into the SPDR S&P 500 ETF")) == {"SPY": NAME_IN_TITLE}


def test_the_letters_inside_att_and_tmobile_are_not_a_bare_t() -> None:
    result = run("AT&T and T-Mobile report")

    assert result.flags == []
    assert set(seen(result)) == {"T", "TMUS"}


def test_a_bare_symbol_is_reported_and_not_matched() -> None:
    for text, ticker in (("Plan T rollout", "T"), ("VZ rose 2% on Friday", "VZ")):
        result = run(text)
        assert result.mentions == []
        assert [(f.ticker, f.reason) for f in result.flags] == [(ticker, "bare symbol in the text")]


def test_a_bare_symbol_is_not_reported_when_another_rule_found_the_company() -> None:
    result = run("T-Mobile: TMUS rose")

    assert seen(result) == {"TMUS": NAME_IN_TITLE}
    assert result.flags == []


def test_a_ticker_that_is_also_a_word_never_matches_as_a_word() -> None:
    assert run("all of the above, and are we sure").mentions == []

    shouted = run("ALL OF THE ABOVE")
    assert shouted.mentions == []
    assert [f.ticker for f in shouted.flags] == ["ALL"]

    assert seen(run("Allstate (NYSE: ALL) reports")) == {"ALL": SYMBOL_IN_TEXT}
    assert seen(run("Allstate reports")) == {"ALL": NAME_IN_TITLE}
    assert seen(run("Insurers: NYSE: ALL gains")) == {"ALL": SYMBOL_IN_TEXT}


def test_the_strongest_rule_wins_and_mentions_come_sorted() -> None:
    result = run("Verizon (NYSE: VZ) and AT&T", "T-Mobile", "NYSE:VZ", "NASDAQ:TMUS")

    assert seen(result) == {"VZ": TAG, "T": NAME_IN_TITLE, "TMUS": TAG}
    assert [m.ticker for m in result.mentions] == ["T", "TMUS", "VZ"]


def test_confidence_levels_are_ordered_by_how_much_the_rule_proves() -> None:
    assert TAG > SYMBOL_IN_TEXT > NAME_IN_TITLE > NAME_IN_BODY > 0
