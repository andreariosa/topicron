# PROJECT_STATE.md

*The single, live answer to "where is this project right now" — for the founder and for any AI assistant starting a session cold. Update this whenever a milestone gate passes, an ADR's status changes, a deferred trigger fires, or a priority shifts (`AGENTS.md` §8's docs-sync discipline applies to this file at least as much as any other document). Last updated: 2026-07-27 — M0 write-ups at 4 of 10–20 (~2/day pace); landing page + email-capture code built, reviewed, and pushed, Vercel deployment still pending; Reddit API application deliberately resequenced to after deployment (see task 1).*

## Current phase

Pre-build for the real application (jobs/, Supabase schema, ingestion) — M0 concierge test in progress. Planning, architecture, and repository-governance documentation are complete. The repository holds `docs/*.md`, `docs/ADR/ADR-0001` and `ADR-0002`, the six process files this earlier phase of work produced (`AGENTS.md`, `CLAUDE.md`, `CURSOR_RULES.md`, `DECISIONS.md`, `CONTRIBUTING.md`, this file), `m0/` — four hand-written topic-and-thesis write-ups plus a running intervention log — and a minimal `app/` (Next.js landing page + `/api/subscribe` Resend-backed email capture), built and pushed but not yet confirmed live on Vercel.

Worth saying plainly, since accuracy is this file's entire job: everything built so far, including the four write-ups now in `m0/`, is still validating the core hypothesis, not building the product itself. Topicron's actual core hypothesis — whether a target-persona reader finds a hand-written thesis genuinely useful — is now testable in principle, but hasn't been tested yet: no target-persona reader has seen any write-up.

## Completed milestones

None. M0 is the first milestone in `docs/ROADMAP.md` and is in progress (see below).

## Active milestone

**M0 — Validate the writing.** Status against `docs/ROADMAP.md`'s "First 10 tasks":

| # | Task | Status |
|---|---|---|
| 1 | File the Reddit API developer application | **Deliberately resequenced, not overdue.** Reddit tightened its approval process in late 2025 to favor established, commercial, or clearly-scoped applicants — filing today, as a pre-revenue project with no public site, risks rejection. Plan: file once the landing page is live, pointing to it for a stronger case. Task 4 (manual subreddit reading) does not depend on this and can proceed independently regardless of outcome or timing. |
| 2 | Hand-write 10–20 topic-and-thesis write-ups, with an intervention log | **In progress** — 4 of 10–20 done at roughly a 2/day working pace: AI power demand/utilities, GLP-1 capacity buildout, European defense rearmament, US manufacturing reshoring (`m0/topic-thesis-01` through `04`). Intervention log live and current at `m0/intervention-log.md`. |
| 3 | Write down the primary persona; share write-ups with 5–10 target-persona readers | **Persona done** (`docs/VISION.md`, `README.md`) — sharing not yet started, depends on task 2 and the distribution list progressing further |
| 4 | Read relevant subreddits by hand; log earliness vs. curated RSS | Not started — free to start any time, no dependency on task 1 |
| 5 | Landing page, email list, distribution list; confirm Finnhub/Supabase/Claude access; finalize RSS feeds | **In progress** — landing page + `/api/subscribe` (Resend, required segment, honeypot) built, reviewed, committed, and pushed to `main`; **Vercel deployment still pending** (next concrete action); distribution list first draft exists (not finalized); Finnhub/Supabase/Claude access confirmation and RSS feed finalization not started |
| 6 | Scaffold the remaining repo pieces (`jobs/`, GitHub Actions, initial migration) | Not started |
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

No core application code exists yet beyond the M0 landing page, so there's minimal code-level debt so far. What remains open:

| Item | Status |
|---|---|
| Branch protection on `main` not yet configured, per `CONTRIBUTING.md` §1 | Open, deliberately deferred — `CONTRIBUTING.md`'s PR/CI discipline formally applies "from M1's first scaffolding commit onward," so this isn't overdue, but worth configuring before M1's first scaffolding commit |
| Finnhub free-tier coverage of non-US exchanges (XETRA, LSE, Euronext, Borsa Italiana) is unverified | Open — surfaced while drafting `m0/topic-thesis-03-european-defense.md`. Marketing claims broad global coverage; independent reviews describe real-time depth as uneven outside US markets. Needs a direct API check before any thesis with non-US-listed constituents can actually be tracked in `price_snapshots` |
| Landing page built and pushed, but not confirmed live on Vercel | Open — code exists on `main`; deployment (import repo into a Vercel project, set `RESEND_API_KEY`/`RESEND_SEGMENT_ID` in Vercel's env settings) has not been done yet |
| Whether this governance-layer work should retroactively become ADR-0003 | Undecided, not urgent — per `DECISIONS.md` §2's own criteria (an ADR is needed for scope, architecture, gate, or decision changes), this is process documentation and likely doesn't need one |

## Deferred features

Full lists with reinstatement triggers: `docs/MVP_SCOPE.md`, `docs/TECH_STACK.md`. None of these triggers have fired:

Reddit ingestion · the automated, metered Claude API pipeline · a deployed backend service (FastAPI) · Celery/Redis · `pgvector` · auth and login · the interactive dashboard · watchlists · user-editable portfolios · additional data sources beyond curated RSS · paid market data (Massive.com).

## Current priorities

1. **Deploy the M0 landing page to Vercel.** The code has been built, reviewed, and pushed — it's providing zero real-world value (no possible email signups) until it's actually reachable.
2. **Continue M0's core write-up work** at the current ~2/day pace — 4 of 10–20 done.
3. **File the Reddit API developer application after (1) is live**, referencing the deployed site — Reddit's tightened approval process favors applicants who can point to something real, and this project couldn't before now.
4. Finalize the distribution list, confirm Finnhub/Supabase/Claude access, and finalize RSS feeds — the remaining pieces of task 5.
5. Once 5–10 target-persona readers exist and 10–20 write-ups are done: run the M0 gate (`docs/RISKS.md`'s "how would you feel if this no longer existed" question, plus the intervention-log review) before writing any pipeline code.

## Next actions

1. Deploy the landing page: create/connect the Vercel project, set `RESEND_API_KEY` and `RESEND_SEGMENT_ID` in Vercel's project settings, confirm the live form actually adds a contact.
2. Keep writing topic-and-thesis write-ups toward the 10–20 target at the current pace, updating `m0/intervention-log.md` alongside each one.
3. Once the landing page is live: file the Reddit API developer application, referencing it directly in the application's use-case description.
4. Read the relevant subreddits by hand in parallel — no dependency on (3), can start any time.
5. Finalize the distribution list draft; confirm Finnhub/Supabase/Claude access; finalize RSS feeds.
6. Once enough write-ups, a distribution list, and reachable readers exist: recruit 5–10 target-persona readers and run the M0 gate.

## How to keep this file current

- Update **Completed / Active / Pending milestones** at every gate, in the same sitting the gate is evaluated (`CONTRIBUTING.md` §8) — not as a later cleanup pass.
- Update **Implemented ADRs** whenever one is drafted, accepted, or superseded (`DECISIONS.md`).
- Update **Known technical debt** whenever something is fixed or newly discovered — delete a resolved line rather than leaving it marked done; a long resolved list isn't more informative than a short honest one.
- Update the **Last updated** line every time this file changes, even for a small edit.
- Keep entries short and dated, and point back to the document with the actual reasoning — if an entry needs more than two sentences to justify itself, that explanation belongs in the document it's citing, not here.

---

If anything here ever conflicts with `docs/ROADMAP.md`, `docs/MVP_SCOPE.md`, or an ADR, those are canonical — this file is the fast summary, not a new source of truth (`AGENTS.md` §2).
