# PROJECT_STATE.md

*The single, live answer to "where is this project right now" — for the founder and for any AI assistant starting a session cold. Update this whenever a milestone gate passes, an ADR's status changes, a deferred trigger fires, or a priority shifts (`AGENTS.md` §8's docs-sync discipline applies to this file at least as much as any other document). Last updated: 2026-07-30 — Task 4 of M0 is done: two independent attempts at a Reddit-vs-mainstream earliness comparison instead surfaced a finding about Reddit's search reliability for narrow financial narratives (`m0/earliness-log.md`). Task 5 remains fully complete (see below). Only task 1 (Reddit API application) and continuing task 2 (write-ups, 6 of 10-20) are still open before the M0 gate becomes evaluable.*

## Current phase

Pre-build for the real application (jobs/, Supabase schema, ingestion) — M0 concierge test in progress. Planning, architecture, and repository-governance documentation are complete. The repository holds `docs/*.md`, `docs/ADR/ADR-0001` and `ADR-0002`, the six process files this earlier phase of work produced (`AGENTS.md`, `CLAUDE.md`, `CURSOR_RULES.md`, `DECISIONS.md`, `CONTRIBUTING.md`, this file), `m0/` — six hand-written topic-and-thesis write-ups, a running intervention log, a finalized distribution list, and a finalized RSS feed list — and `app/`, a live Next.js landing page with a Resend-backed `/api/subscribe` route at topicron.vercel.app.

Worth saying plainly, since accuracy is this file's entire job: everything built so far, including the six write-ups now in `m0/`, is still validating the core hypothesis, not building the product itself. Topicron's actual core hypothesis — whether a target-persona reader finds a hand-written thesis genuinely useful — is now testable in principle, but hasn't been tested yet: no target-persona reader has seen any write-up.

## Completed milestones

None. M0 is the first milestone in `docs/ROADMAP.md` and is in progress (see below).

## Active milestone

**M0 — Validate the writing.** Status against `docs/ROADMAP.md`'s "First 10 tasks":

| # | Task | Status |
|---|---|---|
| 1 | File the Reddit API developer application | Ready to file (landing page is live); not yet filed |
| 2 | Hand-write 10–20 topic-and-thesis write-ups, with an intervention log | **In progress** — 6 of 10–20 done: AI power demand/utilities, GLP-1 capacity buildout, European defense rearmament, US manufacturing reshoring, memory chip supercycle, regional banks (`m0/topic-thesis-01` through `06`). Intervention log live and current at `m0/intervention-log.md`. |
| 3 | Write down the primary persona; share write-ups with 5–10 target-persona readers | **Persona done** (`docs/VISION.md`, `README.md`) — sharing not yet started, depends on task 2 progressing further |
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

Next ID if a new ADR is drafted: **ADR-0003** (decision registry continues at **D-25** — `DECISIONS.md` §3).

## Known technical debt

The only application code so far is the M0 landing page, live and verified. What remains open:

| Item | Status |
|---|---|
| Branch protection on `main` not yet configured, per `CONTRIBUTING.md` §1 | Open, deliberately deferred — `CONTRIBUTING.md`'s PR/CI discipline formally applies "from M1's first scaffolding commit onward," so this isn't overdue, but worth configuring before M1's first scaffolding commit |
| Finnhub free tier does not cover quotes for non-US exchanges | **Confirmed, not just suspected** — tested directly on 2026-07-28: `AAPL` returns real data; `RHM.DE` (XETRA), `BA.L` (LSE), `HO.PA` (Euronext Paris), and `LDO.MI` (Borsa Italiana) all return an access-denied error on the same key. This is a real scope constraint going forward, not an open question: new write-ups should default to US-listed companies or US-listed ADRs unless a deliberate decision is made to pay for expanded Finnhub coverage (or another data source) — worth a one-line addition to `docs/TECH_STACK.md`'s Finnhub entry so this constraint is visible where the vendor choice itself is documented, not just here. |
| Whether this governance-layer work should retroactively become ADR-0003 | Undecided, not urgent — per `DECISIONS.md` §2's own criteria (an ADR is needed for scope, architecture, gate, or decision changes), this is process documentation and likely doesn't need one |

## Deferred features

Full lists with reinstatement triggers: `docs/MVP_SCOPE.md`, `docs/TECH_STACK.md`. None of these triggers have fired:

Reddit ingestion · the automated, metered Claude API pipeline · a deployed backend service (FastAPI) · Celery/Redis · `pgvector` · auth and login · the interactive dashboard · watchlists · user-editable portfolios · additional data sources beyond curated RSS · paid market data (Massive.com).

## Current priorities

1. **File the Reddit API developer application**, referencing the live site — the only fully unblocked task with its own calendar-time lag left untouched, and now the single most overdue item on the board.
2. **Continue M0's core write-up work** — 6 of 10–20 done. Default to US-listed companies/ADRs given the confirmed Finnhub constraint above.
3. Once 5–10 target-persona readers exist and 10–20 write-ups are done: run the M0 gate (`docs/RISKS.md`'s "how would you feel if this no longer existed" question, plus the intervention-log review) before writing any pipeline code.

## Next actions

1. File the Reddit API developer application, referencing topicron.vercel.app directly in the use-case description.
2. Keep writing topic-and-thesis write-ups toward the 10–20 target (US-listed/ADR companies going forward), updating `m0/intervention-log.md` alongside each one.
3. Once enough write-ups and reachable readers exist: recruit 5–10 target-persona readers (via `m0/distribution-list.md`) and run the M0 gate.
4. Optional, low-priority: add a one-line cross-reference from `docs/RISKS.md` or `docs/MVP_SCOPE.md`'s Reddit-ingestion entry to `m0/earliness-log.md`'s searchability finding.

## How to keep this file current

- Update **Completed / Active / Pending milestones** at every gate, in the same sitting the gate is evaluated (`CONTRIBUTING.md` §8) — not as a later cleanup pass.
- Update **Implemented ADRs** whenever one is drafted, accepted, or superseded (`DECISIONS.md`).
- Update **Known technical debt** whenever something is fixed or newly discovered — delete a resolved line rather than leaving it marked done; a long resolved list isn't more informative than a short honest one.
- Update the **Last updated** line every time this file changes, even for a small edit.
- Keep entries short and dated, and point back to the document with the actual reasoning — if an entry needs more than two sentences to justify itself, that explanation belongs in the document it's citing, not here.

---

If anything here ever conflicts with `docs/ROADMAP.md`, `docs/MVP_SCOPE.md`, or an ADR, those are canonical — this file is the fast summary, not a new source of truth (`AGENTS.md` §2).
