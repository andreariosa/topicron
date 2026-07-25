# ADR-0001 — MVP scope, architecture, and sequencing

**Status:** Accepted
**Date:** 2026-07-23
**Context:** Adjudication of the skeptical-CTO review of the pre-build planning set (`README`, `ARCHITECTURE`, `DATA_MODEL`, `AI_SYSTEM`, `ROADMAP`, `RISKS`).
**Decision owners:** founder + technical co-founder

Each criticism from the review is classified ACCEPT / PARTIALLY ACCEPT / REJECT, with rationale, MVP impact, and — where accepted — the exact documentation change required.

---

## Part I — Strategic criticisms

### D-01 — The differentiator does not exist at launch

**Criticism:** The product's core claim ("public, unedited track record") requires 6–12 months of elapsed calendar time. On launch day it is empty, and at month three it is statistical noise (n≈15, high-beta baskets, one quarter).

**Verdict: ACCEPT**

**Why:** This is arithmetic, not opinion. No engineering decision changes it. The plan currently has no stated answer to "why would anyone use this in month one," which means the first six months are unfunded by any value proposition.

**Impact on MVP:** Forces an explicit *interim* value proposition — thesis writing quality — and moves the engineering centre of gravity from systems to content. The accountability loop becomes a compounding asset that is *accumulated* early and *marketed* late.

**Documentation change:**
- `README.md` — add a "Why this is useful before the track record exists" section. Interim value prop: *a structured, cited, hedged thesis on a narrative you'd otherwise only see as a headline*. State plainly that the track record is the year-two moat, not the launch pitch.
- `RISKS.md` — promote this to the top of Product risks, above "AI slop", as **Cold-start of the differentiator itself** (distinct from the existing feed-emptiness cold start).

---

### D-02 — Backtesting cannot substitute for a live track record

**Criticism:** Generating theses against historical data with a current model is lookahead-contaminated; publishing those numbers is the AI-washing `RISKS.md` already warns against.

**Verdict: ACCEPT**

**Why:** The model has read the outcome. There is no clean way to remove that, and a published backtest would be a marketing claim the product cannot substantiate — precisely the SEC pattern cited in `RISKS.md`.

**Impact on MVP:** Removes the tempting shortcut. Historical runs remain useful for *pipeline debugging* (does it produce schema-valid, grounded, non-generic output?) but produce no performance figure that may ever leave the building.

**Documentation change:**
- `AI_SYSTEM.md` — add to "Evaluating AI-generated ideas": historical/backtested performance figures are **never published, quoted, or shown in-product**. Historical runs are for pipeline QA only.
- `RISKS.md` — add to the AI-washing bullet: a published backtest counts as an unsubstantiated capability claim.

---

### D-03 — Start the performance clock immediately (invert M4)

**Criticism:** Price snapshots + positions + a daily arithmetic job is the cheapest component in the plan and the only one whose value is a function of elapsed time. Building it at week 8 discards two months of track record permanently.

**Verdict: ACCEPT**

**Why:** Asymmetric cost/benefit. The *data collection* is a cron script and a loop; the *chart* is the expensive, deferrable part. The roadmap currently couples them and defers both.

**Impact on MVP:** `PriceSnapshot`, `Position`, and `PerformanceSnapshot` move from M4 into M1/M2. No UI work moves forward. By the time a chart is built, it has real depth on day one.

**Documentation change:**
- `ROADMAP.md` — split the old M4 in two: *performance data capture* (moves into M1/M2, invisible to users) and *performance presentation* (stays late). Rewrite the milestone table accordingly.
- `ARCHITECTURE.md` — state that the daily price + performance job ships with ingestion, before the AI pipeline is trustworthy, because its value accrues with time rather than with quality.

---

## Part II — Overengineering

### D-04 — Two services and two languages for a solo developer

**Criticism:** Drop FastAPI; the pandas justification doesn't survive contact with the actual maths (`Σ(weight × price_now/price_entry) − 1`).

**Verdict: PARTIALLY ACCEPT**

**Why:** Accepted for the *deployed HTTP service* — it buys a second deploy target, a second CI path, an OpenAPI contract to keep in sync, and CORS, for zero capability the frontend can't get from Supabase directly. Rejected for *Python itself*: the ingestion, extraction, and LLM batch jobs are Python regardless, and the review's framing implied Python leaves with FastAPI. It doesn't. The repo stays polyglot; it just stops being multi-service.

**Impact on MVP:** One deploy target (Vercel) plus scheduled jobs. Frontend reads Postgres through the Supabase client with row-level security. Roughly a week of scaffolding, CORS, and contract-sync work removed.

**Documentation change:**
- `ARCHITECTURE.md` — replace the "Backend" section. New shape: **Next.js on Vercel + Supabase (Postgres/auth) + a `jobs/` package of Python scripts on scheduled GitHub Actions.** Railway drops out of the MVP stack.
- Add explicit **reinstatement triggers** for FastAPI: (a) a consumer that isn't our own frontend, (b) logic that cannot live in a job or an RPC, (c) a job runtime exceeding the Actions ceiling. Until then, no service.
- `README.md` — update the tech-stack table.

---

### D-05 — The schema is built for year two

**Criticism:** Cut `Position.exit_*`, `Portfolio.user_id`, `InvestmentThesis.version`, the `draft/published` status, the four-state topic status, and `SentimentSnapshot`.

**Verdict: PARTIALLY ACCEPT** — this one I got partly wrong. Per field:

| Field / table | Verdict | Reasoning |
|---|---|---|
| `SentimentSnapshot` (table) | **ACCEPT — cut** | An entire table serving the one capability `RISKS.md` calls commoditized. See D-06. |
| `Portfolio.user_id` | **ACCEPT — cut** | No user portfolios before M6. Every MVP portfolio is system-generated. |
| `Topic.status` (4 states) | **ACCEPT — reduce** | Collapse to `active` / `archived`. `emerging` vs. `trending` is a query over mention counts, not stored state. |
| `Thesis.status` draft/published | **ACCEPT — cut** | One publisher. A `published_at` timestamp (nullable) covers it. |
| `Position.exit_price` / `exit_date` | **REJECT — keep** | The review contradicted itself: D-13 mandates a fixed holding period, which *requires* exit fields. They are load-bearing from week one. |
| `Thesis.version`, `model_used`, `prompt_version` | **REJECT — keep** | Three columns, near-zero cost, and they are the only mechanism making a post-hoc quality regression diagnosable. Cutting audit metadata to save three columns is false economy. |

**Impact on MVP:** Seven tables — `content_items`, `companies`, `topics`, `theses`, `positions`, `prices`, `performance_snapshots` — plus the two join tables (`topic_content_items`, `content_item_company_mentions`), which stay because traceability is the product's honesty mechanism.

**Documentation change:**
- `DATA_MODEL.md` — substantial rewrite. Remove `SentimentSnapshot` entirely; remove `Portfolio.user_id`; collapse both status enums; keep exit and versioning fields with a one-line note on *why* each survives. Update the Mermaid ER diagram to match. Add a short "deferred entities" appendix so the year-two shape isn't lost, just unbuilt.

---

### D-06 — Internal contradiction on sentiment

**Criticism:** `RISKS.md` says mention/sentiment tracking is commoditized and shouldn't get disproportionate investment; `DATA_MODEL.md` gives it a table and `AI_SYSTEM.md` centres a momentum score.

**Verdict: ACCEPT**

**Why:** A genuine inconsistency across documents. Left unresolved, it will be resolved by whoever writes the code first.

**Impact on MVP:** Momentum becomes `count(content_items linked to topic in trailing 48h)` compared against a trailing baseline — computed in a query, stored nowhere, trivially auditable. No sentiment scoring in the MVP at all.

**Documentation change:**
- `AI_SYSTEM.md` — rewrite the momentum note in Agent 2: define it as a stored-nowhere query over mention counts; remove sentiment from Agent 1's remit and from the cost-control section's "extraction and sentiment" phrasing.
- `DATA_MODEL.md` — remove `SentimentSnapshot`.
- `RISKS.md` — keep the commoditization bullet; add that the resolution is *no sentiment subsystem in the MVP*.

---

### D-07 — Auth in M3 is premature

**Criticism:** A signup wall in front of an unvalidated product, at the exact moment you're trying to measure return behaviour.

**Verdict: PARTIALLY ACCEPT**

**Why:** Accepted that a *login wall* is wrong — it depresses the very metric being measured and gates content that should be publicly shareable and indexable. Rejected as a blanket "no identity": email capture is the single most valuable asset of the first six months (see D-18), so identity arrives — as a subscribe box, not a gate. Supabase auth stays available and unused.

**Impact on MVP:** All topic and thesis pages are public and anonymous. PostHog anonymous IDs measure return visits. Email addresses are collected voluntarily for the digest. Login ships only when there is something user-specific behind it (watchlists, M5+).

**Documentation change:**
- `ROADMAP.md` — remove auth from the M3 deliverables; replace with "public pages + email capture."
- `ARCHITECTURE.md` — note Supabase auth is provisioned but unused until user-specific state exists.

---

## Part III — Assumptions

### D-08 — The 8–10 week estimate

**Criticism:** Plausible for construction, unbounded for quality. M2's risk isn't wiring, it's reaching a thesis standard a professional would respect, and prompt iteration has no schedule.

**Verdict: ACCEPT**

**Why:** The estimate silently bundles a bounded engineering task with an unbounded research task. Bundled estimates like this are the standard mechanism by which a two-month project becomes a six-month one without anyone noticing the moment it happened.

**Impact on MVP:** The roadmap is re-expressed as **build weeks** (estimable) and **quality gates** (not estimable, and empowered to stop the project). 8–10 weeks stands as the construction estimate; total elapsed time is explicitly unknown.

**Documentation change:**
- `ROADMAP.md` — separate the two tracks. Each gate gets a written pass criterion and an explicit "if this fails, we stop or pivot" clause. Delete the unqualified 8–10 week MVP claim from the milestone preamble and restate it as construction-only.

---

### D-09 — The concierge test will flatter you

**Criticism:** You'll cherry-pick topics, discard bad generations, and edit prose — validating a bar the pipeline can't reach.

**Verdict: ACCEPT**

**Why:** Near-zero cost to fix, and the failure mode is invisible without the fix.

**Impact on MVP:** M0 gains one artifact: an **intervention log** recording, per write-up, every topic rejected before selection, every fabricated or unsupported claim removed, and every sentence rewritten. The delta is the M2 engineering backlog. A large delta is itself a finding: it means the validated product was a human writing, not a pipeline.

**Documentation change:**
- `ROADMAP.md` (M0) and `RISKS.md` (Validation strategy, item 1) — make the intervention log a required deliverable of the concierge test, with the three categories above. State that the log is reviewed at the M0 gate.

---

### D-10 — Reddit is a trap

**Criticism:** Free tier is non-commercial; commercial tier is five figures; you'd build a connector in week 2 for a source you must remove the day you monetize. Cut it.

**Verdict: PARTIALLY ACCEPT** — and this is the item where the original plan had the better instinct.

**Why:** The licensing analysis is right and unavoidable. But the review's conclusion overreached: curated finance RSS is a *lagging* source. If Reuters has written it, the narrative is no longer emerging, and "topic discovery first" — the product's stated entry point — is weakened by an RSS-only diet. The resolution isn't to choose between them; it's to separate the *signal question* from the *build question*.

**Impact on MVP:**
- **Build:** no Reddit connector in the MVP. RSS proves the ingestion pipeline.
- **Signal:** during M0, a human reads the relevant subreddits directly. This costs zero API calls, is not a commercial use of the API, and answers the real question — does social chatter surface narratives meaningfully earlier than curated feeds? If M0 shows it doesn't, the licensing problem evaporates. If it does, the five-figure tier becomes a costed, revenue-funded decision made on evidence.
- **Option:** file the API application in week 1 regardless. Free, 2–4 week lag, preserves optionality.

**Documentation change:**
- `ARCHITECTURE.md` (Data ingestion table) — mark Reddit **deferred**, retain the licensing note, and add the "human reading during M0" method.
- `ROADMAP.md` — remove the Reddit connector from week 2 and from first-10-tasks item 6; keep the API application as task 1 with its rationale rewritten as option-preservation. Add the earliness comparison as an M0 finding.
- `README.md` — remove Reddit from "Building now"; move to "Deliberately deferred" with the licensing rationale.

---

### D-11 — North star metric and the missing distribution plan

**Criticism:** 7-day return rate is the right metric with an unusable denominator at n=20; and there is no distribution plan anywhere in six documents.

**Verdict: PARTIALLY ACCEPT** (metric) / **ACCEPT** (distribution)

**Why:** The metric is correct and should stay — it distinguishes "interesting once" from "habit" better than any alternative. But at n=20 it swings 15 points on two people, so it cannot be a *gate* at that scale; it's directional only. The distribution gap is the larger finding: for a publishing product, distribution is not a marketing afterthought, it is the product's delivery mechanism, and its total absence from the planning set is the single biggest omission.

**Impact on MVP:** Two gates instead of one — quantitative (return rate, directional until n≈200) and qualitative (the "very disappointed" question already in `RISKS.md`, plus unprompted sharing behaviour). A distribution plan becomes a first-class M0/M3 deliverable, not a launch-week improvisation.

**Documentation change:**
- `RISKS.md` — qualify the north star with its minimum viable denominator; pair it with the qualitative gate; add **"No distribution plan"** as a named product risk.
- `ROADMAP.md` — add a distribution workstream: named communities, a publishing cadence, and one owned channel (email list) started in M0 alongside the landing page.

---

## Part IV — Missing pieces

### D-12 — Topic identity across runs

**Criticism:** The synthesizer runs every few hours over 30–100 items with no merge/dedup/continuity rule. "AI datacenter power demand" at T and "Utilities strained by AI buildout" at T+3h become two topics.

**Verdict: ACCEPT**

**Why:** The hardest unsolved problem in the pipeline and it isn't mentioned anywhere. It determines whether the feed reads as a set of tracked narratives or as churn — and a topic that fragments cannot carry a thesis, a portfolio, or a track record. It silently breaks D-03.

**Impact on MVP:** Every synthesis run must receive the currently-active topics as context and must return, per output, either an existing topic id (update) or a new-topic flag. Embedding similarity via `pgvector` is the fallback if prompt-level continuity proves insufficient — this is the one place the earlier "no vector DB" ruling may need revisiting, and `pgvector` inside Postgres honours it anyway.

**Documentation change:**
- `AI_SYSTEM.md` — new subsection under Agent 2, **Topic continuity**: active topics passed as input, output must resolve to update-or-create, merge rule for topics that converge, archive rule for topics with no new content in N days. Flag as the highest-uncertainty component of the pipeline.
- `RISKS.md` — add topic fragmentation to Technical risks.
- `ARCHITECTURE.md` — note `pgvector` as the escalation path, still inside Postgres.

---

### D-13 — Holding period and exit rules are undefined

**Criticism:** Nothing says how long a position is held or what happens when a topic cools. Without a pre-committed rule, every performance number is unfalsifiable.

**Verdict: ACCEPT**

**Why:** An exit rule chosen after seeing the results is not an exit rule. This is the difference between a track record and a story.

**Impact on MVP:** A fixed rule, written down before the first position opens, and applied mechanically: **entry at the next daily close after thesis publication; hold 90 days; exit at close on day 90; no discretionary exits; a cooling topic changes nothing about its open positions.** Boring and defensible beats clever and unfalsifiable.

**Documentation change:**
- `DATA_MODEL.md` — document the rule against `Position`, and confirm `exit_price`/`exit_date` as required (per D-05).
- `AI_SYSTEM.md` — add to the evaluation engine: the holding rule is fixed in advance and never adjusted retroactively; changes apply only to positions opened after the change, and are logged.
- `README.md` — state the holding period in the accountability description.

---

### D-14 — Benchmark choice

**Criticism:** An equal-weight basket of narrative stocks versus SPY measures beta, not skill.

**Verdict: ACCEPT**

**Why:** With SPY alone, a rising market makes every thesis look prescient. The accountability claim would be technically true and substantively misleading.

**Impact on MVP:** Report **two** benchmarks per portfolio: SPY (the comparison users expect and understand) and a sector or thematic ETF matched to the thesis (the comparison that isolates narrative selection). Two columns on `PerformanceSnapshot`, negligible cost.

**Documentation change:**
- `DATA_MODEL.md` — `PerformanceSnapshot` gains a second benchmark column plus a benchmark identifier; remove the "SPY or another fixed benchmark" ambiguity.
- `AI_SYSTEM.md` / `README.md` — state that performance is always shown against both, never against SPY alone.

---

### D-15 — Copyright exposure in `claim_excerpt`

**Criticism:** Storing and displaying excerpts of RSS content republishes third-party text.

**Verdict: ACCEPT**

**Why:** Low cost to fix now, awkward to fix after the field is populated and rendered.

**Impact on MVP:** `ThesisCitation` stores the source URL, publisher, headline, timestamp, and *our own paraphrase* of the supporting claim. No verbatim source body text is displayed. Citations link out.

**Documentation change:**
- `DATA_MODEL.md` — rename/redefine `claim_excerpt` accordingly and note the constraint.
- `AI_SYSTEM.md` — the thesis generator's citation contract requires a paraphrase plus a source id, never a quoted excerpt.
- `RISKS.md` — add content licensing to Data quality / legal risks: RSS feeds grant syndication of headlines and links, not reproduction of article bodies.

---

### D-16 — No cost model

**Criticism:** No token or dollar estimate appears anywhere.

**Verdict: ACCEPT**

**Why:** `AI_SYSTEM.md` already names cost surprise as the most common way an AI-heavy MVP goes wrong, then provides no numbers. An hour of arithmetic now determines whether the pipeline is a hobby-scale or a problem-scale expense before a single user exists.

**Impact on MVP:** A one-page estimate — items/day × tokens/item × price per model tier, split across extraction, synthesis, and thesis generation — plus a hard daily spend cap enforced in code (not just an alert) and a kill-switch.

**Documentation change:**
- `AI_SYSTEM.md` — replace the qualitative cost-control section with an estimate table and a stated monthly ceiling. Specify that the cap is enforced programmatically, and that exceeding it halts generation rather than degrading silently.

---

### D-17 — The user is undefined

**Criticism:** "Target users" recurs throughout and is never defined. A retail swing trader, a professional analyst, and a curious generalist want three incompatible products.

**Verdict: ACCEPT**

**Why:** It determines thesis depth, tone, hedging, publishing cadence, distribution channel, and the M0 recruiting list. Every one of those is currently unresolvable.

**Impact on MVP:** One named primary persona, written down before M0 recruiting, since M0's entire validity depends on showing the write-ups to the right people. My recommendation: **the informed non-professional who follows markets closely, reads more than they trade, and wants a structured argument rather than a signal.** They are reachable, they read long-form, and they are unlikely to mistake the output for advice — which also serves the publisher's-exclusion posture.

**Documentation change:**
- `README.md` — add a "Who this is for" section with the primary persona and one explicit anti-persona.
- `ROADMAP.md` — M0 recruiting targets that persona specifically; the gate is invalid if the readers aren't representative.
- `RISKS.md` — persona drift as a product risk (widening the audience dilutes the writing).

---

## Part V — The leaner MVP

### D-18 — Publication-first instead of dashboard-first

**Criticism:** Ship a weekly email before a dashboard: easier to build, measurable at scale, fits "general and regular circulation," and is the native format for what is actually a research publication.

**Verdict: PARTIALLY ACCEPT**

**Why:** Accepted that the *publication* is the product and that a scheduled cadence should come before an interactive UI — it is cheaper, it is measurable at n=500 rather than n=20, and `RISKS.md`'s own reading of *Lowe v. SEC* favours regular circulation over episodic reaction. Rejected as email-only: theses carry citations, linked companies, and eventually performance charts, none of which render well or track reliably in email clients, and the shareable, indexable public link is the distribution mechanism identified in D-11.

**Impact on MVP:** The M3 deliverable becomes a **public static-rendered topic/thesis page** (no auth, indexable, shareable) **plus a weekly email that summarizes and links to it.** The interactive dashboard — filtering, sorting, trending feed, charts — moves behind the retention gate. Email is pulled forward from M5; dashboard is pushed back.

**Documentation change:**
- `ROADMAP.md` — restructure M3 as "Publication v1 (public pages + weekly email)" and move the dashboard to M5, conditional on retention. Move Resend/Postmark from "once the digest ships" to the M3 dependency list.
- `ARCHITECTURE.md` — transactional email becomes an MVP external service, not a later addition.
- `README.md` — describe the product as a research publication with tracked outcomes, rather than a dashboard.

---

## Summary of verdicts

| ID | Criticism | Verdict |
|---|---|---|
| D-01 | Differentiator absent at launch | ACCEPT |
| D-02 | Backtesting is contaminated | ACCEPT |
| D-03 | Start the performance clock immediately | ACCEPT |
| D-04 | Drop the second service | PARTIALLY ACCEPT |
| D-05 | Schema over-built | PARTIALLY ACCEPT |
| D-06 | Sentiment contradiction | ACCEPT |
| D-07 | Auth too early | PARTIALLY ACCEPT |
| D-08 | Timeline conflates build and quality | ACCEPT |
| D-09 | Concierge test flatters | ACCEPT |
| D-10 | Cut Reddit | PARTIALLY ACCEPT |
| D-11 | Metric denominator / no distribution plan | PARTIALLY ACCEPT / ACCEPT |
| D-12 | No topic continuity | ACCEPT |
| D-13 | No exit rule | ACCEPT |
| D-14 | Benchmark measures beta | ACCEPT |
| D-15 | Copyright in citations | ACCEPT |
| D-16 | No cost model | ACCEPT |
| D-17 | User undefined | ACCEPT |
| D-18 | Publication before dashboard | PARTIALLY ACCEPT |

---

# 1. Updated MVP philosophy

**Topicron is a research publication with a database behind it — not a data platform that happens to publish.**

Five operating principles:

1. **Time-dependent assets start now; everything else waits.** Anything whose value compounds with elapsed calendar time (price history, positions, the track record, the email list) is built in week two even if nobody sees it for months. Anything whose value is available on demand (dashboards, filters, charts, auth) is built last.
2. **Quality is the gate; code is not.** The project's existential risk is generic output, and no amount of infrastructure addresses it. Build weeks are estimated; quality gates are not, and they are permitted to stop the project.
3. **Publish on a schedule, in public, unedited.** A fixed cadence serves the reader, the habit, and the publisher's exclusion simultaneously. Losing theses are shown exactly as prominently as winning ones — the moment that stops being true, the product has no thesis.
4. **Only claim what arithmetic can defend.** Every performance number traces to cached daily bars and a pre-committed holding rule. No backtests, no model grading models, no capability claims the product cannot demonstrate.
5. **Defer with a trigger, not a wish.** Every deferred component (FastAPI, Celery, Reddit, vector DB, user portfolios) carries a written condition that reinstates it. "Later" without a trigger is how deferral becomes denial.

---

# 2. Updated roadmap

Two tracks: **build weeks** are estimable; **gates** are not, and each can stop the project.

| Phase | Build weeks | Deliverables | Gate to pass |
|---|---|---|---|
| **M0 — Validate the writing** | 2–3 | 10–20 hand-written topic+thesis write-ups; intervention log; primary persona defined; landing page + email list live; distribution list of named communities; Reddit-vs-RSS earliness comparison; Reddit API application filed; cost model estimated | Do target-persona readers find the write-ups genuinely useful, and is the intervention delta small enough that a pipeline could plausibly close it? |
| **M1 — Ingestion + the clock** | 2 | RSS connectors (10–15 feeds), dedupe, ticker extraction, `PriceSnapshot` ingestion, schema migration, cron on GitHub Actions | Is content flowing cleanly, and is price history accumulating daily without gaps across weekends and holidays? |
| **M2 — Pipeline + first positions** | 3–4 | Topic synthesis with continuity resolution, thesis generation with citations, structured-output validation, golden-set regression check, first system positions opened under the 90-day rule, daily `PerformanceSnapshot` job. **No UI.** | Does automated output hold the M0 quality bar, judged against the same rubric by the same readers? *Highest-risk gate in the plan.* |
| **M3 — Publication v1** | 2 | Public, indexable topic/thesis pages; weekly email; PostHog instrumentation; first 100+ subscribers via the M0 distribution list | Do people open, read, return, and share — measured over at least four issues? |
| **M4 — Surface the record** | 1 | Performance charts against dual benchmarks; public track-record page including losers; closed-position retrospectives | Does visible accountability measurably change engagement or conversion? |
| **M5 — Dashboard and retention** | 3 | Interactive trending feed, filtering, watchlists, auth (now that user-specific state exists) | Return-rate gate at a usable denominator (n≈200) |
| **M6 — Scale carefully** | — | Additional sources, paid Reddit tier if M0 justified it, user portfolios, monetization (with counsel) | Validated retention |

Construction total through M4: **10–12 weeks.** Elapsed time including gates: unknown by design.

**Sequencing changes from the original roadmap:** performance data capture moved M4 → M1/M2; email moved M5 → M3; dashboard moved M3 → M5; auth moved M3 → M5; Reddit connector moved M1 → M6-conditional.

---

# 3. Updated architecture

```
Data sources (RSS feeds, Finnhub)
        │
        ▼
Python jobs  ──  scheduled GitHub Actions
  ingest/    hourly    → content_items (deduped)
  extract/   hourly    → ticker + company mentions
  prices/    daily     → price_snapshots
  synth/     6-hourly  → topics (with continuity resolution)
  thesis/    daily     → theses + positions
  perf/      daily     → performance_snapshots
        │
        ▼
   Postgres (Supabase) — single source of truth
        │
        ▼
Next.js on Vercel — static/ISR public pages, reads via Supabase client + RLS
        │
        ▼
   Resend — weekly email
```

**In the MVP:** Vercel, Supabase (Postgres + auth-provisioned-unused), GitHub Actions (cron), Claude API, Finnhub, Resend, Sentry, PostHog.

**Out of the MVP, with reinstatement triggers:**

| Deferred | Trigger to reinstate |
|---|---|
| FastAPI service | A non-frontend API consumer, or logic that can't live in a job/RPC |
| Railway | Job runtime exceeds the Actions ceiling |
| Celery + Redis | Retries or concurrency genuinely required — not anticipated |
| `pgvector` | Prompt-level topic continuity proves insufficient (D-12) |
| Reddit connector | M0 shows meaningful earliness advantage *and* revenue funds the commercial tier |
| Auth / login | User-specific state exists (watchlists, M5) |
| Vector DB (external) | Never at this scale; `pgvector` first |

**Schema (7 tables + 2 joins):** `content_items`, `companies`, `topics`, `theses`, `positions`, `price_snapshots`, `performance_snapshots`, `topic_content_items`, `content_item_company_mentions`.

**Load-bearing invariants:**
- No LLM call in a request path, ever.
- Every performance figure derives from `price_snapshots` and the fixed 90-day holding rule.
- Every thesis claim carries a paraphrased citation with a source id; no verbatim source text stored or displayed.
- Every generation logs model version and prompt version.
- Daily spend cap enforced in code; breach halts generation.

---

# 4. Updated scope

**In (MVP):**
- Curated RSS ingestion with dedupe
- Rule-based ticker/company extraction with LLM fallback
- Topic synthesis with explicit continuity resolution
- Thesis generation: bull case, bear case, risks, confidence, equal-weight basket, paraphrased citations, hypothesis caveat
- Daily price snapshots and daily performance snapshots against dual benchmarks
- One system portfolio per thesis, 90-day fixed holding period
- Public topic/thesis pages, indexable and shareable
- Weekly email digest
- Public track record including losers
- Sentry, PostHog, cost cap, golden-set regression check, weekly manual QA sampling

**Deferred (trigger-gated):** Reddit ingestion, FastAPI, Celery/Redis, auth and login, interactive dashboard, watchlists, user-editable portfolios, additional sources, paid market data, `pgvector`.

**Explicitly out (not backlog — boundaries):** personalized recommendations of any kind; real brokerage integration or real trades; any published backtest or historical performance figure; conviction- or personalization-weighted allocations; LLM-graded thesis accuracy; scraping any source that prohibits it; verbatim republication of source article text; monetization before securities counsel review.

---

# 5. Documentation files that must be rewritten

All six existing documents change. No new documents beyond this ADR — adding a doc per concern would be its own overengineering.

| File | Extent | Changes |
|---|---|---|
| `README.md` | **Substantial** | Add "Who this is for" (persona + anti-persona, D-17); add "Why this is useful before the track record exists" (D-01); reposition as a research publication rather than a dashboard (D-18); rewrite the tech-stack table (D-04); move Reddit to deferred (D-10); state the 90-day holding rule and dual benchmarks (D-13, D-14) |
| `ARCHITECTURE.md` | **Substantial** | Replace the Backend section — no FastAPI, no Railway (D-04); jobs on GitHub Actions; mark Reddit deferred with the M0 human-reading method (D-10); performance job ships with ingestion (D-03); add Resend as an MVP service (D-18); add `pgvector` escalation path (D-12); add the deferral-trigger table |
| `DATA_MODEL.md` | **Substantial** | Remove `SentimentSnapshot` (D-06); remove `Portfolio.user_id` (D-05); collapse both status enums (D-05); keep and justify exit + versioning fields (D-05); redefine `claim_excerpt` as paraphrase + source (D-15); second benchmark column (D-14); document the holding rule (D-13); update the ER diagram; add a deferred-entities appendix |
| `AI_SYSTEM.md` | **Substantial** | New topic-continuity subsection under Agent 2 (D-12); momentum redefined as a stored-nowhere query, sentiment removed (D-06); citation contract requires paraphrase (D-15); no published backtests (D-02); fixed holding rule, never retroactively adjusted (D-13); dual benchmarks (D-14); replace qualitative cost control with an estimate table and a code-enforced cap (D-16) |
| `ROADMAP.md` | **Full rewrite** | New milestone structure; build weeks separated from gates with written pass criteria (D-08); performance capture pulled forward (D-03); email pulled forward, dashboard and auth pushed back (D-07, D-18); Reddit connector removed from week 2 (D-10); intervention log as an M0 deliverable (D-09); distribution workstream added (D-11); first-30-days and first-10-tasks rewritten against the new sequence |
| `RISKS.md` | **Moderate** | Differentiator cold-start promoted to top product risk (D-01); topic fragmentation added to technical risks (D-12); content licensing added (D-15); no-distribution-plan added (D-11); persona drift added (D-17); north star qualified with minimum denominator and paired qualitative gate (D-11); sentiment resolution noted (D-06); backtest-as-AI-washing added (D-02); intervention log added to validation strategy (D-09) |

Regulatory content in `RISKS.md` is unchanged and remains accurate; the *Lowe* analysis in fact strengthens under D-18, since a scheduled publication fits "general and regular circulation" better than an on-demand dashboard.
