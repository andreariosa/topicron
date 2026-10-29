"""Rule-based company matching for one content item (docs/AI_SYSTEM.md, Agent 1).

Pure functions, no I/O. The failure mode this is built around is the collision of a ticker
with a common word ("ALL", "ARE", "IT", "ON", "SO" are real tickers, docs/RISKS.md): a bare
symbol in running text is never accepted. It is logged for the founder instead, because the
model that would resolve it is deferred (ADR-0002, D-20).

Each rule has a fixed confidence, so the number tells which rule fired. It is a rule level,
not a probability, and nothing public shows it.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, field

TAG = 1.0  # the publisher tagged the item with EXCHANGE:SYMBOL
SYMBOL_IN_TEXT = 0.9  # "(NYSE: VZ)", "$VZ" or "(TMUS)" in the title or description
NAME_IN_TITLE = 0.8  # "Verizon" in the title
NAME_IN_BODY = 0.6  # "Verizon" in the description only


@dataclass(frozen=True)
class Target:
    """A company the matcher looks for: a row of `companies` plus its names."""

    company_id: str
    ticker: str
    exchange: str  # as stored, e.g. "NYSE Arca"
    names: tuple[str, ...] = ()


@dataclass(frozen=True)
class Mention:
    company_id: str
    ticker: str
    confidence: float


@dataclass(frozen=True)
class Flag:
    """A case the rules cannot settle. It is reported, never resolved automatically."""

    ticker: str
    reason: str


@dataclass
class Result:
    mentions: list[Mention] = field(default_factory=list)
    flags: list[Flag] = field(default_factory=list)
    # Tags of the form EXCHANGE:SYMBOL that match no company in the table, as written.
    unknown_tags: list[str] = field(default_factory=list)


def exchange_key(name: str) -> str:
    """ "NYSE Arca" (companies) and "NYSEARCA" (MarketBeat tags) are the same exchange."""
    return re.sub(r"[^A-Z0-9]", "", name.upper())


# A tag token: EXCHANGE:SYMBOL, or just :SYMBOL when the publisher left the exchange out.
_TAG = re.compile(r"^(?P<exchange>[A-Z]*):(?P<symbol>[A-Z][A-Z0-9.\-]*)$")
_BARE_TAG = re.compile(r"^[A-Z][A-Z0-9.\-]*$")

# "(NYSE: VZ)", "NASDAQ:TMUS", "NYSE Arca: SPY". The symbol must be upper case.
_QUALIFIED = re.compile(
    r"(?<!\w)(?i:(?P<exchange>NYSE ?ARCA|NYSE ?AMERICAN|NYSE|NASDAQ|AMEX|BATS|CBOE|OTCMKTS))"
    r"\s*:\s*(?P<symbol>[A-Z][A-Z0-9]{0,5}(?:\.[A-Z])?)(?!\w)"
)
_CASHTAG = re.compile(r"(?<![\w$])\$(?P<symbol>[A-Z]{1,5})(?!\w)")
# Two letters or more: "(T)" is too often a footnote or a label.
_PARENTHESISED = re.compile(r"\((?P<symbol>[A-Z]{2,5})\)")


def _bare(symbol: str) -> re.Pattern[str]:
    # Not a piece of "AT&T", "T-Mobile", "NYSE:T", "$T" or "(T)": other rules handle those forms.
    return re.compile(rf"(?<![\w&\-./$:(]){re.escape(symbol)}(?![\w&\-./:)])")


def _name(name: str) -> re.Pattern[str]:
    return re.compile(rf"(?<!\w){re.escape(name)}(?!\w)", re.IGNORECASE)


def extract(title: str, body: str, categories: Sequence[str], targets: Sequence[Target]) -> Result:
    result = Result()
    best: dict[str, float] = {}
    by_symbol: dict[str, list[Target]] = {}
    for target in targets:
        by_symbol.setdefault(target.ticker, []).append(target)

    def hit(target: Target, confidence: float) -> None:
        best[target.company_id] = max(best.get(target.company_id, 0.0), confidence)

    def find(symbol: str, exchange: str | None) -> Target | None:
        for target in by_symbol.get(symbol, []):
            if exchange is None or exchange_key(target.exchange) == exchange:
                return target
        return None

    # 1. The publisher's own tags. Several tickers can share one category, split by spaces.
    for category in categories:
        for token in category.split():
            tag = _TAG.match(token)
            if tag and tag["exchange"]:
                found = find(tag["symbol"], exchange_key(tag["exchange"]))
                if found:
                    hit(found, TAG)
                else:
                    # Also what a different listing looks like: TSE:T is TELUS, not AT&T.
                    result.unknown_tags.append(token)
            else:
                symbol = tag["symbol"] if tag else token
                if _BARE_TAG.match(symbol) and symbol in by_symbol:
                    result.flags.append(Flag(symbol, "tag without an exchange"))

    # 2. Symbols written in the text with an exchange, a dollar sign or parentheses.
    for text in (title, body):
        for qualified in _QUALIFIED.finditer(text):
            found = find(qualified["symbol"], exchange_key(qualified["exchange"]))
            if found:
                hit(found, SYMBOL_IN_TEXT)
        for cashtag in _CASHTAG.finditer(text):
            found = find(cashtag["symbol"], None)
            if found:
                hit(found, SYMBOL_IN_TEXT)
        for parenthesised in _PARENTHESISED.finditer(text):
            found = find(parenthesised["symbol"], None)
            if found:
                hit(found, SYMBOL_IN_TEXT)

    # 3. Company names.
    for target in targets:
        for name in target.names:
            pattern = _name(name)
            if pattern.search(title):
                hit(target, NAME_IN_TITLE)
            elif pattern.search(body):
                hit(target, NAME_IN_BODY)

    # 4. A bare symbol settles nothing, so it is only reported, and only when no rule above
    #    already found the company in this item.
    for target in targets:
        if target.company_id in best:
            continue
        pattern = _bare(target.ticker)
        if pattern.search(title) or pattern.search(body):
            result.flags.append(Flag(target.ticker, "bare symbol in the text"))

    ticker_of = {t.company_id: t.ticker for t in targets}
    result.mentions = sorted(
        (
            Mention(company_id, ticker_of[company_id], confidence)
            for company_id, confidence in best.items()
        ),
        key=lambda m: m.ticker,
    )
    return result
