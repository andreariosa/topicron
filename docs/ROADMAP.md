# Roadmap

*This document implements ADR-0001, Part 2 ("Updated roadmap") in full — a complete rewrite of the original milestone sequence. Deferred-item triggers are in [`MVP_SCOPE.md`](MVP_SCOPE.md); the validation methodology behind each gate, including the north-star metric's denominator problem, is in [`RISKS.md`](RISKS.md). Decisions are cited inline as "ADR-0001, D-XX."*

## Milestones

Two tracks, deliberately kept separate: **build weeks** are estimable, the way any engineering task is; **quality gates** are not, and any one of them is allowed to stop the project rather than just delay it (ADR-0001, D-08; `docs/VISION.md`, MVP philosophy #2).

| Milestone | Build weeks | Deliverables | Gate to pass |
|---|---|---|---|
| **M0 — Validate the writing** | 2–3 | 10–20 hand-written topic+thesis write-ups; intervention log; primary persona defined; landing page + email list live; distribution list of named communities; Reddit-vs-RSS earliness comparison; Reddit API application filed; cost model estimated | Do target-persona readers find the write-ups genuinely useful, and is the intervention delta small enough that a pipeline could plausibly close it? |
| **M1 — Ingestion + the clock** | 2 | RSS connectors (10–15 feeds), dedupe, ticker extraction, `price_snapshots` ingestion, schema migration, cron on GitHub Actions | Is content flowing cleanly, and is price history accumulating daily without gaps across weekends and holidays? |
| **M2 — Pipeline + first positions** | 3–4 | Topic synthesis with continuity resolution, thesis generation with citations, structured-output validation, golden-set regression check, first system positions opened under the 90-day rule, daily `performance_snapshots` job. **No UI.** | Does automated output hold the M0 quality bar, judged against the same rubric by the same readers? *Highest-risk gate in the plan.* |
| **M3 — Publication v1** | 2 | Public, indexable topic/thesis pages; weekly email; PostHog instrumentation; first 100+ subscribers via the M0 distribution list | Do people open, read, return, and share — measured over at least four issues? |
| **M4 — Surface the record** | 1 | Performance charts against dual benchmarks; public track-record page including losers; closed-position retrospectives | Does visible accountability measurably change engagement or conversion? |
| **M5 — Dashboard and retention** | 3 | Interactive trending feed, filtering, watchlists, auth (now that user-specific state exists) | Return-rate gate at a usable denominator (n≈200) |
| **M6 — Scale carefully** | — | Additional sources, paid Reddit tier if M0 justified it, user portfolios, monetization (with counsel) | Validated retention |

Construction total through M4: **10–12 weeks.** Elapsed time including gates is unknown by design — a gate that takes four extra weeks to pass because the writing needs another revision isn't a missed estimate, it's the gate doing its job.

**What moved from the original plan, and why:**

- Price and performance data capture moved from M4 into M1/M2 — the clock on the track record starts as early as possible, since it's the one component whose value compounds with elapsed time regardless of pipeline quality (ADR-0001, D-03).
- The weekly email moved from M5 into M3, and the interactive dashboard moved from M3 into M5 — publication is the actual MVP; the dashboard is a retention-gated addition, not the launch vehicle (ADR-0001, D-18).
- Auth moved from M3 into M5 — there's nothing user-specific to protect until M5, and a login wall in front of an unvalidated product would depress the exact metric M5's gate measures (ADR-0001, D-07).
- The Reddit connector moved from week 2 of the original plan to M6, conditional on both a demonstrated earliness advantage and revenue to fund the commercial tier (ADR-0001, D-10).

## Reading the gates

Most of the gates above are qualitative — a judgment call by the people running M0's reader panel or M2's quality-bar comparison, not a formula. That's deliberate: the project's existential risk is generic output, and no metric catches "technically correct, reads like AI slop" as reliably as a person reading it does (`docs/VISION.md`, MVP philosophy #2). The one quantitative gate, M5's return-rate threshold, is itself paired with a qualitative check — the "how would you feel if this no longer existed" question and unprompted sharing behavior — because a return-rate number at a small sample swings wildly on a handful of people and shouldn't be trusted alone until the sample is large enough to mean something (`docs/RISKS.md`, North star metric).

## Distribution workstream

The single biggest omission in the original planning set wasn't a feature — it was the complete absence of a distribution plan across six documents (ADR-0001, D-11). For a publishing product, distribution isn't a marketing afterthought; it's the delivery mechanism, as central as the pipeline itself. Three pieces, started in M0 and carried forward:

- **A named list of communities and channels** where the primary persona (`docs/VISION.md`, Who this is for) actually spends time — not "post it somewhere and see," a specific, written list drafted before M0's write-ups even exist, so sharing them isn't an afterthought once they're done.
- **One owned channel: the email list**, live from M0's landing page onward. Every other channel — a community, a platform, a partnership — can change its rules or disappear; an email list a reader opted into directly doesn't.
- **A publishing cadence, fixed from M3 onward.** Weekly, regardless of whether anything dramatic happened in the market that week (`docs/VISION.md`, Why publication, before dashboard) — the cadence itself is part of what keeps this a publication rather than a reaction to hot moments, and it's also what the north-star metric measures against.

None of this is optional groundwork to revisit later. A pipeline that produces excellent theses nobody sees has the same practical outcome as a pipeline that produces mediocre ones.

## First 30 days

This covers M0 in full and the start of M1 — roughly four to five weeks at the stated build-week estimates, treated here as "the first month" loosely rather than a precise day-count, since M0 is a gate as much as a build phase, and gates don't run on a calendar.

**Weeks 1–3 — M0: validate the writing, not the code.**

- Hand-write 10–20 topic-and-thesis write-ups using real, current market narratives — no code beyond a notebook or script. Keep an intervention log alongside them: every topic rejected before selection, every fabricated or unsupported claim removed, every sentence rewritten (ADR-0001, D-09). A large intervention delta is itself a finding — it means what got validated was a human writing, not a pipeline.
- Write down the primary persona — the informed generalist (`docs/VISION.md`, Who this is for) — before recruiting a single reader; the gate below is only valid if the readers who see the write-ups actually match that persona.
- Share the write-ups with 5–10 target-persona readers and ask the "how would you feel if this no longer existed" question (`docs/RISKS.md`).
- In parallel: read the relevant subreddits directly, by hand, for the same period — zero API calls, not a commercial use of Reddit's API — and log whether social chatter surfaced any of the same narratives meaningfully earlier than curated RSS would have (`docs/ARCHITECTURE.md`, Data ingestion). File the Reddit API developer application regardless; it's free, and the reported approval lag is 2–4 weeks, so the clock should start now no matter what the comparison shows.
- Stand up a landing page describing the core value proposition and an email list — the first piece of a real distribution plan, not a launch-week improvisation (ADR-0001, D-11). Draft the distribution list itself: named communities and channels where the target persona actually spends time.
- Build the one-page cost model (`docs/AI_SYSTEM.md`, Cost model) and confirm Claude API, Finnhub, and Supabase access.
- **Gate:** do target-persona readers find the write-ups genuinely useful, and is the intervention delta small enough that a pipeline could plausibly close it? If not, stop and revisit the concept before writing a line of pipeline code.

**Weeks 4–5 — M1 begins: ingestion and the clock.**

- Scaffold the repo: Next.js on Vercel, the `jobs/` package for the Python scripts, GitHub Actions for CI and cron (`docs/ARCHITECTURE.md`).
- Write the Postgres schema migration for the core tables (`docs/DATA_MODEL.md`).
- Build the RSS connectors for the feeds validated in M0, with dedupe into `content_items`, running hourly.
- Build ticker/company extraction (`docs/AI_SYSTEM.md`, Agent 1).
- Start the `prices/` job — daily `price_snapshots` for every tracked company — deliberately before the AI pipeline exists, so price history already has weeks of depth by the time `thesis/` needs it (ADR-0001, D-03).

By day 30–35, the honest state of the project is: the M0 gate has passed, content is flowing, and price history has started accumulating. There is no AI pipeline yet and no user-facing page yet — both come later, and rushing them earlier is exactly the bundled-estimate mistake ADR-0001 D-08 flags.

## First 10 tasks

1. File the Reddit API developer application — option-preservation only. Free, with a 2–4 week lag; no connector gets built against it in the MVP (ADR-0001, D-10).
2. Hand-write 10–20 topic-and-thesis write-ups on real, current narratives, no code, keeping an intervention log of every rejected topic, removed claim, and rewritten sentence (ADR-0001, D-09).
3. Write down the primary persona and share the write-ups with 5–10 readers who actually match it (`docs/VISION.md`, Who this is for).
4. Read the relevant subreddits by hand for the same period as task 2, and log whether they surfaced narratives earlier than curated RSS would have (`docs/ARCHITECTURE.md`, Data ingestion).
5. Stand up the landing page, email list, and a named-communities distribution list (ADR-0001, D-11); sign up for Finnhub and Supabase, confirm Claude API access, and finalize the 10–15 curated RSS feeds.
6. Scaffold the repo — Next.js on Vercel, the `jobs/` package, GitHub Actions for CI and cron — and write the initial Postgres schema migration (`docs/DATA_MODEL.md`).
7. Build the RSS ingestion connector with dedupe into `content_items`, running hourly, plus ticker/company extraction (`docs/AI_SYSTEM.md`, Agent 1).
8. Start the `prices/` job — daily `price_snapshots` — before the AI pipeline exists, so price history has real depth by the time positions start opening (ADR-0001, D-03).
9. Build the topic synthesizer (with continuity resolution) and thesis generator, with structured output, citations, and a golden-set regression check, run against real ingested data. No UI (`docs/AI_SYSTEM.md`).
10. Open the first system positions under the fixed 90-day rule, start the daily `performance_snapshots` job, and only then build the public pages and weekly email. Do not start the interactive dashboard until M5's retention gate passes (`docs/MVP_SCOPE.md`).
