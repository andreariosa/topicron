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

## Write-up 11 — Gold Miners: Operating Leverage Still Hasn't Fully Re-Rated Into Equity Prices

First write-up drafted natively under the ADR-0003 template (not a rewrite of an older piece).

**Claims removed:**
- Did not name Newmont, Barrick, Agnico Eagle, or Franco-Nevada in the basket despite all being covered in sourcing — these are large-cap majors with less operating leverage than the mid-tier names the thesis is specifically about; including them would have diluted the actual claim (leveraged mid-tiers vs. gold) into a generic "gold miners" bet.
- Considered using a gold-miners ETF (GDXJ) as the benchmark instead of GLD, since the sourcing itself centers on the GDXJ/GDX gap — rejected because GDXJ vs. GDX tests miner selection, not this thesis's actual claim (miners vs. the metal itself). GLD is the correct, more precise benchmark for what's actually being argued.

**Basket construction note:** used equal weight here (D-32), unlike write-ups 8/9/12 — the thesis argues mid-tier miners as a *group* are under-re-rated relative to gold, not that any one of the three is specifically mispriced relative to the others, so equal weight is the correct application of D-32's own logic, not an oversight.

## Write-up 12 — EV Makers Post-Subsidy: Rivian's Proof of Profit vs. Tesla's AI Bet

First write-up drafted natively under the ADR-0003 template. The single freshest write-up to date — key facts (the Uber-Rivian deal, Rivian's Q2 earnings date) are 1-2 days old relative to the write-up date, not weeks or months.

**Timing note kept deliberately visible, not smoothed over:** Rivian's Q2 2026 earnings landed the day before this write-up was drafted. Rather than wait and risk missing the news cycle, or pretend the "why now" section reflects a post-earnings picture it doesn't, the write-up says so explicitly in its own opening note and tells the reader to check the actual print before trusting the bull case. This is a direct, practical instance of D-33 (staleness disclosure) applied at the most extreme end — hours-old, not months-old.

**Claims removed:**
- Did not include Lucid Motors or legacy automakers (Ford, GM) in the basket despite appearing in adjacent sourcing — the specific thesis is about Tesla's subsidy-era profitability crutch disappearing versus Rivian's subsidy-independent profit proof; adding names without that specific contrast would have diluted the actual claim into a generic "EV stocks" basket.

**Milestone note:** 12 of the 10-20 target for task 2, both drafted natively under ADR-0003 rather than backfilled from the old format.

## Write-up 13 — US Wireless Carriers: The SpaceX Selloff Prices a 2027 Threat Into 2026 Stocks

Drafted natively under the ADR-0003 template, 2026-10-11, as the first write-up checked against primary sources (company releases, FCC orders, Treasury data) rather than built from one secondary market summary. The topic came from a single such summary (9 October), and the template's own steps changed the thesis in these ways:

- **Facts corrected against better sources.** The summary implied a Friday announcement with a known price. The deal was announced after Thursday's close, SpaceX did not disclose a price, and the $8 billion is a Wall Street Journal figure relayed by Forbes. The thesis says so in its opening note and treats it as unconfirmed.
- **A percentage that would have been wrong.** Aggregator and article figures for Verizon (-8.75%) and AT&T (-9.81%) on 9 October are measured against a dividend-adjusted prior close, because both went ex-dividend that day. Raw close to close, which is what `price_snapshots` will record, is -10.1% and -10.8%. The thesis uses the raw figures and states the dividend effect.
- **D-29 forced a dated catalyst search.** It surfaced three Q3 report dates and, in the FCC order for the Grain licences, two dated process steps (5 November, 4 December) that no market summary mentioned.
- **D-28 forced a valuation frame.** Free-cash-flow yields of 11.6-12.8% on guidance, translated into what they imply about the market's expectations; that is the claim the thesis rests on (priced versus unpriced).
- **D-27 forced a benchmark check.** The usual sector ETF (IYZ) was rejected after reading its holdings: roughly a third is Cisco and Arista, and it holds SpaceX itself (3.9%). The thesis uses SPY and an equal-weight carrier basket. This exposes a design gap, flagged and not fixed: `docs/DATA_MODEL.md` expects `sector_benchmark_ticker` to be an ETF.

**Claims removed or not used:**
- A reported rise in Crown Castle on 9 October: single secondary source, and it is not clear which way it should be read.
- The oil and optical-networking candidates from the same summary: the first is too binary and geopolitical for a falsifiable 90-day claim, the second needs its own verification pass.
- SpaceX itself is not in the basket: the hypothesis is about whether the incumbents overshot, not about SpaceX.

**Basket construction note:** differentiated 40/40/20 (D-32), not equal weight. The thesis argues Verizon and AT&T are better supported than T-Mobile (multiple, dividend, a Q3 it has guided soft), so the basket reflects that. T-Mobile stays in at 20% because it fell most; the weighting call is graded separately at day 90.

**Re-check on 12 October (before the commit).** Facts only; price moves after the 9 October close were deliberately not used to change the thesis.
- **A consideration that was incomplete.** The first draft said T-Mobile sold its 800 MHz licences to Grain "for $2.9 billion in cash". The FCC order (DA 26-653) says $2.9 billion in cash **and** Grain's 600 MHz licences (10 MHz in 212 counties), which T-Mobile's own August release confirms. The cash-only wording understated what T-Mobile received and made the comparison with SpaceX's reported $8 billion look like for like. Corrected in the thesis (source 1, T-Mobile weighting note) and in the distribution copy.
- **A fact added.** SpaceX's statement to the FCC asks for expedited approval and describes a terrestrial overlay on towers and rooftops, not only satellite service (Light Reading, now source 20). The bear case says so, and the hypothesis now says "a SpaceX mobile service" instead of "a satellite-based competitor"; the measurable claim (basket, SPY, 5 points, 90 days) is unchanged.
- **Closes cross-checked.** The 9 October closes agree to the cent on companiesmarketcap.com (VZ, T, TMUS) and stockinvest.us (VZ, SPY). All are aggregators and exchange data was not reachable; the founder then confirmed all four closes (VZ, T, TMUS, SPY) against investing.com the same day.
- **Checked and unchanged.** Q3 dates (company releases for AT&T 21 Oct, Verizon 26 Oct, T-Mobile 28 Oct); the $8 billion remains a Wall Street Journal report that neither company has confirmed (one trade-press summary also credited Bloomberg, and the next one did not, so it is not used); no carrier statement or FCC action since 9 October was found.

**Open items carried forward:** SpaceX's blog post and FCC filing were not opened directly (described by Light Reading); `AGENTS.md` §6/§7 and `CLAUDE.md` still conflict with D-32 on weighted baskets (`PROJECT_STATE.md`, Known technical debt).

**Milestone note:** 13 of the 10-20 target for task 2.

## Validation spend

- **2026-10-12: Prolific reader panel approved by the founder, cap EUR 100** (`AGENTS.md` §6, "Money"; one-off validation spend, not a stack component, so ADR-0002 D-19 is untouched). Design and worst-case cost: `m0/prolific-study-spec.md`. Spent so far: nothing. Replace this line with the actual total when the studies close.
