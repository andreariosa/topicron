"""How each company is named in a headline, for the companies in the `companies` table.

Why a file: adding a name is a reviewed change, like adding a ticker to the prices universe
(jobs/prices/universe.py). A company with no entry here is still found by its symbol, in the
forms matching.py accepts; only the plain-name rule needs this list. Case does not matter.
"""

from __future__ import annotations

ALIASES: dict[str, tuple[str, ...]] = {
    "VZ": ("Verizon",),
    "T": ("AT&T",),
    "TMUS": ("T-Mobile",),
    # The fund, not the index: "S&P 500" alone is the index and must not match.
    "SPY": ("SPDR S&P 500",),
}
