# M0 intervention-log review

*Written for the founder's round-2 review on 2026-10-21 and accepted by him that day (chat). The reading in section 6 is recorded as a gate result only when the verdict is written. Nothing here changes an ADR. Source: `m0/intervention-log.md` at commit 36a9d52 (13 write-ups).*

## 1. The question and the rule

The M0 gate (`docs/ROADMAP.md`) asks: "is the intervention delta small enough that a pipeline could plausibly close it? If not, stop and revisit the concept before writing a line of pipeline code." ADR-0001 D-09 adds that the delta "is the M2 engineering backlog" and that a large delta "means the validated product was a human writing, not a pipeline".

No document sets a number for "small enough". The answer below is therefore a judgement, and it is labelled as one.

## 2. What the log contains

| Category | Entries | Where |
|---|---|---|
| Topics rejected before selection | 4 | write-ups 1 (2), 2 (1), 6 (1) |
| Claims removed or left out | 18 | 16 bullets under "Claims removed", plus one excluded source (write-up 8) and one claim excluded from the catalysts (write-up 9) |
| Sentences rewritten | 5 | write-ups 1 to 5 |
| Substantive corrections (the draft was wrong or stale) | 5 items in 3 write-ups | 8 (stale premise), 9 (the favoured carrier changed), 13 (three: announcement timing and price, percentage on the wrong basis, a consideration stated as cash only) |

The counts are entries in a narrative log, not edits or hours. One entry can cover a rewritten section.

## 3. What the counts do not show

- **Logging is uneven.** Rewritten sentences are logged only for write-ups 1 to 5, and rejected topics only for 1, 2 and 6. Silence after that means either no intervention or no logging; the log cannot tell which.
- **There is no first-draft-versus-final comparison.** The log records changes made inside working sessions (some Claude's own corrections, some the founder's checks). It does not measure the distance between a one-shot model output and the published text, so it cannot say how much of a raw pipeline output would have survived.
- **There is no measure of time or effort.**

## 4. The 18 removals, by kind

- **Support: 8.** A claim with one source, a stale source, or one that could not be verified. Write-up 1 (single-analyst price targets), 2 (manufacturer names), 4 (GE Aerospace and EnerSys figures), 6 (figures from 2025; a name with one source), 8 (an unverifiable source), 9 (discontinued merger talks used as a catalyst), 13 (a single-source price move).
- **Scope and selection: 10.** Names or benchmarks left out by a rule or a judgement. Write-up 3, 5, 7, 9 (European carriers), 10, 11 (two), 12, 13 (two).

The log already states or implies the rules behind the scope choices: US-listed names only (5, 9, from the Finnhub gap in 3); no company in two baskets (10); a name needs support from more than one source (3, 7); the benchmark must test the stated claim (11, 13); keep the basket to the names that carry the claim (11, 12).

## 5. Where the delta moved

- **Write-ups 1 to 5:** wording and hedging (four of the five rewrites turn assertive wording into hedged wording; the fifth splits a conflated risk), plus support-level removals. Small and mechanical.
- **Write-ups 8, 9 and 13:** factual accuracy and freshness. A premise that had gone stale (8), a favoured carrier that changed after earnings (9), and in 13 an announcement date and price that one market summary had wrong, a percentage measured against a dividend-adjusted close, and a consideration that was cash plus licences, not cash only.
- **The delta did not shrink as the write-ups improved; it changed kind.** Write-up 13 is the first checked against primary sources and has the longest log. This is also consistent with checking having become stricter rather than the early write-ups being error-free, which the log cannot exclude.
- **The ADR-0003 template caught some of it.** The log credits it with the stale premise in write-up 8 (D-28) and with three changes in write-up 13 (D-27 benchmark, D-28 valuation frame, D-29 dated catalysts). The other corrections in write-up 13 came from re-checking against primary documents.

## 6. Proposed reading for the gate

1. **Closable by written rules:** wording (5) and scope (10). The rules exist in the log, in ADR-0003 and in the standing US-listed guideline.
2. **Closable only if the pipeline checks claims against primary sources:** the support-level removals (8) and the five substantive corrections. The write-up 13 errors came from a secondary summary. A pipeline that summarises RSS items, which is M1's input, would repeat them.
3. **Not shown by this log:** whether M2 as planned (thesis generation with citations, structured-output validation, a golden-set check) would catch these cases. The roadmap does not list a primary-source verification step for M2.

Proposed wording for the gate record, in the style of `m0/round-2-channels.md` §4.1:

> Intervention delta, read on 2026-10-21 from 13 write-ups: not small, and not shrinking; it moved from wording (write-ups 1 to 5) to factual accuracy and freshness against primary sources (8, 9, 13). Plausibly closable only if the pipeline verifies claims against primary sources; M2 as planned does not yet include that. Recorded as "plausible, conditional", not as passed.

The alternative is "not tested": no pipeline exists, so the gate's "plausibly" cannot be backed by a run. Both are defensible; the first says more.

## 7. For the founder to decide

1. Done on 2026-10-21: the draft and the reading in section 6 were accepted.
2. Whether a primary-source verification step becomes a stated requirement for M2. That changes M2's scope, so it belongs with the gate verdict (and in ADR-0004 if one is written).
3. If more write-ups are written, log rejected topics and rewrites for each, so the next review has counts that can be compared.

Sources: `m0/intervention-log.md`; `docs/ROADMAP.md` (M0 gate); `docs/ADR/ADR-0001-mvp-scope-and-architecture.md` D-09; `docs/ADR/ADR-0003-thesis-structure-standard.md`.
