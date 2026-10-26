# ADR-0004: Starting M1 With the Demand Half of the M0 Gate Not Tested

**Status:** Accepted
**Date:** 2026-10-26 (drafted 2026-10-21, revised 2026-10-25 with the founder's answers to the open points, accepted by the founder at the M0 verdict without changes to the decisions). The free-reader count was checked again on the evening of 2026-10-26 and was still zero, so the Context stands as written.
**Decision owners:** founder + technical co-founder
**Relationship to prior ADRs:** Additive, not reopening. It uses ADR-0001 D-03 (the price clock is the one component whose value grows with elapsed time) and ADR-0002 D-20 (the pipeline is founder-run and free). It does not change any M1 or M2 gate in `docs/ROADMAP.md`; it splits M1 in two parts that run in order, adds a checkpoint before M2 and adds one requirement to M2. It is the founder decision that `m0/round-2-channels.md` §4.1 and `AGENTS.md` §6 ("Milestone sequencing") reserve for the case where a gate half is "not tested".
**Decision registry:** D-34 and D-35 (continues `DECISIONS.md` §3; ADR-0003 = D-25–D-33)

## Context

The M0 gate (`docs/ROADMAP.md`) asks whether target-persona readers find the write-ups genuinely useful and whether the intervention delta is small enough for a pipeline to plausibly close. It says that if not, the project stops and revisits the concept before any pipeline code. The demand question ("how would you feel if this no longer existed", `docs/RISKS.md`) is recorded separately in `m0/round-2-channels.md` §4.1. Where the gate stands:

- **Quality: met on the pre-set thresholds.** 16 paid readers read write-up 13 on 2026-10-13; all four thresholds were met, three of them at the limit (`m0/reader-feedback-log.md`, `m0/prolific-study-spec.md` §5).
- **Intervention delta: "plausible, conditional".** Not small and not shrinking, but it moved from wording (write-ups 1–5) to facts and freshness against primary sources (8, 9, 13). It is closable by written rules for wording and scope, and for facts only if the pipeline checks primary sources (`m0/intervention-log-review.md`).
- **Demand: not tested.** On 2026-10-21 every free-reader source was at zero: no comments or score on the r/SecurityAnalysis post, no replies on X, no reply from the 2 outreach contacts, 0 subscribers on the landing page. The first public post was 2026-10-14. §4.1 reads this as the cost of getting attention, not as a finding about need, and the founder has no further free channel to try. The only free channels in use are X and Reddit, and nothing has been spent on promotion (founder, 2026-10-25).

So the demand half cannot be tested by waiting: no new data is expected beyond late replies. The question this ADR answers is whether M1 starts anyway, and under what condition work stops before M2.

M1 costs no money: GitHub Actions, Supabase, Finnhub (US quotes) and Vercel are all on free tiers (`docs/TECH_STACK.md`, ADR-0002 D-21). Its cost is founder hours. ADR-0002 D-20 also makes M2 founder-run, so the cost of M2 is founder time as well, not a recurring bill.

## Decision

### D-34 — M1 starts in two parts, one after the other; a demand checkpoint on 2026-11-16 decides whether M2 starts

**Decision:** M1 is split in two parts that run in order. Neither waits for the checkpoint.

- **M1a, the price clock, starts on acceptance.** Repository scaffolding (`jobs/`, GitHub Actions, an initial migration limited to what M1a needs) and the daily `prices/` job writing `price_snapshots` for the US-listed tickers and benchmarks named in the write-ups, starting with thesis 13 (VZ, T, TMUS and SPY). The job gives an independent series to cross-check the hand-recorded closes of thesis 13 at day 30, 60 and 90. No ingestion, no AI generation, no UI.
- **M1b, ingestion, follows M1a.** RSS connectors (10–15 feeds), dedupe and ticker extraction, as `docs/ROADMAP.md` lists them for M1. It starts once the M1a job is running and does not wait for the checkpoint. The founder's reading is that a low count in the coming weeks would measure how little has been done to be seen (X and Reddit only, nothing spent on promotion) more than whether the product is needed, so a low count is not a reason to hold ingestion.
- **Survey, before the checkpoint.** The founder adds a short survey to the landing page that asks the "how would you feel if this no longer existed" question, so that answers from visitors he did not contact can be counted at the checkpoint. Today the landing page only collects email signups (`app/subscribe-form.tsx`). The format is not designed here and must stay inside the free tiers (ADR-0002 D-21). It can be reached from X, the landing page and email, but not from Reddit posts: r/SecurityAnalysis rule 3 bars links and surveys, and several of the other subreddits reviewed bar surveys too (`m0/round-2-channels.md` §3.0; `m0/topic-thesis-13-distribution-copy.md` §0, item 5).
- **Checkpoint, on Monday 2026-11-16 (three weeks after the verdict):** the founder counts what free readers did in the meantime: email signups on the landing page from people the founder did not contact directly, replies on X, Reddit and email, and answers to the "how would you feel" question. Rule for continuing (the founder sets the numbers and kept these on 2026-10-25): at least 10 such signups, or at least 3 free readers who answered the question with at least 2 of them "very disappointed". **The checkpoint decides whether M2 starts. It does not decide M1b.** The public record keeps running in the meantime: the X updates after Verizon (26 Oct) and T-Mobile (28 Oct), thesis 13 at day 30 (11 Nov).
- **A miss is not an automatic stop.** At this size the numbers measure reach as much as need (`docs/RISKS.md` already warns, for the north-star metric, that a small denominator mistakes noise for signal). A miss means M2 does not start and the founder chooses between one more specific demand test, reshaping the concept, or stopping. The choice is recorded in ADR-0005.
- **Promoted posts on X are not decided here.** The founder has named them as a possible demand test. They would be a metered cost, so any spend is a separate decision under `AGENTS.md` §6 ("Money") and ADR-0002 D-19, with an explicit cap in euros set in advance. This ADR authorises no spend. To count toward the 2026-11-16 checkpoint, a test would have to start before it.

**Why:** The price clock is the only M1 component whose value grows with elapsed time (ADR-0001 D-03; `docs/ARCHITECTURE.md`, jobs table), costs nothing, and does not depend on whether anyone reads the publication. Ingestion has no such property, but it is started before the checkpoint anyway for three reasons: it costs hours and no money; a low count at this audience size is, by the founder's reading, a measure of reach and not of need, so holding M1b for it would add delay and protect nothing; and the roadmap gives M1 two weeks, so if that estimate holds M1 is done around the checkpoint and M2 can start straight after a pass. The checkpoint sits before M2 because M2 is the largest cost in the plan (3–4 weeks, marked "Highest-risk gate in the plan" in `docs/ROADMAP.md`).

**Impact:** M1a is a small share of the two weeks the roadmap gives M1 (the exact share is not estimated here). M1's own gate (content flowing, price history without gaps) is judged in two steps: price history after M1a, content after M1b. M2 gains a pre-condition: the checkpoint. The exposure the founder accepts is the hours spent on M1b before the checkpoint result is known; no money is at risk.

**Documentation change:** `docs/ROADMAP.md`: split the M1 row into M1a and M1b, in order; add the checkpoint of 2026-11-16 as a pre-condition of M2 (not of M1b); add the landing-page survey as a task before it; correct "First 30 days" and "First 10 tasks" to match. `PROJECT_STATE.md`: status, next actions, pending milestones. `DECISIONS.md`: index row and next ID (ADR-0005, D-36).

### D-35 — M2 includes a primary-source verification step and a golden set drawn from the intervention log

**Decision:** M2's thesis generation is not "done" until two things exist. First, every factual claim in a generated thesis is checked against a primary source (company releases and filings, regulator orders, exchange or Treasury data) or is labelled unverified, in the form write-up 13 uses for its $8 billion figure (a Wall Street Journal report relayed by Forbes, treated as unconfirmed). Second, the golden-set regression check (`docs/AI_SYSTEM.md`; `CONTRIBUTING.md`) is built from the cases in `m0/intervention-log.md`: the five substantive corrections in write-ups 8, 9 and 13 and the support-level removals, so that a prompt change that reintroduces one of them is caught before it ships.

**Why:** The write-up 13 errors (an announcement date and price, a percentage on a dividend-adjusted basis, a consideration stated as cash only) came from a secondary summary and were caught only by going to primary documents. A pipeline fed by RSS items, which is M1b's input, would repeat them. The roadmap's M2 deliverables list citations and validation but no primary-source step. Under ADR-0002 D-20 the step is feasible at no cost, because the founder-run session fetches the sources.

**Impact:** M2 scope grows. The roadmap's 3–4 week estimate for M2 is not revised here; the founder should expect it to move. M2 remains the "Highest-risk gate in the plan" (`docs/ROADMAP.md`), judged against the M0 quality bar by the same rubric.

**Documentation change:** `docs/ROADMAP.md`: add the two items to the M2 row. `docs/AI_SYSTEM.md`: update Agent 3's output contract (a source type and an "unverified" flag per claim), which ADR-0003's consequences already flagged as due before M2, and define the golden set from the intervention log. `docs/ARCHITECTURE.md`: note that `thesis/` needs access to primary sources.

## Alternatives considered

**M1b waits for the checkpoint, or starts on 2026-11-16 whatever the result.** Rejected by the founder on 2026-10-25. Waiting would protect founder hours only if a miss stopped M1b, and a miss is read as a measure of reach; starting on the 16th regardless would delay M1b by three weeks and protect nothing. The cost of the chosen path is the M1b hours already spent if the checkpoint later leads to reshaping or stopping. It costs no money.

**Hold M1 until a demand signal arrives.** Rejected: no free channel remains, so waiting produces no data, and every week of delay is a week of price history that cannot be recovered.

**Stop or reshape the concept now.** Rejected: the quality half is met, and a result of zero from a near-zero audience does not separate "no demand" from "no reach". It stays open as the outcome of a missed checkpoint.

**Buy attention (promoted posts on X, sponsored newsletters).** Not decided here: it would be a new metered or recurring cost. It stays a founder option, at or before the checkpoint, under `AGENTS.md` §6 and ADR-0002 D-19 and with a cap set in advance, not a default.

## Founder answers to the open points (2026-10-25) and what remains

1. Whether M1a starts before the checkpoint: yes, on acceptance.
2. M1a only, or the whole of M1: the whole of M1, in order. M1b follows M1a and does not wait for the checkpoint.
3. The checkpoint date and rule: Monday 2026-11-16, rule unchanged (10 signups, or 3 answers with 2 "very disappointed"). It decides M2 only. At this audience size the numbers are directional, not a pass/fail test.
4. Whether D-35 belongs in this ADR: yes, it stays here.
5. Acceptance is the founder's alone (`DECISIONS.md` §4): the Status stays `Proposed` until he says so, and the documentation changes above are applied in the same batch as acceptance.

Not decided here: whether to run promoted posts on X and with what cap, and the format of the landing-page survey.
