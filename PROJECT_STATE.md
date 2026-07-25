# PROJECT_STATE.md

*The single, live answer to "where is this project right now" — for the founder and for any AI assistant starting a session cold. Update this whenever a milestone gate passes, an ADR's status changes, a deferred trigger fires, or a priority shifts (`AGENTS.md` §8's docs-sync discipline applies to this file at least as much as any other document). Last updated: 2026-07-25 — ADR-0001/ADR-0002 confirmed Accepted and `.cursor/rules/*.mdc` generated this session; see Known technical debt below for what's still open.*

## Current phase

Pre-build. Planning, architecture, and repository-governance documentation are complete; M0 hasn't started in substance. The repository holds `docs/*.md`, `docs/ADR/ADR-0001` and `ADR-0002`, and the six process files this phase of work produced (`AGENTS.md`, `CLAUDE.md`, `CURSOR_RULES.md`, `DECISIONS.md`, `CONTRIBUTING.md`, this file). No application code exists yet.

Worth saying plainly, since accuracy is this file's entire job: everything built so far is infrastructure for building the product, not the product itself. Topicron's actual core hypothesis — whether a target-persona reader finds a hand-written thesis genuinely useful — hasn't been tested. That test is M0, and M0 hasn't happened yet.

## Completed milestones

None. M0 is the first milestone in `docs/ROADMAP.md` and hasn't been substantively started (see below).

## Active milestone

**M0 — Validate the writing.** Status against `docs/ROADMAP.md`'s "First 10 tasks":

| # | Task | Status |
|---|---|---|
| 1 | File the Reddit API developer application | Not started |
| 2 | Hand-write 10–20 topic-and-thesis write-ups, with an intervention log | Not started |
| 3 | Write down the primary persona; share write-ups with 5–10 target-persona readers | **Persona done** (`docs/VISION.md`, `README.md`) — sharing depends on task 2 |
| 4 | Read relevant subreddits by hand; log earliness vs. curated RSS | Not started |
| 5 | Landing page, email list, distribution list; confirm Finnhub/Supabase/Claude access; finalize RSS feeds | Not started |
| 6 | Scaffold the repo (Next.js/Vercel, `jobs/`, GitHub Actions, initial migration) | Not started |
| 7 | RSS ingestion connector + dedupe + ticker extraction | Not started |
| 8 | Start `prices/` job | Not started |
| 9 | Topic synthesizer + thesis generator (structured output, golden-set check) | Not started |
| 10 | Open first positions, start `performance_snapshots`, build public pages + email | Not started |

**M0 gate:** not evaluable yet — there are no write-ups to show target-persona readers.

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

No application code exists yet, so there's no code-level debt. All six governance files are written, and `CURSOR_RULES.md` is now also live as `.cursor/rules/*.mdc` (`general`, `python-jobs`, `frontend`, `testing`). What remains open:

| Item | Status |
|---|---|
| Live GitHub repo predates ADR-0002 — pushed `README.md` doesn't mention it, and its ADR link path doesn't match `docs/ADR/` | Open — the founder needs to push the current doc set; no tool in this session has git/network access to do it directly |
| Branch protection on `main` not yet configured, per `CONTRIBUTING.md` §1 | Open — only one commit exists so far |
| Whether this governance-layer work should retroactively become ADR-0003 | Undecided, not urgent |

## Deferred features

Full lists with reinstatement triggers: `docs/MVP_SCOPE.md`, `docs/TECH_STACK.md`. None of these triggers have fired:

Reddit ingestion · the automated, metered Claude API pipeline · a deployed backend service (FastAPI) · Celery/Redis · `pgvector` · auth and login · the interactive dashboard · watchlists · user-editable portfolios · additional data sources beyond curated RSS · paid market data (Massive.com).

## Current priorities

1. **Push the current documentation set to the live repository** (the one remaining gap in Known technical debt) — everything else this session flagged is already resolved.
2. **Start M0 for real.** Governance and architecture are no longer the bottleneck — zero topic-and-thesis write-ups exist, and the entire product bet is untested until target-persona readers see some. This is the priority, not a formality that comes after the "real" work: `docs/RISKS.md` and `docs/ROADMAP.md` both say a failed M0 gate should stop the project before a line of pipeline code gets written.
3. Everything else in `docs/ROADMAP.md`'s First 10 tasks can run alongside (2) — filing the Reddit application and standing up the landing page don't depend on the write-ups existing first.

## Next actions

1. Push the current documentation set to `main` so the live repo matches what this session's work was built against.
2. Hand-write the first topic-and-thesis write-up, with the intervention log started alongside it (`docs/ROADMAP.md`, M0, task 2) — the single highest-value next unit of work.
3. In parallel: file the Reddit API application; stand up the landing page and email list; draft the distribution list.
4. Once 5–10 target-persona readers exist and 10–20 write-ups are done: run the M0 gate (`docs/RISKS.md`'s "how would you feel if this no longer existed" question, plus the intervention-log review) before writing any pipeline code.

## How to keep this file current

- Update **Completed / Active / Pending milestones** at every gate, in the same sitting the gate is evaluated (`CONTRIBUTING.md` §8) — not as a later cleanup pass.
- Update **Implemented ADRs** whenever one is drafted, accepted, or superseded (`DECISIONS.md`).
- Update **Known technical debt** whenever something is fixed or newly discovered — delete a resolved line rather than leaving it marked done; a long resolved list isn't more informative than a short honest one.
- Update the **Last updated** line every time this file changes, even for a small edit.
- Keep entries short and dated, and point back to the document with the actual reasoning — if an entry needs more than two sentences to justify itself, that explanation belongs in the document it's citing, not here.

---

If anything here ever conflicts with `docs/ROADMAP.md`, `docs/MVP_SCOPE.md`, or an ADR, those are canonical — this file is the fast summary, not a new source of truth (`AGENTS.md` §2).
