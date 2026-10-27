"""The companies whose daily prices are recorded.

Why a file and not a database edit: adding a ticker is a reviewed change (a
pull request), and US-listed names only, because Finnhub's free plan returns no
quotes for non-US exchanges (docs/TECH_STACK.md, PROJECT_STATE.md).

Starting set (ADR-0004, D-34): thesis 13's basket and its benchmark.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    ticker: str
    name: str
    exchange: str
    sector: str | None


UNIVERSE: tuple[Company, ...] = (
    Company("VZ", "Verizon Communications Inc.", "NYSE", "Communication Services"),
    Company("T", "AT&T Inc.", "NYSE", "Communication Services"),
    Company("TMUS", "T-Mobile US, Inc.", "NASDAQ", "Communication Services"),
    Company("SPY", "SPDR S&P 500 ETF Trust", "NYSE Arca", None),
)
