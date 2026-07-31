# PROJECT_STATE.md

*The single, live answer to "where is this project right now" — for the founder and for any AI assistant starting a session cold. Update this whenever a milestone gate passes, an ADR's status changes, a deferred trigger fires, or a priority shifts (`AGENTS.md` §8's docs-sync discipline applies to this file at least as much as any other document). Last updated: 2026-07-31 — Task 3 round 1 concluded: 3 of 5 personal-network readers responded, but all three self-reported skimming rather than reading carefully, so the M0 gate question remains unresolved. 2 of 3 flagged the pieces as too long — plausibly why they skimmed. Recommendation: round 2 via self-selected channels (Reddit, Show HN) rather than more personal-network asks; consider testing a shorter write-up variant.*

## Current phase

Pre-build for the real application (jobs/, Supabase schema, ingestion) — M0 concierge test in progress. Planning, architecture, and repository-governance documentation are complete. The repository holds `docs/*.md`, `docs/ADR/ADR-0001`, `ADR-0002`, and `ADR-0003`, the six process files this earlier phase of work produced (`AGENTS.md`, `CLAUDE.md`, `CURSOR_RULES.md`, `DECISIONS.md`, `CONTRIBUTING.md`, this file), `m0/` — ten hand-written topic-and-thesis write-ups, a running intervention log, a finalized distribution list, and a finalized RSS feed list — and `app/`, a live Next.js landing page with a Resend-backed `/api/subscribe` route at topicron.vercel.app.

Worth saying plainly, since accuracy is this file's entire job: everything built so far, including the ten write-ups now in `m0/`, is still validating the core hypothesis, not building the product itself. Topicron's actual core hypothesis — whether a target-persona reader finds a hand-written thesis genuinely useful — is now testable in principle, but hasn't been tested yet: no target-persona reader has seen any write-up.

## Completed milestones

None. M0 is the first milestone in `docs/ROADMAP.md` and is in progress (see below).

## Active milestone

**M0 — Validate the writing.** Status against `docs/ROADMAP.md`'s "First 10 tasks":

| # | Task | Status |
|---|---|---|
| 1 | File the Reddit API developer application | **Submitted 2026-07-31, awaiting response.** Filed via the actual current process (a support ticket through the Reddit Data API Wiki's contact form, not the old self-service reddit.com/prefs/apps flow — see `docs/TECH_STACK.md`, Deferred). Automated "we received your request" confirmation received; no ticket number captured. Per Reddit's own published pattern, expect a multi-week wait, and a real chance of no response or a generic rejection even for a well-scoped request. Nothing further to do until a response arrives. |
| 2 | Hand-write 10–20 topic-and-thesis write-ups, with an intervention log | **12 of 10–20 done**, spanning 10 distinct sectors (`m0/topic-thesis-01` through `12`). Write-ups 8, 9, 11, and 12 follow the ADR-0003 ten-section template — 11 and 12 drafted natively under it, not rewrites. Write-ups 1–7 remain on the original five-section format; backfilling them is optional, not required. Intervention log live and current at `m0/intervention-log.md`. |
| 3 | Write down the primary persona; share write-ups with 5–10 target-persona readers | **Round 1 concluded, inconclusive.** Persona done (`docs/VISION.md`, `README.md`). 3 of 5 personal-network readers responded (`m0/reader-feedback-log.md`); founder doesn't expect more from this batch. All 3 self-reported skimming rather than reading carefully, so the round doesn't resolve the gate question either way — though 2 of 3 flagged the pieces as too long, plausibly the reason they skimmed rather than read. Recommendation: round 2 via `m0/distribution-list.md`'s self-selected channels (Reddit, Show HN) instead of further personal-network asks. |
| 4 | Read relevant subreddits by hand; log earliness vs. curated RSS | **Done, with a finding rather than a clean number.** Two separate attempts (manual sorted search, then a broader scrape across four phrases) found Reddit's native search unreliable for narrow financial narratives — including one search term ("Huntington Bancshares") that returned only an unrelated same-named company (Huntington Ingalls Industries), zero real matches. Documented in `m0/earliness-log.md`, with a recommendation to cross-reference it from `docs/RISKS.md` or `docs/MVP_SCOPE.md`'s Reddit-ingestion entry. |
| 5 | Landing page, email list, distribution list; confirm Finnhub/Supabase/Claude access; finalize RSS feeds | **Done.** Landing page + email capture: live and verified end-to-end. Distribution list: finalized (`m0/distribution-list.md`). RSS feeds: finalized (`m0/rss-feeds.md`). Claude access: already satisfied. Supabase: project created, publishable key, secret key, Postgres password, and project URL all saved (no schema needed yet — that's M1). Finnhub: API key confirmed working for US tickers; non-US exchange quotes confirmed unavailable on the free tier (see Known Technical Debt) — this is a resolved finding, not a blocker to closing this task. |
| 6 | Scaffold the remaining repo pieces (`jobs/`, GitHub Actions, initial migration) | Not started |
| 7 | RSS ingestion connector + dedupe + ticker extraction | Not started |
| 8 | Start `prices/` job | Not started |
| 9 | Topic synthesizer + thesis generator (structured output, golden-set check) | Not started |
| 10 | Open first positions, start `performance_snapshots`, build public pages + email | Not started |

**M0 gate:** not evaluable yet — write-ups exist and the landing page is live, but no target-persona reader has seen any write-up yet.

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
| ADR-0003 | `Accepted` (2026-07-30) | Partially reflected — write-ups 8 and 9 (`m0/`) follow the new ten-section thesis structure; write-ups 1-7 remain on the old format (backfill optional); `docs/AI_SYSTEM.md`'s Agent 3 output contract still needs updating to match before any pipeline work begins (M2), flagged in the ADR itself, not yet done |

Next ID if a new ADR is drafted: **ADR-0004** (decision registry continues at **D-34** — `DECISIONS.md` §3).

## Known technical debt

The only application code so far is the M0 landing page, live and verified. What remains open:

| Item | Status |
|---|---|
| Branch protection on `main` not yet configured, per `CONTRIBUTING.md` §1 | Open, deliberately deferred — `CONTRIBUTING.md`'s PR/CI discipline formally applies "from M1's first scaffolding commit onward," so this isn't overdue, but worth configuring before M1's first scaffolding commit |
| Finnhub free tier does not cover quotes for non-US exchanges | **Confirmed and documented** — tested directly on 2026-07-28: `AAPL` returns real data; `RHM.DE`, `BA.L`, `HO.PA`, and `LDO.MI` all return an access-denied error on the same key. `docs/TECH_STACK.md`'s Finnhub entry now states this explicitly; new write-ups default to US-listed companies/ADRs unless a deliberate paid-tier decision is made. |
| `.cursor/rules/general.mdc` likely still says "Never violate ADR-0001 or ADR-0002. Both are frozen" | Open — this file isn't in Claude's accessible project files (only the `docs/`-mirrored `.md` files are), so it couldn't be checked or fixed as part of the 2026-07-30 ADR-consistency audit that fixed the equivalent text in `CURSOR_RULES.md`, `AGENTS.md`, `README.md`, and `DECISIONS.md`. Needs a manual one-line fix: add "or ADR-0003" / "All three." |

## Deferred features

Full lists with reinstatement triggers: `docs/MVP_SCOPE.md`, `docs/TECH_STACK.md`. None of these triggers have fired:

Reddit ingestion · the automated, metered Claude API pipeline · a deployed backend service (FastAPI) · Celery/Redis · `pgvector` · auth and login · the interactive dashboard · watchlists · user-editable portfolios · additional data sources beyond curated RSS · paid market data (Massive.com).

## Current priorities

1. **Recruit 5–10 target-persona readers and share the write-ups** (task 3) — 10 write-ups across 8 sectors is now a presentable set; this remains the main open item standing between here and the M0 gate. (AI-model feedback on write-ups 8/9, used to inform ADR-0003, is not a substitute for this — no target-persona reader has seen any write-up yet.)
2. Continuing write-ups toward 20 remains available but is now optional, not required.
3. Reddit API: submitted, nothing to do but wait — check back periodically, don't block other work on it.

## Next actions

1. Recruit 5–10 target-persona readers via `m0/distribution-list.md` and share 1–2 write-ups (not all ten at once), asking for honest reactions rather than upvotes.
2. Once reader feedback comes in: run the M0 gate (`docs/RISKS.md`'s "how would you feel if this no longer existed" question, plus the intervention-log review) before writing any pipeline code.
3. Optional: continue writing toward the 20-write-up ceiling, or add a one-line cross-reference from `docs/RISKS.md`/`docs/MVP_SCOPE.md` to `m0/earliness-log.md`'s searchability finding.

## How to keep this file current

- Update **Completed / Active / Pending milestones** at every gate, in the same sitting the gate is evaluated (`CONTRIBUTING.md` §8) — not as a later cleanup pass.
- Update **Implemented ADRs** whenever one is drafted, accepted, or superseded (`DECISIONS.md`).
- Update **Known technical debt** whenever something is fixed or newly discovered — delete a resolved line rather than leaving it marked done; a long resolved list isn't more informative than a short honest one.
- Update the **Last updated** line every time this file changes, even for a small edit.
- Keep entries short and dated, and point back to the document with the actual reasoning — if an entry needs more than two sentences to justify itself, that explanation belongs in the document it's citing, not here.

---

If anything here ever conflicts with `docs/ROADMAP.md`, `docs/MVP_SCOPE.md`, or an ADR, those are canonical — this file is the fast summary, not a new source of truth (`AGENTS.md` §2).
