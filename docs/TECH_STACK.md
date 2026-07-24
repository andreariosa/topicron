# Tech stack

*This document covers every tool and external service, with the rationale, trade-offs, and reinstatement triggers behind each choice. System-level context — how these pieces fit together — is in [`ARCHITECTURE.md`](ARCHITECTURE.md); this document implements ADR-0001, Part 3 ("Updated architecture") at the tool-selection level. Decisions are cited inline as "ADR-0001, D-XX."*

## In the MVP

- **Claude API** — the LLM pipeline. Three tiers matched to task complexity, not one model for everything (`docs/AI_SYSTEM.md`): Haiku 4.5 for high-volume, low-complexity extraction; Sonnet 5 for topic synthesis, which now carries real judgment via continuity resolution (ADR-0001, D-12); Opus 4.8 reserved for thesis generation, where output quality has the most direct product impact. Called only from background jobs, batched wherever possible, and — since nothing in this pipeline has a latency requirement (`docs/ARCHITECTURE.md`) — a strong candidate for the Batch API's 50% discount across the board (`docs/AI_SYSTEM.md`, Cost model).
- **Finnhub** — market data, free tier. 60 calls/minute, real-time US quotes, fundamentals, and SEC filings — enough for daily snapshot ingestion at MVP scale (`docs/ARCHITECTURE.md`, Data ingestion). Worth naming explicitly: IEX Cloud, an earlier default choice for projects like this one, was fully shut down in August 2024. It still shows up often enough in older tutorials and templates that it's worth a standing warning — do not build against it. Massive.com (formerly Polygon.io, rebranded October 2025) is the paid upgrade path once revenue justifies it (see Deferred, below); it no longer offers a free tier, which is exactly why it isn't the MVP default.
- **Supabase** — Postgres + authentication. Bundling auth in the same product removes a separate service (Clerk, Auth0) that would otherwise need wiring up and paying for independently — even though auth itself sits unused until M5 (ADR-0001, D-07), having it provisioned and ready removes a whole integration task from that milestone when it arrives. Per ADR-0001 D-04, Supabase's role in this stack grew beyond the original plan: with no deployed backend service, the Supabase client plus row-level security is what the frontend reads through directly, and a Postgres function exposed as an RPC is the escalation path for anything beyond a straightforward filtered read. Neon remains a reasonable alternative specifically if per-branch database copies (one branch per feature or PR) become valuable to the workflow — pick one and move on rather than running both; nothing in the MVP currently needs that capability.
- **Vercel** — frontend hosting. Next.js's first-party deployment target: zero-config CI from a git push, an edge network well suited to the public, indexable, shareable pages that are the actual product surface (`docs/VISION.md`, Why publication, before dashboard), and a free tier that comfortably covers MVP traffic. Netlify is a reasonable substitute for a Next.js app but doesn't offer anything Vercel doesn't already cover here — no reason to introduce a second vendor relationship for parity.
- **GitHub Actions** — scheduled job execution and CI. Replaces the original plan's Railway Cron (ADR-0001, D-04): the same workflow that runs lint, type-check, and tests on every push also triggers the six scheduled jobs (`docs/ARCHITECTURE.md`) on cron schedules, with no second platform, no second billing relationship, and no separate place to check when a job silently stops running. The trade-off is a hard ceiling on job runtime and a less full-featured scheduler than a dedicated worker platform — acceptable at MVP volume, and explicitly the condition that brings a real worker platform back if it's ever hit (see Deferred, below).
- **Resend** — weekly email digest. Pulled into the MVP stack rather than deferred to a later milestone, since the publication is the actual M3 deliverable, not an add-on to it (ADR-0001, D-18). Chosen over Postmark mainly on developer experience and Next.js-ecosystem familiarity — both are legitimate choices for transactional and digest email at this scale, and this isn't a decision worth spending much more time on than it takes to read this sentence. Subscriber emails for the digest live in Resend's own audience feature rather than a custom Postgres table (`docs/DATA_MODEL.md`, Consolidation notes) — no reason to duplicate list management the email provider already does well.
- **Sentry** — error tracking. Unchanged from the original plan; a standard choice with no real alternative evaluation needed at this scale.
- **PostHog** — product analytics. Unchanged from the original plan. Doubles as the instrument for the north-star return-rate metric (`docs/RISKS.md`, North star metric) via anonymous IDs, since there's no login to key off of before M5 (ADR-0001, D-07).

## Deferred, with reinstatement triggers

The reasoning behind each of these is in ADR-0001 in full (particularly D-04, D-10, D-12); this table states the resulting condition, not the argument for it (`docs/MVP_SCOPE.md`).

| Deferred | What it is | Trigger to reinstate |
|---|---|---|
| FastAPI (deployed service) | A dedicated backend API layer | A consumer appears that isn't our own frontend, or logic emerges that can't live in a scheduled job or a Supabase RPC (ADR-0001, D-04) |
| Railway | Hosting for the above | Only relevant if FastAPI is reinstated — there's nothing else in this stack Railway would host |
| Celery + Redis | Task retries, controlled concurrency | Retries or concurrency are genuinely required — not anticipated at MVP job volume |
| Upstash | Managed Redis for the above | Only relevant once Celery is reinstated |
| `pgvector` | Embedding-based topic matching | Prompt-level topic continuity (`docs/AI_SYSTEM.md`) demonstrably fails to prevent topic fragmentation (ADR-0001, D-12) |
| Vector DB, external (Pinecone, Weaviate) | A dedicated vector database | Not anticipated at this scale under any current plan; `pgvector` inside the existing Postgres instance is the first, and likely only, escalation step |
| Reddit Data API | Content ingestion from Reddit | M0's human-read comparison shows meaningful earliness over RSS, *and* revenue exists to fund the commercial tier — the free tier is non-commercial-use only (ADR-0001, D-10) |
| Massive.com (formerly Polygon.io) | Real-time market data | Revenue exists to justify the upgrade over free-tier Finnhub |

Auth doesn't appear in this table on purpose — Supabase, the tool, is already selected and provisioned above. What's deferred is turning it on, which is a product decision about user-specific state existing (`docs/MVP_SCOPE.md`), not a tool-selection question.

## What's avoided, not deferred

A few choices aren't on the table above because they're not trigger-gated at all — they're boundaries this stack doesn't cross regardless of pressure:

- **Scraping Reddit, or any source, as a workaround for API limits.** Reddit's terms explicitly prohibit it and the company actively defends against it (`docs/MVP_SCOPE.md`, Explicitly out of scope). The Reddit connector is deferred; scraping around the deferral is not an option that becomes available under any trigger.
- **Building against IEX Cloud.** Fully shut down in August 2024 — not a trade-off to weigh, just dead.
- **A second deployed service "just in case."** Every tool above earns its place by solving a problem that exists today. Standing up infrastructure ahead of a proven need is the overengineering this stack was rebuilt to avoid (ADR-0001, D-04).
