# ADR-0005: Starting M2 After the Demand Checkpoint of 2026-11-16 Was Missed

**Status:** Accepted
**Date:** 2026-11-21 (drafted and accepted by the founder the same day, without changes to the decision)
**Decision owners:** founder + technical co-founder
**Relationship to prior ADRs:** Applies and, for one point, amends ADR-0004 D-34. D-34 made the demand checkpoint a pre-condition of M2 ("a miss means M2 does not start") and listed three ways forward after a miss (one more demand test, reshaping the concept, stopping), to be recorded here. The founder chose a fourth, which D-34 does not list: M2 starts anyway. ADR-0004 stays `Accepted` and its text is not edited; this ADR waives the pre-condition for M2, once, and changes nothing else in D-34 or D-35. It does not reopen ADR-0001, ADR-0002 or ADR-0003, and it adds no spend (ADR-0002 D-19, D-20, D-21).
**Decision registry:** D-36 (continues `DECISIONS.md` §3; ADR-0004 = D-34–D-35)

## Context

D-34 set the checkpoint for Monday 2026-11-16 with the rule the founder fixed on 2026-10-25: at least 10 signups from free readers the founder did not contact, or at least 3 free readers answering "how would you feel if this no longer existed" with at least 2 "very disappointed". It decides whether M2 starts.

**The checkpoint was not held on 2026-11-16.** The founder counted on Saturday 2026-11-21 at about 19:30 Rome, five days late. The delay does not change the count: the rule counts signals since 2026-10-26, and the only paid source, the X test, had been paused since 2026-11-09.

**Result: missed on both branches.**

- Signups: 0. Resend Contacts is empty (the founder's own test contact of 2026-11-13, which showed that the chain form, `/api/subscribe`, Resend works end to end, has been deleted).
- Survey answers: 0. Tally shows 0 submissions and 3 visits in all; some of those visits are the founder's and the assistant's own checks, so at most one can have come from the ad.
- Replies, comments and votes on X and Reddit: none, including the day-30 posts of 2026-11-12. Inbox: empty.
- The X test (2026-11-04 to 2026-11-09): 59,232 impressions, 115 link clicks, EUR 23.28 net (about EUR 28.4 with VAT), no survey answer. The landing page has no analytics, so where the clicks were lost is unknown.

**What the miss does and does not show.** It shows that no free reader has reached the survey or the signup form in five weeks of public posting. It does not separate "nobody needs this" from "nobody was reached": the founder's channels are small, nothing else is planned, and the one paid test did not get a single visitor to the survey. D-34 already read a miss this way. The demand half of the M0 gate stays "not tested", as it was when ADR-0004 was accepted.

## Decision

### D-36 — M2 starts although the checkpoint was missed; no further demand checkpoint is added

**Decision:** The founder starts M2 on 2026-11-21. The checkpoint is recorded as missed, not reinterpreted. For this occasion only, a miss does not stop M2. Everything else about M2 stays as ADR-0004 D-35 and `docs/ROADMAP.md` set it: the Agent 3 output contract in `docs/AI_SYSTEM.md` is the first task, before prompts and the golden set; every factual claim is checked against a primary source or labelled unverified; the golden set comes from `m0/intervention-log.md`.

Three boundaries go with the decision:

1. **No new spend.** M2 is founder-run (ADR-0002 D-20) and costs hours. No promoted posts, no paid reader panel and no new service are authorised here; any of them is a separate decision with a cap in euros set in advance (`AGENTS.md` §6, "Money").
2. **No extra stop condition is added.** The founder declined a dated recount (proposed: Monday 2027-01-11, the exit of thesis 13, with the D-34 rule counted from 2026-11-21). The next reading of demand is M3's gate (do people open, read, return and share, over at least four issues). Stopping or reshaping stays open to the founder at any time, and M2's quality gate and M3's gate can each stop the project (ADR-0001 D-08).
3. **The demand half stays "not tested".** The PROJECT_STATE verdict wording and the public posts do not say or imply that demand has been shown.

**Why:** M2 costs founder hours and no money, which is the same reason D-34 started M1 with the demand half untested. A miss at this audience size measures reach more than need, so it is weak evidence for stopping. The price record and the thesis-13 track record keep accumulating whatever the pipeline does, and M3 is the first milestone in which demand can be read from public pages and a weekly email instead of from the founder's own channels. Stopping now would give up a free option for a result that cannot tell the two readings apart.

**Impact:** M2's gate question asks whether automated output holds the M0 quality bar "judged against the same rubric by the same readers" (`docs/ROADMAP.md`). Those readers were a paid panel, the unused balance was forfeited on 2026-10-21, and no free readers exist. **How M2's gate gets its readers is open and is not decided here.** A panel is spend, so it is decided before that gate with a cap in advance; until then M2 can be built and tested against the rubric by the founder, but it cannot be declared passed on reader evidence.

**Risks accepted (recorded here, not argued away):** the largest risk to the project is still reach, not the pipeline, and M2 does not address it (`docs/ROADMAP.md`, Distribution workstream: a pipeline that produces excellent theses nobody sees has the same practical outcome as one that produces mediocre ones). Hours already spent on M1b, and hours spent on M2, are lost if M3's gate later says no. The landing page still has no analytics, so the next demand reading would again leave the funnel unmeasured unless that changes; adding analytics needs a change to the privacy policy and a founder decision, and is not made here.

**Documentation change:**
- `docs/ROADMAP.md`: the M2 row (the checkpoint was missed and M2 starts anyway, ADR-0005 D-36; the readers for M2's gate are not yet arranged), the "what moved" note, the M1b close-out line "For M2", the "First 30 days" closing paragraph and "First 10 tasks" item 9.
- `PROJECT_STATE.md`: twenty-third update; the checkpoint result after the M0 verdict; the M2 rows; the ADR table (ADR-0004's still-to-do, the new ADR-0005 row, next ID ADR-0006 and D-37); priorities and next actions; one Known technical debt row for the missing analytics.
- `DECISIONS.md`: index row for ADR-0005; next ID ADR-0006 (D-37).
- `m0/round-2-channels.md` §4 (table rows for the day-30 posts and the checkpoint; the status of 2026-11-21 in §4.1), `m0/reader-feedback-log.md` (counts of 2026-11-21), `m0/intervention-log.md` (billing re-read), `m0/topic-thesis-13-distribution-copy.md` §3 (heading: posted).

## Alternatives considered

**One more demand test before M2.** Not chosen by the founder. It would need a cap in euros. The one paid test of this kind produced no survey answer from 115 clicks, so a second test would measure the same lost funnel unless the funnel changed first.

**Reshape the concept.** Not chosen. Nothing in the data points at a specific change: the quality half of the gate was met, and the miss is about reach.

**Stop.** Not chosen. M2 costs hours only, and stopping would end the track record that is the one asset accruing with time.

**A dated recount (2027-01-11, same rule, counted from 2026-11-21).** Proposed by the assistant as a stop-loss so that "continue anyway" is not open-ended; declined by the founder on 2026-11-21, who prefers no checkpoint beyond the gates already in the plan. Recorded here because the first reading of demand after M2 is therefore M3's gate, not a calendar date.
