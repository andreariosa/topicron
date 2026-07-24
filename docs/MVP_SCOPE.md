# MVP scope

*This document applies the five operating principles in [`VISION.md`](VISION.md) to produce a concrete answer to "what are we actually building." It implements ADR-0001, Part 4 ("Updated scope"), constrained further by the free-tier-first execution rules in ADR-0002. Decisions are cited inline as "ADR-0001, D-XX" or "ADR-0002, D-XX."*

**Free-tier-first note (ADR-0002, D-19).** Every "in scope" item below is additionally constrained, for as long as Topicron remains a pre-revenue hobby project, to run on a free service tier or locally — no component may introduce a new recurring cost beyond the founder's existing Cursor and Claude Pro subscriptions. This changes *how* some in-scope items are executed, not *whether* they're in scope; see the Extraction, Topic synthesis, and Thesis generation rows below, and ADR-0002 in full.

Three categories, in order of commitment: **in scope** (building this, now), **deferred** (not building this yet, and here is exactly what would change that), and **explicitly out** (not a backlog item — a boundary this product doesn't cross while it's structured this way).

## In scope

| Area | What's included | Traces to |
|---|---|---|
| Ingestion | Curated RSS feeds (10–15), deduped into `content_items` | — |
| Extraction | Rule-based ticker/company matching; LLM fallback for ambiguous cases deferred during free-tier-first, logged for manual review instead | ADR-0002, D-20 |
| Price & performance tracking | Daily price snapshots; daily performance snapshots computed against two benchmarks | D-03, D-14 |
| Topic synthesis | LLM-driven, with explicit continuity resolution across runs; founder-run via Claude Pro/Code during free-tier-first rather than a scheduled job; momentum is a trailing mention-count comparison computed in a query — no sentiment-scoring subsystem | D-12, D-06, ADR-0002 D-20 |
| Thesis generation | Bull case, bear case, named risks, confidence level, equal-weight suggested basket, paraphrased citations, hypothesis caveat; founder-run via Claude Pro/Code during free-tier-first | D-15, ADR-0002 D-20 |
| Portfolios | One system-generated hypothetical portfolio per published thesis; fixed 90-day hold, no discretionary exits | D-13 |
| Publication | Public, indexable, shareable topic/thesis pages; weekly email digest via voluntary signup, no login wall | D-07, D-18 |
| Track record | Public, including losing theses, updated daily, never quietly stopped or de-emphasized | `docs/VISION.md` |
| Ops & QA | Sentry, PostHog, a code-enforced daily cost cap (dormant until ADR-0002, D-24 fires), a golden-set regression check (founder-run during free-tier-first), weekly manual QA sampling | D-16, ADR-0002 |

Full mechanics behind each row: `docs/ARCHITECTURE.md` (system shape), `docs/DATA_MODEL.md` (schema), `docs/AI_SYSTEM.md` (agent behavior).

## Deferred (trigger-gated)

Nothing below is cut — each carries a specific, written condition that brings it back. The discipline is in writing the condition down before deferring, not after (`docs/VISION.md`, MVP philosophy #5).

| Deferred | What it would add | Trigger to reinstate |
|---|---|---|
| Claude API (automated, unattended pipeline) | Scheduled Haiku/Sonnet/Opus calls replacing the founder-run Claude Pro/Code sessions for extraction fallback, topic synthesis, and thesis generation | Real revenue exists, founder-run sessions consistently exceed ~3–4 hours/week, content volume outgrows what one session can responsibly cover, or the founder decides the ~$13–25/month is worth paying regardless (ADR-0002, D-24) |
| Reddit ingestion | An earlier-signal source than curated RSS | M0's human-read comparison shows meaningful earliness over RSS, *and* revenue exists to fund the commercial API tier — the free tier is non-commercial-use only |
| A separately deployed backend service (FastAPI) | A dedicated API layer independent of the frontend | A consumer appears that isn't our own frontend, or logic emerges that can't live in a scheduled job or a Supabase RPC |
| Celery + Redis | Task retries and controlled concurrency for background jobs | Retries or concurrency are genuinely required — not anticipated at MVP scale |
| `pgvector`-based topic matching | A fallback for topic continuity if prompt-level resolution proves insufficient | Prompt-level continuity (`docs/AI_SYSTEM.md`) demonstrably fails to prevent topic fragmentation |
| Auth and login | Persistent, user-specific state | User-specific state actually exists to gate — watchlists, saved portfolios (M5) |
| Interactive dashboard (filtering, sorting, trending feed) | A browsable, on-demand alternative to the publication | The publication shows a real retention signal at a usable sample size (`docs/ROADMAP.md`, M5 gate, n≈200) |
| Watchlists | Personalized, saved topic tracking per reader | Same trigger as the dashboard — both are M5, both require auth |
| User-editable portfolios | Reader-customized position weights, instead of the system's naive equal weight | Validated retention from M5, and confirmation that customized weights don't reintroduce the personalization risk `docs/RISKS.md` warns about |
| Additional data sources (beyond the curated RSS list) | Broader topic coverage | Validated retention from M5 justifies the ingestion and QA overhead of more sources |
| Paid market data (Massive.com, formerly Polygon.io) | Real-time quotes instead of Finnhub's free-tier delay | Revenue exists to justify the upgrade over free-tier Finnhub |

The reasoning behind each trigger — particularly Reddit (D-10), the dropped backend service (D-04), topic continuity's `pgvector` fallback (D-12), and the free-tier-first AI pipeline (ADR-0002, D-20/D-24) — is in ADR-0001 and ADR-0002 in full; this table states the resulting condition, not the argument for it.

## Explicitly out of scope

These aren't deferred features waiting for a trigger — they're boundaries. Each one either crosses a legal line this product's positioning depends on staying behind, or defeats the accountability claim that is the entire product bet. Revisiting any of them requires a deliberate decision, not a milestone passing.

- **Personalized recommendations of any kind.** The line between "impersonal publisher" and "investment adviser" (`docs/RISKS.md`, Regulatory considerations).
- **Real brokerage integration or real trades.** No real money moves through this product, full stop.
- **Any published backtest or historical performance figure.** A thesis generated against historical data by a current model has already read the outcome — publishing that number is the AI-washing pattern `docs/RISKS.md` warns about (ADR-0001, D-02). Historical runs exist only for internal pipeline QA and are never shown in-product.
- **Conviction- or personalization-weighted allocations.** `suggested_basket` stays a naive equal weighting, on purpose (`docs/AI_SYSTEM.md`).
- **LLM-graded thesis accuracy.** The only judge of a thesis is real subsequent market data via the performance-snapshot job — never a model grading its own or another thesis's output (`docs/AI_SYSTEM.md`, Evaluation engine).
- **Scraping any source whose terms prohibit it.** Reddit's terms explicitly prohibit scraping and the company actively defends against it; this product doesn't route around a licensing decision with a technical workaround (`docs/TECH_STACK.md`).
- **Verbatim republication of source article text.** Citations store a URL, publisher, headline, and our own paraphrase — never quoted body text (ADR-0001, D-15; `docs/DATA_MODEL.md`).
- **Monetization before securities counsel review.** Nothing about pricing, subscriptions, or premium tiers ships ahead of a specific legal review, regardless of how retention looks.

The in-scope list above maps to concrete system components in `docs/ARCHITECTURE.md`; the tool-level rationale and full reinstatement-trigger detail behind every deferred infrastructure choice is in `docs/TECH_STACK.md`.
