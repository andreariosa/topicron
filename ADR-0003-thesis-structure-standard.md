# ADR-0003: Thesis Structure Standard — From Narrative Brief to Falsifiable Investment Thesis

**Status:** Accepted
**Date:** 2026-07-30
**Deciders:** Andrea (founder), Claude (technical co-founder / senior architect)
**Decision registry:** D-25 through D-33 (continues `DECISIONS.md` §3; ADR-0001 = D-01–D-18, ADR-0002 = D-19–D-24)

## Context

Four independent reviews of `m0/topic-thesis-08-cybersecurity.md` and `m0/topic-thesis-09-airlines.md` converged, without prompting from each other, on the same structural gap: the bull/bear/risks format produces well-organized **narrative briefs**, but not yet **falsifiable investment theses**. The specific, repeated findings:

1. No single-sentence, testable hypothesis stated up front.
2. "Track against a benchmark" with no stated benchmark, no stated expected-outperformance threshold, and no stated reason that benchmark isolates the claim being made.
3. No valuation or "what does the market already price in" context — the pieces argue whether a narrative is *true*, never whether it's already *priced*.
4. No stated mechanism for why the price would move within the 90-day holding window specifically.
5. No explicit invalidation criteria — "Confidence: Medium" carries no information without a stated "wrong if X" condition.
6. The "Risks" section frequently restates the Bear case in different words rather than adding portfolio-mechanics or external risks the Bear case didn't cover.
7. Basket weights default to naive equal-weight even when the thesis text itself argues for differentiated conviction across components (write-up 9 argued Delta was protected and American carried outsized risk, then weighted both at 33.3% — the basket contradicts the argument).
8. Citations lean on secondary investment-content aggregators (Zacks, 24/7 Wall St, Kavout) where primary sources (filings, transcripts, investor presentations, IATA's own releases) were available for the same claim.
9. No "as of" framing or staleness check — write-up 8's load-bearing fact (a ~29% AI-disruption-fear drawdown) was a February 2026 data point being presented, unflagged, as the current situation in July. A direct check while drafting this ADR confirmed the premise had since inverted: CrowdStrike, Palo Alto, and Fortinet were up 60%, 79%, and 109% year-to-date respectively by late July, trading at rich valuations, with the actual live tension having shifted to whether that rally has run ahead of fundamentals — the opposite question from the one the write-up posed.

This is not a cosmetic issue. `AGENTS.md`'s "AI as product" distinction and the entire accountability-loop premise (`docs/VISION.md`) depend on theses that can actually be graded as right or wrong. A thesis written to be true in almost any outcome — "could," "may," "reflects a real question" — defeats the purpose of publishing losers at all. Automating an unfalsifiable template (M2) would faithfully reproduce this problem at scale, which is exactly the kind of expensive-to-discover-late mistake M0 exists to catch first.

## Decision

### D-25 — Adopt a ten-section thesis structure, replacing the five-section format

Every topic-and-thesis write-up, hand-written or (eventually) pipeline-generated, follows this structure:

1. **The hypothesis** — one falsifiable sentence.
2. **Why now** — what changed recently, with an explicit as-of date.
3. **What the market may be missing** — the non-obvious insight, distinct from restating the news.
4. **Bull case** — the mechanism for outperformance.
5. **Best bear case** — the strongest competing interpretation of the same evidence, not a strawman.
6. **Valuation and expectations** — what the market currently appears to price in.
7. **Catalysts** — at least one plausible mechanism for the price to move within 90 days.
8. **Invalidation conditions** — what would prove the thesis wrong, stated as observable thresholds.
9. **Basket and benchmark** — composition, weights, benchmark, expected-outperformance threshold, and the reasoning connecting all four to the hypothesis.
10. **Results at 30/60/90 days** — performance plus which of (thesis wrong / thesis right but priced in / catalyst didn't occur / market moved for unrelated reasons) actually happened. (Populated after publication; the template reserves the section now so it isn't bolted on later.)

### D-26 — The hypothesis must be a single falsifiable sentence, stated before the bull case

Example of the standard: *"Over the next 90 days, established cybersecurity vendors will outperform the broader software sector as rising AI-security demand outweighs disruption fears."* Not: two paragraphs a reader has to synthesize into a claim themselves.

### D-27 — Benchmark requires an explicit outperformance threshold and a stated reason for that specific benchmark

"Tracked against a benchmark" is not sufficient. Required: **Benchmark: [name]. Expected outcome: [basket] outperforms by at least [N] percentage points over 90 days. Reason: [what this benchmark isolates that a broader index wouldn't].** An arbitrary threshold stated in advance is more useful than a precise one interpreted after the fact.

### D-28 — Valuation and expectations is a mandatory section

At minimum: what the relevant tickers currently trade at (a multiple, relative to history/peers/growth where feasible) and one sentence on what that multiple implies the market already believes. A true statement that is already fully priced is not the same claim as an underpriced true statement.

### D-29 — At least one 90-day catalyst is mandatory

Earnings dates, guidance updates, investor days, product launches, regulatory decisions, industry data releases, or a named macro variable (e.g., oil price) with a specific level. Without a stated catalyst, a null result at day 90 is uninterpretable — it could mean the thesis was wrong, or that 90 days was simply the wrong window.

### D-30 — Invalidation conditions are mandatory and distinct from Risks

Stated as observable thresholds ("wrong if X"), not as prose restating the bear case. Example: *"Wrong if CrowdStrike's next-quarter net-new ARR reaccelerates without a corresponding stock re-rating"* is a falsifiable checkpoint; *"disruption risk"* is not.

### D-31 — Risks is redefined: portfolio mechanics and external risks, not a Bear-case restatement

Risks covers things like concentration risk (basket construction), geopolitical/macro pass-through risk, and data/execution risk — categories the Bear case doesn't already cover. If a risk-list item restates a Bear-case sentence with different adjectives, it is cut, not kept for length.

### D-32 — Basket weighting must follow from the thesis's own stated conviction, not default silently

Naive equal-weight (ADR-0001) remains the default **only** when the thesis text itself makes no differentiated claim about individual components' relative quality or risk. When the thesis explicitly argues differentiated conviction (as write-up 9 did for Delta vs. American), the basket must reflect that: overweighting, excluding a name, or reframing as an explicit relative/pair trade (e.g., long DAL vs. AAL) rather than a flat sector basket. This refines, and does not reverse, ADR-0001's equal-weight default — it adds the condition under which that default no longer applies.

### D-33 — Source hierarchy: primary sources preferred where one reasonably exists for the same claim

Regulatory/industry-body releases, earnings releases and transcripts, and investor presentations are preferred over secondary investment-content aggregators (Zacks, 24/7 Wall St, Kavout, and similar) when a primary source carries the same fact. Secondary sources remain acceptable for synthesis, context, and interpretation, and are often the only source for a "why this is trending" framing itself. Every thesis states its facts' as-of date and, where a load-bearing fact is more than a few weeks old relative to publication, flags that explicitly rather than presenting it as current.

## Consequences

- Each write-up requires meaningfully more work: a valuation check and a catalyst check are new, mandatory research steps beyond the original four-citation pattern.
- The intervention log gains a new category worth watching: cases where the *template itself* forced a stronger thesis (e.g., checking valuation surfaced that a write-up's core premise had gone stale) — this is a feature of the template, not an incidental finding, and worth noting explicitly when it happens.
- `docs/AI_SYSTEM.md`'s Agent 3 (thesis generator) output contract should eventually be updated to match this structure before any pipeline work begins (M2) — not done as part of this ADR, since M0 is still hand-written and the pipeline itself remains gated behind the M0 reader-feedback gate. Flagged here so it isn't rediscovered cold at M2.
- Write-ups 8 and 9 are rewritten under this structure as the first real test of it (see `m0/topic-thesis-08-cybersecurity.md` and `m0/topic-thesis-09-airlines.md`, both dated 2026-07-30). Write-ups 1–7 are not retroactively rewritten — revisiting them is optional, lower-priority backfill, not required to proceed.

## Alternatives considered

**Keep the five-section format, add valuation/catalysts informally as prose within the existing sections.** Rejected: the reviews' clearest finding was that Risks silently duplicating Bear-case content, and equal-weight silently contradicting stated conviction, are *structural* defects — an informal addition doesn't force the discipline of stating a falsifiable hypothesis or an explicit invalidation threshold, and the same gaps would likely recur in write-up 11 onward without a structural requirement.

**Only apply the new structure going forward, treat 8 and 9 as already "done."** Rejected: rewriting 8 and 9 is the only way to confirm the new structure actually produces a better thesis rather than just a longer one, and write-up 8 specifically can't be left as-is regardless of template — its core premise is now factually stale.
