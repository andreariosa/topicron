# PROJECT_STATE.md

*The single, live answer to "where is this project right now" — for the founder and for any AI assistant starting a session cold. Update this whenever a milestone gate passes, an ADR's status changes, a deferred trigger fires, or a priority shifts (`AGENTS.md` §8's docs-sync discipline applies to this file at least as much as any other document). Last updated: 2026-10-21 (sixth update) — ADR-0004 drafted as Proposed: M1 in two parts with a demand checkpoint (D-34) and a primary-source step for M2 (D-35); the founder decides at the verdict. Fifth update, the same day — round-2 review done: every free-reader source is at zero (no comments, no replies, no subscribers), a follow-up went to each of the 2 outreach contacts, r/ValueInvesting was skipped, no further free channel is planned, the reading of the intervention log is accepted (`m0/intervention-log-review.md`), the M0 gate verdict was brought forward from 2026-11-07 to Monday 2026-10-26 (founder), and no further Prolific spend is planned. Fourth update, 2026-10-16 — outreach closed by the founder after 2 messages (the search found 2 candidates who passed the filter), the landing-page list is empty (0 subscribers), and the observations are in `m0/reader-feedback-log.md`. Third update, the same day — r/SecurityAnalysis: the Request to Post sent on 2026-10-12 was counted as no on 2026-10-14, then approved by the moderators on 2026-10-15; AutoModerator removed the first submission at once (account under 60 days old) and the moderators approved the post, so it has been live since 2026-10-16; the Reddit and outreach lines of task 3, the gate line, the priorities and the next actions were brought in line. Second update, 2026-10-14 — r/SecurityAnalysis counted as no (reversed on 2026-10-15), the X thread posted, Prolific spend closed at about £66.49 (about EUR 79), and the one-page default restated as "not shown to be worse than the full text". First update the same day — Round 2 of task 3 run and read: a paid reader panel (Prolific) read write-up 13 in a full-text and a one-page version, 16 readers in all (results in `m0/reader-feedback-log.md`, setup and cost in `m0/prolific-study-spec.md` and `m0/intervention-log.md`), and `m0/round-2-channels.md` now carries the execution status and a proposed wording for the 2026-11-07 verdict. Task 3, the M0 gate line, the current-phase paragraph, the priorities and the next actions were re-checked; the other statuses are as of 2026-08-05 and were not re-checked. Earlier: 2026-10-12, write-up 13 added with its Reddit and X copy, subreddit rules recorded, r/stockpitches dropped as dormant, the Prolific panel approved (cap EUR 100); 2026-10-10, consistency cleanup of counts and wording, and GitHub `main` documented as the single source of truth with a manual Claude Project re-sync after every commit (`CONTRIBUTING.md` §11, `AGENTS.md` §15).*

## Current phase

Pre-build for the real application (jobs/, Supabase schema, ingestion) — M0 concierge test in progress. Planning, architecture, and repository-governance documentation are complete. The repository holds `docs/*.md`, `docs/ADR/ADR-0001`, `ADR-0002`, and `ADR-0003`, the six process files this earlier phase of work produced (`AGENTS.md`, `CLAUDE.md`, `CURSOR_RULES.md`, `DECISIONS.md`, `CONTRIBUTING.md`, this file), `m0/` — thirteen hand-written topic-and-thesis write-ups (two also in Italian), the intervention log, the distribution and RSS feed lists, the earliness log, the reader questionnaire and feedback log, and the privacy-policy source text — and `app/`, a live Next.js landing page with a Resend-backed `/api/subscribe` route at topicron.vercel.app.

Worth saying plainly, since accuracy is this file's entire job: everything built so far, including the thirteen write-ups now in `m0/`, is still validating the core hypothesis, not building the product itself. Topicron's actual core hypothesis — whether a target-persona reader finds a hand-written thesis genuinely useful — now has its first careful reads: 16 paid readers who say they invest in individual stocks read write-up 13 on 2026-10-13, and they meet the quality thresholds (three of four at the limit). The other half, whether anyone would miss it, is untested: paid readers cannot answer it without inflation, and round 1 (personal network, three skimmers) did not.

## Completed milestones

None. M0 is the first milestone in `docs/ROADMAP.md` and is in progress (see below).

## Active milestone

**M0 — Validate the writing.** Status against `docs/ROADMAP.md`'s "First 10 tasks":

| # | Task | Status |
|---|---|---|
| 1 | File the Reddit API developer application | **Rejected, 2026-08-05.** Generic rejection ("not in compliance with Reddit's Responsible Builder Policy and/or lacks necessary details"), no specific deficiency given. Closed — reapplying without knowing what specifically fell short wouldn't have better odds, and the task 4 finding had already lowered the expected value of Reddit ingestion regardless. Reddit ingestion itself remains deferred per ADR-0001, D-10; this closes one path to it, not the underlying decision. |
| 2 | Hand-write 10–20 topic-and-thesis write-ups, with an intervention log | **13 of 10–20 done**, spanning 11 distinct sectors (`m0/topic-thesis-01` through `13`). Write-ups 8, 9, 11, 12, and 13 follow the ADR-0003 ten-section template — 11, 12, and 13 drafted natively under it, not rewrites. Write-ups 1–7 remain on the original five-section format; backfilling them is optional, not required. Intervention log live and current at `m0/intervention-log.md`. |
| 3 | Write down the primary persona; share write-ups with 5–10 target-persona readers | **Round 1 inconclusive; round 2 half done (2026-10-21).** Persona done (`docs/VISION.md`, `README.md`). Round 1 (personal network, 2026-07-30/31): 3 of 5 readers responded and all 3 skimmed (`m0/reader-feedback-log.md`). Round 2, paid panel (Prolific, approved 2026-10-12, cap EUR 100): on 2026-10-13, 16 readers read write-up 13, 10 the full text and 6 a one-page version; about £66.49 spent, roughly EUR 79, of £72.81 reserved (`m0/prolific-study-spec.md`, `m0/intervention-log.md`). The quality thresholds are met (three of four at the limit); the one-page version is not shown to be worse than the full text within the pre-set margin (on its own it misses the "any stock" threshold), so it is the entry format for readers who do not know the author, with the full text always linked; 13 of 16 readers named the invalidation conditions among the most useful parts. Not answered: whether anyone would miss it, which only readers who read for free can say. Free-reader channels: X (@topicron) thread posted 2026-10-14, an AT&T Q3 update posted on 2026-10-21, no replies; outreach to independent analysts from a private kit that is not in the repository: the search found 2 candidates who passed the filter, 2 messages were sent on 2026-10-16, a follow-up to each on 2026-10-21, no reply so far, and the search was closed (results and observations: `m0/reader-feedback-log.md`); the landing-page list had 0 subscribers on 2026-10-21 (the X profile links to the page); Reddit — r/SecurityAnalysis: the Request to Post, counted as no on 2026-10-14, was approved by the moderators on 2026-10-15; AutoModerator removed the post at once (account under 60 days old) and the moderators approved it, so it has been live since 2026-10-16 (no comments as of 2026-10-21; a dated AT&T Q3 comment was added under it); r/ValueInvesting blocks posting by an account-age check (probably also an age rule) and was skipped on 2026-10-21, r/stockpitches was dropped as dormant, and r/investing, r/StockMarket and r/ItaliaPersonalFinance are excluded (AI-text and self-promotion rules). Channel facts and rules: `m0/round-2-channels.md`. |
| 4 | Read relevant subreddits by hand; log earliness vs. curated RSS | **Done, with a finding rather than a clean number.** Two separate attempts (manual sorted search, then a broader scrape across four phrases) found Reddit's native search unreliable for narrow financial narratives — including one search term ("Huntington Bancshares") that returned only an unrelated same-named company (Huntington Ingalls Industries), zero real matches. Documented in `m0/earliness-log.md`, with a recommendation to cross-reference it from `docs/RISKS.md` or `docs/MVP_SCOPE.md`'s Reddit-ingestion entry. |
| 5 | Landing page, email list, distribution list; confirm Finnhub/Supabase/Claude access; finalize RSS feeds | **Done.** Landing page + email capture: live and verified end-to-end. Distribution list: finalized (`m0/distribution-list.md`). RSS feeds: finalized (`m0/rss-feeds.md`). Claude access: already satisfied. Supabase: project created, publishable key, secret key, Postgres password, and project URL all saved (no schema needed yet — that's M1). Finnhub: API key confirmed working for US tickers; non-US exchange quotes confirmed unavailable on the free tier (see Known Technical Debt) — this is a resolved finding, not a blocker to closing this task. |
| 6 | Scaffold the remaining repo pieces (`jobs/`, GitHub Actions, initial migration) | Not started |
| 7 | RSS ingestion connector + dedupe + ticker extraction | Not started |
| 8 | Start `prices/` job | Not started |
| 9 | Topic synthesizer + thesis generator (structured output, golden-set check) | Not started |
| 10 | Open first positions, start `performance_snapshots`, build public pages + email | Not started |

**M0 gate:** the quality half can be read and is met on the thresholds in `m0/prolific-study-spec.md` §5 (round 2, 2026-10-13, three of four at the limit); the demand half is not tested, because the free-reader channels have produced no signal yet (on 2026-10-21: no comment on the r/SecurityAnalysis post, no reply on X or from the 2 outreach contacts, 0 subscribers; no further free channel is planned); the review of the intervention log is still to do. Verdict proposed for 2026-11-07; how it is worded when a half has no valid signal: `m0/round-2-channels.md` §4.1.

## Pending milestones

| Milestone | One-line scope |
|---|---|
| M1 | Ingestion + the clock — RSS connectors, price snapshots, schema migration |
| M2 | Pipeline + first positions — topic/thesis generation, no UI |
| M3 | Publication v1 — public pages, weekly email, first subscribers |
| M4 | Surface the record — performance charts, public track record |
| M5 | Dashboard and retention — interactive layer, auth, retention gate |
| M6 | Scale carefully — additional sources, monetization (with counsel) |

Full deliverables and gates: `docs/ROADMAP.md`.

## Implemented ADRs

| ADR | Formal status | Functional status |
|---|---|---|
| ADR-0001 | `Accepted` (2026-07-25) | Fully reflected across the repository — every scope, architecture, and sequencing decision it made is already how the project is described and run |
| ADR-0002 | `Accepted` (2026-07-25) | Fully reflected — the free-tier-first execution mode is already how `docs/AI_SYSTEM.md`, `docs/ARCHITECTURE.md`, `docs/TECH_STACK.md`, and `docs/MVP_SCOPE.md` describe the project |
| ADR-0003 | `Accepted` (2026-07-30) | Partially reflected — write-ups 8, 9, 11, 12, and 13 (`m0/`) follow the new ten-section thesis structure; write-ups 1-7 remain on the old format (backfill optional); `docs/AI_SYSTEM.md`'s Agent 3 output contract still needs updating to match before any pipeline work begins (M2), flagged in the ADR itself, not yet done |

Next ID if a new ADR is drafted: **ADR-0004** (decision registry continues at **D-34** — `DECISIONS.md` §3).

## Known technical debt

The only application code so far is the M0 landing page, live and verified. What remains open:

| Item | Status |
|---|---|
| Branch protection on `main` not yet configured, per `CONTRIBUTING.md` §1 | Open, deliberately deferred — `CONTRIBUTING.md`'s PR/CI discipline formally applies "from M1's first scaffolding commit onward," so this isn't overdue, but worth configuring before M1's first scaffolding commit |
| `AGENTS.md` §6/§7 and `CLAUDE.md` still describe `suggested_basket` as naive equal-weight and refuse a "conviction-weighted" one, while ADR-0003 D-32 requires weights to follow a thesis's stated conviction (write-ups 8, 9, 12, and 13 do) | Open. Per `AGENTS.md` §2 the ADR wins, but §6 makes any change to `suggested_basket` wording a founder decision; align the process files before M2 and before any weighted basket is shown as a `suggested_basket` |
| Finnhub free tier does not cover quotes for non-US exchanges | **Confirmed and documented** — tested directly on 2026-07-28: `AAPL` returns real data; `RHM.DE`, `BA.L`, `HO.PA`, and `LDO.MI` all return an access-denied error on the same key. `docs/TECH_STACK.md`'s Finnhub entry now states this explicitly; new write-ups default to US-listed companies/ADRs unless a deliberate paid-tier decision is made. |

## Deferred features

Full lists with reinstatement triggers: `docs/MVP_SCOPE.md`, `docs/TECH_STACK.md`. None of these triggers have fired:

Reddit ingestion · the automated, metered Claude API pipeline · a deployed backend service (FastAPI) · Celery/Redis · `pgvector` · auth and login · the interactive dashboard · watchlists · user-editable portfolios · additional data sources beyond curated RSS · paid market data (Massive.com).

## Current priorities

1. **Get a demand signal from readers who read for free** (task 3, second half) — the quality half has its careful reads; "would you miss this" can only come from X, outreach and the r/SecurityAnalysis post (live since 2026-10-16). All three were at zero on 2026-10-21 and no further free channel is planned. Without a signal, the gate records the demand half as "not tested" (`m0/round-2-channels.md` §4.1).
2. Continuing write-ups toward 20 remains available but is now optional, not required.
3. Reddit API application: closed (rejected 2026-08-05). No action needed — see task 1 above.

## Next actions

1. Replies to the follow-ups sent on 2026-10-21, if any, are logged as they come (`m0/reader-feedback-log.md`); no further outreach messages and no further candidate search.
2. The r/SecurityAnalysis post is live (no comments as of 2026-10-21): answer any comment on substance without links and log it anonymously (`m0/topic-thesis-13-distribution-copy.md` §1.1).
3. **Mon 2026-10-26 and Wed 2026-10-28:** Verizon and T-Mobile Q3 reports against the invalidation conditions of thesis 13 (`m0/topic-thesis-13-us-wireless-spacex.md`). AT&T reported on 2026-10-21 and neither condition is triggered for AT&T (guidance "$18 billion or more"; postpaid phone net additions +379,000). A dated X post follows each report, in the same format as the AT&T post (facts only, hypothesis unchanged).
4. **Mon 2026-10-26.** M0 gate verdict into this file (brought forward from 2026-11-07 by the founder on 2026-10-21), including the intervention-log review (reading accepted on 2026-10-21 and recorded with the verdict: `m0/intervention-log-review.md`) and the demand half. No further free channel is planned, so no new demand data is expected beyond late replies. ADR-0004 is drafted (Proposed, `docs/ADR/ADR-0004-m1-start-with-untested-demand.md`) and the founder accepts, changes or rejects it at the verdict. If the demand half is untested, whether M1 may start is a founder decision (`AGENTS.md` §6) and is recorded in it, with the condition that would stop the project before M2.
5. **Founder decisions open.** (a) Whether third-party precedent examples are allowed in write-ups under ADR-0001 D-02 and `AGENTS.md` §7: a reader asked for them (`m0/reader-feedback-log.md`, Round 2). (b) The `AGENTS.md` / `CLAUDE.md` wording against ADR-0003 D-32 (Known technical debt). (c) The open points of the Proposed ADR-0004: whether M1a starts before the checkpoint, M1a only or all of M1, the checkpoint date and rule, and the primary-source step for M2 (D-35; `m0/intervention-log-review.md` §7).
6. Optional: continue writing toward the 20-write-up ceiling, carrying the bear-case checklist from `m0/reader-feedback-log.md`; or add a one-line cross-reference from `docs/RISKS.md`/`docs/MVP_SCOPE.md` to `m0/earliness-log.md`'s searchability finding.

## How to keep this file current

- Update **Completed / Active / Pending milestones** at every gate, in the same sitting the gate is evaluated (`CONTRIBUTING.md` §8) — not as a later cleanup pass.
- Update **Implemented ADRs** whenever one is drafted, accepted, or superseded (`DECISIONS.md`).
- Update **Known technical debt** whenever something is fixed or newly discovered — delete a resolved line rather than leaving it marked done; a long resolved list isn't more informative than a short honest one.
- Update the **Last updated** line every time this file changes, even for a small edit. It is also the freshness marker for the Claude Project's copy of the repo: after committing, re-sync the Claude Project (`CONTRIBUTING.md` §11) — GitHub `main` is the source of truth, the Project only holds a cache — and a stale "Last updated" on the Claude side means the sync hasn't run.
- Keep entries short and dated, and point back to the document with the actual reasoning — if an entry needs more than two sentences to justify itself, that explanation belongs in the document it's citing, not here.

---

If anything here ever conflicts with `docs/ROADMAP.md`, `docs/MVP_SCOPE.md`, or an ADR, those are canonical — this file is the fast summary, not a new source of truth (`AGENTS.md` §2).
