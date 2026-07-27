# PROJECT_STATE.md

*The single, live answer to "where is this project right now" — for the founder and for any AI assistant starting a session cold. Update this whenever a milestone gate passes, an ADR's status changes, a deferred trigger fires, or a priority shifts (`AGENTS.md` §8's docs-sync discipline applies to this file at least as much as any other document). Last updated: 2026-07-26 — M0 landing page + email-capture endpoint live in `app/`; M0 concierge-test write-ups started (2 of 10–20 done, intervention log live in `m0/`); branch protection on `main` deliberately deferred for now, not forgotten.*

## Current phase

Pre-build for application code; M0 concierge test in progress. Planning, architecture, and repository-governance documentation are complete. The repository holds `docs/*.md`, `docs/ADR/ADR-0001` and `ADR-0002`, the six process files this earlier phase of work produced (`AGENTS.md`, `CLAUDE.md`, `CURSOR_RULES.md`, `DECISIONS.md`, `CONTRIBUTING.md`, this file), and now `m0/` — the first hand-written topic-and-thesis write-ups plus a running intervention log. No application code exists yet.

Worth saying plainly, since accuracy is this file's entire job: everything built so far, including the two write-ups now in `m0/`, is still validating the core hypothesis, not building the product itself. Topicron's actual core hypothesis — whether a target-persona reader finds a hand-written thesis genuinely useful — is now testable in principle, but hasn't been tested yet: no target-persona reader has seen either write-up.

## Completed milestones

None. M0 is the first milestone in `docs/ROADMAP.md` and is in progress (see below).

## Active milestone

**M0 — Validate the writing.** Status against `docs/ROADMAP.md`'s "First 10 tasks":

| # | Task | Status |
|---|---|---|
| 1 | File the Reddit API developer application | Not started |
| 2 | Hand-write 10–20 topic-and-thesis write-ups, with an intervention log | **In progress** — 2 of 10–20 done (`m0/topic-thesis-01-ai-power-utilities.md`, `m0/topic-thesis-02-glp1-duopoly.md`); intervention log live at `m0/intervention-log.md` |
| 3 | Write down the primary persona; share write-ups with 5–10 target-persona readers | **Persona done** (`docs/VISION.md`, `README.md`) — sharing not yet started, depends on task 2 progressing further |
| 4 | Read relevant subreddits by hand; log earliness vs. curated RSS | Not started |
| 5 | Landing page, email list, distribution list; confirm Finnhub/Supabase/Claude access; finalize RSS feeds | **In progress** — landing page + email-capture endpoint live (`app/page.tsx`, `app/api/subscribe/route.ts`); distribution list and Finnhub/Supabase/Claude access confirmation still open |
| 6 | Scaffold the repo (Next.js/Vercel, `jobs/`, GitHub Actions, initial migration) | Not started |
| 7 | RSS ingestion connector + dedupe + ticker extraction | Not started |
| 8 | Start `prices/` job | Not started |
| 9 | Topic synthesizer + thesis generator (structured output, golden-set check) | Not started |
| 10 | Open first positions, start `performance_snapshots`, build public pages + email | Not started |

**M0 gate:** not evaluable yet — write-ups exist but haven't been shown to target-persona readers.

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

No application code exists yet, so there's no code-level debt. All six governance files are written, `CURSOR_RULES.md` is live as `.cursor/rules/*.mdc`, and the documentation set is confirmed live and current on the public repo. What remains open:

| Item | Status |
|---|---|
| Branch protection on `main` not yet configured, per `CONTRIBUTING.md` §1 | Open, deliberately deferred for now — `CONTRIBUTING.md`'s PR/CI discipline formally applies "from M1's first scaffolding commit onward," so this isn't overdue, but it's worth configuring before M1's first scaffolding commit |
| Whether this governance-layer work should retroactively become ADR-0003 | Undecided, not urgent — per `DECISIONS.md` §2's own criteria (an ADR is needed for scope, architecture, gate, or decision changes), this is process documentation and likely doesn't need one |

## Deferred features

Full lists with reinstatement triggers: `docs/MVP_SCOPE.md`, `docs/TECH_STACK.md`. None of these triggers have fired:

Reddit ingestion · the automated, metered Claude API pipeline · a deployed backend service (FastAPI) · Celery/Redis · `pgvector` · auth and login · the interactive dashboard · watchlists · user-editable portfolios · additional data sources beyond curated RSS · paid market data (Massive.com).

## Current priorities

1. **Continue M0's core write-up work.** 2 of 10–20 topic-and-thesis write-ups are done (`m0/`); keep going, in parallel with (2), not before it.
2. **Start the parallel M0 tracks that carry their own calendar-time lag:** file the Reddit API developer application (free, 2–4 week approval lag); stand up the landing page, email list, and distribution list; begin reading relevant subreddits by hand for the earliness comparison. None of these depend on all 10–20 write-ups existing first.
3. Once 5–10 target-persona readers exist and 10–20 write-ups are done: run the M0 gate (`docs/RISKS.md`'s "how would you feel if this no longer existed" question, plus the intervention-log review) before writing any pipeline code.

## Next actions

1. Keep writing topic-and-thesis write-ups toward the 10–20 target, updating `m0/intervention-log.md` alongside each one.
2. File the Reddit API developer application — the one action whose delay compounds (2–4 week lag), worth doing today regardless of anything else in flight.
3. Stand up the landing page and email list; draft the distribution list (named communities/channels where the "informed generalist" persona actually spends time).
4. Read the relevant subreddits by hand in parallel, logging earliness vs. curated RSS.
5. Once enough write-ups and a distribution list exist: recruit 5–10 target-persona readers and run the M0 gate.

## How to keep this file current

- Update **Completed / Active / Pending milestones** at every gate, in the same sitting the gate is evaluated (`CONTRIBUTING.md` §8) — not as a later cleanup pass.
- Update **Implemented ADRs** whenever one is drafted, accepted, or superseded (`DECISIONS.md`).
- Update **Known technical debt** whenever something is fixed or newly discovered — delete a resolved line rather than leaving it marked done; a long resolved list isn't more informative than a short honest one.
- Update the **Last updated** line every time this file changes, even for a small edit.
- Keep entries short and dated, and point back to the document with the actual reasoning — if an entry needs more than two sentences to justify itself, that explanation belongs in the document it's citing, not here.

---

If anything here ever conflicts with `docs/ROADMAP.md`, `docs/MVP_SCOPE.md`, or an ADR, those are canonical — this file is the fast summary, not a new source of truth (`AGENTS.md` §2).
