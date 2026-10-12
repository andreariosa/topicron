# PROJECT_STATE.md

*The single, live answer to "where is this project right now" — for the founder and for any AI assistant starting a session cold. Update this whenever a milestone gate passes, an ADR's status changes, a deferred trigger fires, or a priority shifts (`AGENTS.md` §8's docs-sync discipline applies to this file at least as much as any other document). Last updated: 2026-10-12 — Write-up 13 (US wireless carriers and the SpaceX spectrum deal, checked against primary sources and re-checked before the commit) added with its Reddit and X copy; subreddit rules recorded in `m0/round-2-channels.md`; X profile assets in `docs/brand/`. Task 3, the priorities and one debt row were re-checked; the other statuses are as of 2026-08-05 and were not re-checked. Earlier on 2026-10-10: consistency cleanup of counts and wording, and GitHub `main` documented as the single source of truth with a manual Claude Project re-sync after every commit (`CONTRIBUTING.md` §11, `AGENTS.md` §15).*

## Current phase

Pre-build for the real application (jobs/, Supabase schema, ingestion) — M0 concierge test in progress. Planning, architecture, and repository-governance documentation are complete. The repository holds `docs/*.md`, `docs/ADR/ADR-0001`, `ADR-0002`, and `ADR-0003`, the six process files this earlier phase of work produced (`AGENTS.md`, `CLAUDE.md`, `CURSOR_RULES.md`, `DECISIONS.md`, `CONTRIBUTING.md`, this file), `m0/` — thirteen hand-written topic-and-thesis write-ups (two also in Italian), the intervention log, the distribution and RSS feed lists, the earliness log, the reader questionnaire and feedback log, and the privacy-policy source text — and `app/`, a live Next.js landing page with a Resend-backed `/api/subscribe` route at topicron.vercel.app.

Worth saying plainly, since accuracy is this file's entire job: everything built so far, including the thirteen write-ups now in `m0/`, is still validating the core hypothesis, not building the product itself. Topicron's actual core hypothesis — whether a target-persona reader finds a hand-written thesis genuinely useful — is testable in principle but hasn't been tested yet: the only readers so far (round 1, personal network) all skimmed, which answers nothing either way.

## Completed milestones

None. M0 is the first milestone in `docs/ROADMAP.md` and is in progress (see below).

## Active milestone

**M0 — Validate the writing.** Status against `docs/ROADMAP.md`'s "First 10 tasks":

| # | Task | Status |
|---|---|---|
| 1 | File the Reddit API developer application | **Rejected, 2026-08-05.** Generic rejection ("not in compliance with Reddit's Responsible Builder Policy and/or lacks necessary details"), no specific deficiency given. Closed — reapplying without knowing what specifically fell short wouldn't have better odds, and the task 4 finding had already lowered the expected value of Reddit ingestion regardless. Reddit ingestion itself remains deferred per ADR-0001, D-10; this closes one path to it, not the underlying decision. |
| 2 | Hand-write 10–20 topic-and-thesis write-ups, with an intervention log | **13 of 10–20 done**, spanning 11 distinct sectors (`m0/topic-thesis-01` through `13`). Write-ups 8, 9, 11, 12, and 13 follow the ADR-0003 ten-section template — 11, 12, and 13 drafted natively under it, not rewrites. Write-ups 1–7 remain on the original five-section format; backfilling them is optional, not required. Intervention log live and current at `m0/intervention-log.md`. |
| 3 | Write down the primary persona; share write-ups with 5–10 target-persona readers | **Round 1 concluded, inconclusive; round 2 in progress (2026-10-11).** Persona done (`docs/VISION.md`, `README.md`). Round 1: 3 of 5 personal-network readers responded (`m0/reader-feedback-log.md`) and all 3 self-reported skimming; 2 of 3 flagged the pieces as too long. Round 2 (channels, verified rules, message drafts): `m0/round-2-channels.md`. Accounts: u/topicron on Reddit and @topicron on X (profile kit in `docs/brand/`). Reddit as of 2026-10-11: r/SecurityAnalysis is in restricted mode and takes posting requests through its Request to Post form; r/ValueInvesting blocks posting by an account-age check (u/topicron was 1 day old); r/stockpitches shows no rules and can be posted to directly; r/investing, r/StockMarket and r/ItaliaPersonalFinance are excluded (AI-text and self-promotion rules). The first post uses write-up 13 (`m0/topic-thesis-13-us-wireless-spacex.md`; Reddit and X copy in `m0/topic-thesis-13-distribution-copy.md`). No round-2 reader has responded yet. |
| 4 | Read relevant subreddits by hand; log earliness vs. curated RSS | **Done, with a finding rather than a clean number.** Two separate attempts (manual sorted search, then a broader scrape across four phrases) found Reddit's native search unreliable for narrow financial narratives — including one search term ("Huntington Bancshares") that returned only an unrelated same-named company (Huntington Ingalls Industries), zero real matches. Documented in `m0/earliness-log.md`, with a recommendation to cross-reference it from `docs/RISKS.md` or `docs/MVP_SCOPE.md`'s Reddit-ingestion entry. |
| 5 | Landing page, email list, distribution list; confirm Finnhub/Supabase/Claude access; finalize RSS feeds | **Done.** Landing page + email capture: live and verified end-to-end. Distribution list: finalized (`m0/distribution-list.md`). RSS feeds: finalized (`m0/rss-feeds.md`). Claude access: already satisfied. Supabase: project created, publishable key, secret key, Postgres password, and project URL all saved (no schema needed yet — that's M1). Finnhub: API key confirmed working for US tickers; non-US exchange quotes confirmed unavailable on the free tier (see Known Technical Debt) — this is a resolved finding, not a blocker to closing this task. |
| 6 | Scaffold the remaining repo pieces (`jobs/`, GitHub Actions, initial migration) | Not started |
| 7 | RSS ingestion connector + dedupe + ticker extraction | Not started |
| 8 | Start `prices/` job | Not started |
| 9 | Topic synthesizer + thesis generator (structured output, golden-set check) | Not started |
| 10 | Open first positions, start `performance_snapshots`, build public pages + email | Not started |

**M0 gate:** not evaluable yet — write-ups exist and the landing page is live, but the only reader feedback so far (round 1) came from three skimmers, which resolves nothing either way.

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

1. **Get careful reads from target-persona readers** (task 3) — 13 write-ups across 11 sectors is a presentable set; round 1 produced only skimmers and round 2 has just started, so this remains the main open item standing between here and the M0 gate. (AI-model feedback on write-ups 8/9, used to inform ADR-0003, is not a substitute for this.)
2. Continuing write-ups toward 20 remains available but is now optional, not required.
3. Reddit API application: closed (rejected 2026-08-05). No action needed — see task 1 above.

## Next actions

1. Round 2: commit write-up 13, send the r/SecurityAnalysis Request to Post, post in r/stockpitches, schedule the X thread (`m0/topic-thesis-13-distribution-copy.md`), then read the replies. The paid reader panel (Prolific, `m0/round-2-channels.md` §2) is the founder's decision and needs an explicit yes (`AGENTS.md` §6). Gate verdict proposed for 2026-11-07.
2. Once reader feedback comes in: run the M0 gate (`docs/RISKS.md`'s "how would you feel if this no longer existed" question, plus the intervention-log review) before writing any pipeline code.
3. Optional: continue writing toward the 20-write-up ceiling, or add a one-line cross-reference from `docs/RISKS.md`/`docs/MVP_SCOPE.md` to `m0/earliness-log.md`'s searchability finding.

## How to keep this file current

- Update **Completed / Active / Pending milestones** at every gate, in the same sitting the gate is evaluated (`CONTRIBUTING.md` §8) — not as a later cleanup pass.
- Update **Implemented ADRs** whenever one is drafted, accepted, or superseded (`DECISIONS.md`).
- Update **Known technical debt** whenever something is fixed or newly discovered — delete a resolved line rather than leaving it marked done; a long resolved list isn't more informative than a short honest one.
- Update the **Last updated** line every time this file changes, even for a small edit. It is also the freshness marker for the Claude Project's copy of the repo: after committing, re-sync the Claude Project (`CONTRIBUTING.md` §11) — GitHub `main` is the source of truth, the Project only holds a cache — and a stale "Last updated" on the Claude side means the sync hasn't run.
- Keep entries short and dated, and point back to the document with the actual reasoning — if an entry needs more than two sentences to justify itself, that explanation belongs in the document it's citing, not here.

---

If anything here ever conflicts with `docs/ROADMAP.md`, `docs/MVP_SCOPE.md`, or an ADR, those are canonical — this file is the fast summary, not a new source of truth (`AGENTS.md` §2).
