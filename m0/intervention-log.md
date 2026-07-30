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
- **Data-infrastructure finding, not an investment risk — resolved, confirmed via live API call (2026-07-28).** All four linked companies trade on non-US exchanges (XETRA, LSE, Euronext Paris, Borsa Italiana). Tested directly: `quote?symbol=AAPL` returns real data on the free tier; `quote?symbol=RHM.DE`, `BA.L`, `HO.PA`, and `LDO.MI` (the exact symbols Finnhub's own search endpoint returned for these four companies) all return `{"error":"You don't have access to this resource."}` with the same key. Confirmed: Finnhub's free tier does not cover quotes for these non-US exchanges — this is a paywalled-tier limitation, not a bug or a missing setup step. This write-up remains valid for M0's reader-validation purpose (the writing itself doesn't depend on live tracking), but if any European-defense-style thesis is ever promoted to a real tracked position, it cannot use Finnhub's free tier as-is. Going forward, new write-ups should default to US-listed companies or US-listed ADRs unless a deliberate decision is made to pay for expanded coverage.
- Deliberately chosen to diversify sector coverage per write-up 1's own note about favoring less mainstream-covered narratives going forward — defense/industrials is a genuinely different sector from AI/utilities and pharma.

## Write-up 4 — US Manufacturing Reshoring Reaches Decade-High Growth Forecasts

**Claims removed:**
- Did not cite specific order-backlog or capex figures for GE Aerospace or EnerSys individually — sourcing supported company-level specificity only for Caterpillar (the Japan-to-Georgia/Texas move, the $725M figure); kept the other two names at the sector-level claims the sources actually supported.

**Sentences rewritten:**
- First draft conflated the tariff-policy legal risk and the cost/margin economics risk into one vaguer sentence — split into two distinct, independently-stated risk vectors since they have different triggers and timelines.

**Other observations:**
- This topic sits closer to active government policy (tariffs, administration priorities) than the first three. Framed the bull/bear split around durability-of-policy vs. underlying-economics specifically so neither side reads as a political endorsement — the bull case is the structural/secular argument, the bear case is the legal-durability-plus-cost-economics argument, not a stance on tariff policy itself.

## Write-up 5 — Memory Chip Supercycle: AI Demand Crowds Out Consumer Supply

**Claims removed:**
- Did not include Samsung or SK Hynix in the suggested basket despite both controlling the largest share of DRAM/HBM supply and appearing throughout the sourcing — both trade on the Korea Exchange (non-US), and given the already-open Finnhub non-US-coverage question from write-up 3, chose not to compound the same unresolved data question in a second basket. Kept to Micron and SanDisk, both cleanly US-listed.

**Sentences rewritten:**
- Bull case's framing of "unusual pricing power" was softened from an earlier draft that implied durability with more certainty than the sourcing supports.

**Other observations:**
- Deliberately different sector (semiconductors/memory) from all four prior write-ups. This is the first write-up where the single most useful data point (Bloomberg's ~700% YoY DRAM spot price figure) came from a source that was itself citing Bloomberg rather than Bloomberg directly — flagged here for transparency; the secondary source's citation of Bloomberg reads as credible given it's corroborated in direction (if not exact magnitude) by three other independent sources' contract-price figures.

## Write-up 6 — Regional Banks Re-Rate on Yield Curve Normalization and a Seven-Year M&A Wave

**Topics rejected before selection:**
- Initially considered using KRE (the regional-bank ETF) as the linked ticker instead of individual companies, since the strongest, most current sourcing was sector-level rather than company-specific. Chose to search further instead, since DATA_MODEL.md's schema is built around individual companies and introducing an ETF would raise a new, avoidable schema question. Found clean multi-source support for two individual names (HBAN, WAL) instead.

**Claims removed:**
- An initial candidate source (transcriptai.substack.com) had specific loan-growth and NIM figures for Western Alliance and Wintrust, but on inspection those figures were from Q2 2025, not 2026 — over a year stale relative to the rest of this write-up's sourcing. Discarded entirely rather than mixed in with current data.
- Did not add Webster Financial as a third basket name despite appearing on the same "strongest projected gains" list as HBAN and WAL — only single-source support, versus multi-source corroboration for the other two.

**Other observations:**
- Fourth different sector in a row (financials/banking), continuing the deliberate diversification from write-up 1's note.

## Write-up 7 — Homebuilders Whipsaw as Mortgage Rates Reverse Mid-2026

**Claims removed:**
- Did not include NVR, Century Communities, Green Brick Partners, or Rocket Companies in the basket despite all being named in sourcing — kept to the four names (Lennar, D.R. Horton, PulteGroup, Toll Brothers) with the most consistent cross-source coverage of the specific rate-reversal dynamic, rather than every builder mentioned anywhere.

**Other observations:**
- Genuinely fresh, not consensus: the bull case (rate-cut rally) and bear case (rate reversal) both happened *within 2026 itself*, one after the other — a real contrast with write-up 1's own self-flagged staleness.

## Write-up 8 — Cybersecurity Caught Between AI-Driven Demand and AI-Disruption Fear

**Source excluded, not just a claim:**
- Found a 24/7 Wall St piece on SentinelOne that tied rising federal AI-security budgets to something it called "Mythos revelations." Excluded this source entirely rather than attempt to characterize what that event actually was — I don't have confident, verified knowledge of it, and citing a claim I can't accurately explain would be worse than leaving it out. Built the write-up entirely from the other three sources instead, which stand on their own.

## Write-up 9 — Airlines Diverge as Fuel Costs Spike and IATA Slashes Its 2026 Profit Outlook

**Claims removed:**
- The IATA source also covered European carriers (IAG, Air France-KLM, Lufthansa, Wizz Air, Ryanair, easyJet) hit by the same fuel shock — excluded all of them from the basket, sticking to US-listed carriers only, consistent with the standing guideline from the confirmed Finnhub non-US-exchange gap.

## Write-up 10 — Solar Splits Between Protected Utility-Scale Backlogs and a Residential Policy Reset

**Claims removed:**
- NextEra Energy (NEE) appears repeatedly in solar-sector sourcing and was a real candidate for this basket — excluded specifically because NEE is already a position in write-up 1's basket (AI power demand/utilities). Letting the same company anchor two different write-ups' baskets would create an unintentional overlapping position across otherwise-distinct theses. Used First Solar and Enphase instead, both well-corroborated independently of NextEra.

**Milestone note:** this write-up brings the total to 10 of the 10-20 target for task 2 — the low end of the range is now met.

## ADR-0003 — Thesis structure standard (2026-07-30)

Four independently-obtained reviews of write-ups 8 and 9 converged on the same structural gaps without cross-referencing each other: no falsifiable hypothesis stated up front, no benchmark/threshold, no valuation context, no 90-day catalyst, no invalidation criteria distinct from Risks, Risks sections restating the Bear case, basket weights defaulting to equal-weight even when the thesis text argued differentiated conviction, and secondary-source-heavy citations where primaries existed. Formalized as ADR-0003 (D-25 through D-33) rather than treated as one-off polish, since the same gaps would likely recur in every future write-up without a structural requirement, and because this touches the eventual pipeline's output contract (`AI_SYSTEM.md`), not just these two documents.

## Write-up 8 — major factual correction, not just a template pass

While gathering valuation data to satisfy the new template (D-28), discovered the original write-up's entire premise had gone stale: it was built on a February 2026 source describing a ~29% AI-disruption-fear drawdown in CrowdStrike and Palo Alto Networks. A direct check found the opposite situation as of July 30: CrowdStrike +60% YTD, Palo Alto +79% YTD, Fortinet +109% YTD, all trading at rich-to-extreme multiples. This is exactly the staleness risk one of the four reviews (002.txt) named explicitly and specifically about this piece — confirmed, not just theoretically true.

**Action taken:** did not patch the old narrative. Rebuilt the topic and thesis from the current situation — a valuation-dispersion thesis (Fortinet's discount to CrowdStrike/Palo Alto despite comparable-or-better fundamentals) replaces the original disruption-fear thesis. Basket changed from equal-weight three-name to a differentiated 50/25/25 overweighting Fortinet, per D-32. Old version fully superseded, not kept as an alternate draft.

## Write-up 9 — updated, not rebuilt, but the "who's winning" framing changed

Q2 2026 earnings were reported for all three carriers since the original draft. The update didn't invalidate the divergence thesis, but it changed which carrier the thesis should favor: United's Q2 print (raised full-year guidance despite absorbing the largest fuel-cost increase of the three) reads stronger than the original write-up's framing of United as the higher-risk, secondary contrarian idea behind Delta. Rewrote the hypothesis around United specifically, with Delta reframed as "quality already priced in" (16x forward vs. an 11x sector average) rather than the clear leader, and added the oil-price whipsaw (WTI ~$101 to ~$85 in two weeks) as a live, ongoing catalyst rather than a static backdrop. Basket changed from equal-weight to 45/35/20 (UAL/DAL/AAL), per D-32.

**Claim deliberately excluded:** a Wall Street Journal report of past United-Delta and United-American merger approaches. Included only as a named risk/wildcard, not as a catalyst the thesis depends on, since the talks were reported as not having progressed or having been rejected — treating rumored, discontinued M&A talks as a forward-looking catalyst would overstate their relevance.

**Milestone note:** these are the first two write-ups under the ADR-0003 template. Write-ups 1-7 remain under the original five-section format; revisiting them is optional per ADR-0003's stated consequences, not required before continuing.
