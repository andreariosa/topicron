# M0 Intervention Log

*Kept alongside the hand-written topic+thesis write-ups per ADR-0001, D-09. Logs every topic rejected before selection, every claim removed for being unsupported, and every sentence rewritten. Reviewed as part of the M0 gate (docs/RISKS.md, Validation strategy).*

## Write-up 1 — AI Power Demand Reshapes Regulated Utilities

**Topics rejected before selection:**
- "AI bubble risk vs. hawkish Fed" (macro theme) — too macro, no clean set of tickers to link into a basket.
- "Mega-IPO rotation" (BlackRock note on capital rotating from AI buyers to AI sellers) — real narrative, but specific beneficiaries stayed too vague for a defensible basket.

**Claims removed:**
- Single-analyst price targets cited in only one article each (e.g., a $455 target on Eaton, a $77 target on Edison International via Barclays) — one analyst, one source, not solid enough to include even paraphrased.

**Sentences rewritten:**
- First draft of the bull case used assertive language ("will keep climbing," "is set to benefit") — rewritten to hedged language ("could continue," "may let") per AI_SYSTEM.md's hallucination-mitigation rule.

**Other observations:**
- This topic is more *consensus* than *emerging* — covered by at least 5 mainstream financial outlets within a 2-3 week window. For a genuine earliness test (ROADMAP.md M0 task 4, RSS vs. Reddit), future write-ups should deliberately favor less mainstream-covered narratives.

## Write-up 2 — GLP-1 Capacity Buildout Reaches an Inflection Point

**Topics rejected before selection:**
- 2026 mega-IPOs (SpaceX, OpenAI, Anthropic) and their index-inclusion mechanics — genuinely fresher and less covered than the utilities topic, but no confirmed, defensible ticker: SpaceX IPO'd June 12, 2026 but no verified ticker found in sourcing; OpenAI and Anthropic remain private/rumored, not investable. A real topic that doesn't yet resolve into a defensible thesis — worth revisiting once tickers and listing status are confirmed.

**Claims removed:**
- Did not name any specific generic/biosimilar manufacturer — sources referenced them only generically ("Asian manufacturers," "compounding pharmacies"), not specific enough to cite as fact.

**Sentences rewritten:**
- Bull case's claim about oral-drug addressable-market expansion was initially more assertive — softened to "may expand."

**Other observations:**
- Good sector diversification signal: this write-up sits in pharma/healthcare rather than AI/tech, useful for the reader panel to judge whether the writing quality holds outside the most obvious AI-adjacent narratives.

## Write-up 3 — European Defense Rearmament: From Momentum Trade to Selective Story

**Claims removed:**
- Did not include Saab or Safran in the suggested basket, despite both appearing in some sourcing — kept the basket to the four companies (Rheinmetall, BAE Systems, Thales, Leonardo) named most consistently across independent sources, rather than every name mentioned anywhere.

**Sentences rewritten:**
- Bull case softened from an earlier, more assertive framing of budget commitments as guaranteed to "could support" / "unusual for" language.

**Other observations (this one matters beyond this write-up):**
- **Open data-infrastructure question, not an investment risk.** All four linked companies trade on non-US exchanges (XETRA, LSE, Euronext Paris, Borsa Italiana). Finnhub's marketing claims broad global-exchange coverage, but independent reviews describe real-time depth as "uneven... stronger in US markets than in many international markets" on the free tier. This has NOT been verified with an actual API call. Before this thesis (or any non-US-listed thesis) could be tracked in `price_snapshots`, someone needs to confirm Finnhub's free tier actually returns clean, working quotes for these four tickers specifically. Flagged in PROJECT_STATE.md's Known Technical Debt as well, since this is a real, durable finding, not just a note about one write-up.
- Deliberately chosen to diversify sector coverage per write-up 1's own note about favoring less mainstream-covered narratives going forward — defense/industrials is a genuinely different sector from AI/utilities and pharma.

## Write-up 4 — US Manufacturing Reshoring Reaches Decade-High Growth Forecasts

**Claims removed:**
- Did not cite specific order-backlog or capex figures for GE Aerospace or EnerSys individually — sourcing supported company-level specificity only for Caterpillar (the Japan-to-Georgia/Texas move, the $725M figure); kept the other two names at the sector-level claims the sources actually supported.

**Sentences rewritten:**
- First draft conflated the tariff-policy legal risk and the cost/margin economics risk into one vaguer sentence — split into two distinct, independently-stated risk vectors since they have different triggers and timelines.

**Other observations:**
- This topic sits closer to active government policy (tariffs, administration priorities) than the first three. Framed the bull/bear split around durability-of-policy vs. underlying-economics specifically so neither side reads as a political endorsement — the bull case is the structural/secular argument, the bear case is the legal-durability-plus-cost-economics argument, not a stance on tariff policy itself.
