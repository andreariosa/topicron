# Topicron

**A research publication with a database behind it.** Topicron discovers investment narratives from public chatter and news, publishes structured, cited, hedged theses on a fixed weekly cadence, and tracks — publicly, on a pre-committed hold period, and including the losers — whether those theses actually played out against real market data. It is not a stock picker and not a robo-advisor: every output is a hypothesis to track, not a recommendation to act on.

> **Governing decision records.** [`ADR-0001-mvp-scope-and-architecture.md`](./ADR-0001-mvp-scope-and-architecture.md) is the source of truth for scope, architecture, and sequencing — approved following a skeptical-CTO review of the original planning set. [`ADR-0002-free-tier-first-mvp.md`](./ADR-0002-free-tier-first-mvp.md) constrains *how* that plan is implemented while Topicron remains a pre-revenue hobby project: no new recurring cost beyond the founder's existing Cursor and Claude Pro subscriptions. Every document in this repository has been rewritten to be consistent with both. Where a decision is cited below (for example, "ADR-0001, D-03" or "ADR-0002, D-20"), the ID refers to a numbered decision inside the relevant ADR; read the ADRs themselves for full rationale.

**Status:** Pre-build. This repository currently holds planning, architecture, and decision-record documentation only — no application code has been written yet. The active milestone is **M0 — Validate the writing** (see `docs/ROADMAP.md`); nothing beyond a hand-run concierge test and a landing page is expected to exist before that gate passes.

## Who this is for

**Primary persona: the informed generalist.** Someone who follows markets closely, already reads long-form business and finance writing, and — this is the important part — reads far more than they trade. They want a structured argument on a narrative they'd otherwise only encounter as an unexplained headline: a bull case, a bear case, and named risks, not a signal telling them what to buy.

**Anti-persona: the signal-seeker.** Someone looking for real-time buy/sell alerts, a shortcut to picking winners without engaging with the reasoning behind them, or advice personalized to their own portfolio or risk tolerance. Topicron will serve this person badly, and product decisions should not chase their engagement — doing so would also weaken the impersonal-publisher posture the product's legal footing depends on (see `docs/RISKS.md`, Regulatory considerations).

This isn't just a marketing choice. The persona determines thesis depth, tone, hedging, publishing cadence, and who gets recruited for every quality gate in `docs/ROADMAP.md` (ADR-0001, D-17).

## Why this is useful before the track record exists

Topicron's core accountability claim — a public, unedited track record of hypothetical thesis performance — takes six to twelve months of elapsed calendar time to mean anything. On launch day it doesn't exist. Three months in, it's statistical noise: on the order of fifteen theses, high-beta baskets, a single quarter of market data (ADR-0001, D-01).

That means the track record cannot be the reason anyone reads Topicron in month one. Carrying the product until then is the interim value proposition: **a structured, cited, hedged investment thesis on a narrative you'd otherwise only see as an unexplained headline.** A bull case, a bear case, and named risks, grounded in real source material and real price data, delivered on a fixed schedule — that's worth reading before there's a single performance number attached to it.

The track record is the year-two moat. It is not the launch pitch.

## What this is

- A research publication, not a dashboard. The primary artifact is a published topic-and-thesis page and a weekly email, not an interactive app — the dashboard is deferred behind a retention gate (ADR-0001, D-18; `docs/ROADMAP.md`, M5).
- A research assistant, not a financial advisor — every output is a hypothesis to track, not a recommendation to act on.
- Topic discovery first, stock picking second — the entry point is always a narrative gaining traction, not a ticker to buy.
- Accountability as the product — every AI-generated thesis gets a hypothetical portfolio, held for a fixed 90-day period with no discretionary exits (ADR-0001, D-13), tracked daily against two benchmarks (ADR-0001, D-14), and published unedited, win or lose.
- Built free-tier-first, for now. While Topicron is a pre-revenue hobby project, no part of the stack costs anything beyond the founder's existing Cursor and Claude Pro subscriptions — everything else runs on a free service tier or locally (ADR-0002).

## What this isn't

- Not investment advice, and not offered by a registered investment adviser.
- Not a broker. No real money and no real trades in the MVP, full stop.
- Not another "what's trending on Reddit" tracker — and, per ADR-0001 D-10, not built on Reddit at all in the MVP. That space is already commoditized by free tools that track mentions and sentiment scores. Topicron's bet is the thesis-plus-tracked-outcome loop layered on top of narrative discovery, not the narrative discovery alone.
- Not an interactive dashboard, not yet. Filtering, a trending feed, and watchlists are real parts of the year-two product, deferred behind a proven retention signal (`docs/ROADMAP.md`, M5).

Full reasoning behind all of the above: `docs/VISION.md`.

## MVP scope (condensed)

Complete in-scope, deferred (with reinstatement triggers), and out-of-scope lists: `docs/MVP_SCOPE.md`.

**Building first:** curated RSS ingestion, ticker/company extraction (rule-based, with the LLM fallback for ambiguous cases deferred for now — `ADR-0002-free-tier-first-mvp.md`), and daily price snapshots. The performance-tracking clock starts here, in M1 — not in M4 as originally planned — because cached daily price history is the one component in this entire plan whose value compounds with elapsed time regardless of how good the AI pipeline turns out to be (ADR-0001, D-03).

**Building next:** LLM-driven topic synthesis, with explicit topic-continuity resolution so a narrative doesn't fragment into duplicate topics across pipeline runs (ADR-0001, D-12), and thesis generation with citations — both founder-run through Claude Code/claude.ai during the free-tier-first MVP rather than scheduled jobs (`ADR-0002-free-tier-first-mvp.md`, D-20); and the first system-generated hypothetical portfolios, opened under the fixed 90-day holding rule and tracked against dual benchmarks (ADR-0001, D-13, D-14).

**Deliberately deferred, each with a written condition that brings it back:** the fully automated, API-billed version of the AI pipeline — Reddit ingestion — a separately deployed backend service, Celery/Redis, user auth and login, the interactive dashboard, watchlists, user-editable portfolios, additional data sources, and paid market data.

**Explicitly out of scope, not deferred at all:** personalized recommendations of any kind, real trades, published backtests, and a handful of other boundaries this product doesn't cross regardless of how retention looks — full list in `docs/MVP_SCOPE.md`, regulatory reasoning behind the personalization boundary specifically in `docs/RISKS.md`.

## Tech stack (condensed)

| Layer | Choice | Notes |
|---|---|---|
| Frontend | Next.js + TypeScript + Tailwind | Deployed on Vercel (Hobby); public pages read Postgres via the Supabase client with row-level security |
| Backend service | None in the MVP | Dropped per ADR-0001, D-04 — no FastAPI, no Railway |
| Background jobs | Python scripts on scheduled GitHub Actions | Ingestion, extraction (rule-based), and price/performance snapshots are fully automated. Topic synthesis and thesis generation are founder-triggered during free-tier-first (ADR-0002, D-20) |
| Database | Postgres (Supabase, free tier) | Bundles auth — provisioned but unused until user-specific state exists (ADR-0001, D-07) |
| AI | Claude Pro + Claude Code (founder-run), for now | Zero incremental cost, via Cursor or claude.ai; the automated, metered Claude API pipeline is deferred (`ADR-0002-free-tier-first-mvp.md`, D-20/D-24) |
| Market data | Finnhub (free tier) | |
| Email | Resend (free tier) | Weekly digest; pulled into the MVP stack per ADR-0001, D-18. Requires one registered domain (ADR-0002, D-22) |
| Ops | Sentry, PostHog (free tiers) | Error tracking and product analytics |

Full rationale, trade-offs, and reinstatement triggers for every deferred choice: `docs/TECH_STACK.md`.

## Documentation

| Doc | Covers |
|---|---|
| `README.md` | This file — positioning, condensed scope and stack, documentation index |
| `ADR-0001-mvp-scope-and-architecture.md` | The governing decision record — source of truth for every scope, architecture, and sequencing decision referenced below |
| `ADR-0002-free-tier-first-mvp.md` | Free-tier-first implementation constraint — which pipeline stages run founder-triggered vs. automated, and why, while Topicron is a pre-revenue hobby project |
| `docs/VISION.md` | Full positioning: what this is and isn't, why it exists, the primary persona and anti-persona, why it's useful before the track record exists |
| `docs/MVP_SCOPE.md` | Complete in-scope, deferred (with reinstatement triggers), and explicitly-out-of-scope lists |
| `docs/ARCHITECTURE.md` | System design: module boundaries, data flow, deployment strategy |
| `docs/TECH_STACK.md` | Every tool and service, with rationale, trade-offs, and reinstatement triggers for deferred choices |
| `docs/DATA_MODEL.md` | Entities, relationships, schema, and the holding-period and benchmark rules |
| `docs/AI_SYSTEM.md` | Agent responsibilities, input/output contracts, topic continuity, hallucination mitigation, cost model, evaluation |
| `docs/ROADMAP.md` | Build weeks vs. quality gates, milestone sequencing |
| `docs/RISKS.md` | Technical, product, data, regulatory, and AI risks, plus validation strategy |

## Getting started

Nothing is implemented yet. Setup instructions land with the first scaffolding commit — see `docs/ROADMAP.md`, M1.

## Legal

Topicron is a research and educational tool. It is not a registered investment adviser and does not provide personalized investment advice. All theses, portfolios, and performance figures are hypothetical and for informational purposes only. See `docs/RISKS.md` for the full regulatory analysis this product is designed against.
