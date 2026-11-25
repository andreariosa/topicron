# AI system design

*This document covers agent responsibilities, input/output contracts, and evaluation. It implements the AI-pipeline decisions in ADR-0001 — D-02, D-05 (versioning fields), D-06, D-12, D-13, D-14, D-15, D-16 — and the execution-mode changes in ADR-0002, D-20. System-level job cadence is in [`ARCHITECTURE.md`](ARCHITECTURE.md); schema is in [`DATA_MODEL.md`](DATA_MODEL.md). Decisions are cited inline as "ADR-0001, D-XX" or "ADR-0002, D-XX." **Note:** the Agent 3 output contract below follows ADR-0003's ten-section thesis structure and ADR-0004's primary-source step (D-35); it was rewritten on 2026-11-25 as the first task of M2 (ADR-0005, D-36). The persistence of the new fields (`theses`) is an M2 migration decision, tracked in `PROJECT_STATE.md`.*

**Free-tier-first note (ADR-0002).** Everything below describes the pipeline's full designed behavior — the state it runs in once reinstated per ADR-0002, D-24. Until that trigger fires, `extract/`'s LLM fallback is deferred and `synth/`/`thesis/` run as founder-triggered sessions through Claude Code or claude.ai rather than scheduled API calls. The input/output contracts, prompts, and schemas below are identical either way — see the "Free-tier-first execution mode" note under each affected agent.

## Pipeline shape

Extraction → topic synthesis (with continuity resolution) → thesis generation, all running as background jobs against stored data (or, during the free-tier-first MVP, founder-triggered sessions using the identical contracts — ADR-0002, D-20) — the `extract/`, `synth/`, and `thesis/` jobs in `docs/ARCHITECTURE.md`. A separate, non-AI evaluation mechanism (the `perf/` job) closes the loop. No agent framework (LangGraph, CrewAI, AutoGen) — a plain sequential pipeline of typed calls to Claude is enough for what is fundamentally a linear process, and is far easier to debug than a framework designed for autonomous multi-step planning.

## Agent 1: entity and ticker extractor

**Responsibility:** identify which companies/tickers a piece of ingested content refers to.

**Model:** Claude Haiku 4.5, for the fallback path described below — dormant during free-tier-first (ADR-0002, D-20); see Free-tier-first execution mode, below.

**Input:** raw `content_items` text, run hourly alongside `ingest/`, batched across many items per call rather than issued one at a time.

**Output:**
```json
{
  "tickers": [{"symbol": "NVDA", "confidence": 0.92}],
  "companies_mentioned": ["Nvidia"]
}
```

**Notes:** rule-based matching (ticker regex + a company-alias dictionary) handles most cases cheaply; the model is used only as a fallback for ambiguous cases. Ticker collisions with common words are a real, recurring failure mode here — "ALL", "ARE", "IT", "ON", and "SO" are all real tickers (`docs/RISKS.md`, Entity resolution).

**Free-tier-first execution mode (ADR-0002, D-20):** the Haiku fallback above is deferred for now — the free-tier-first MVP runs rule-based matching only. Ambiguous cases that would otherwise go to the model (the "ALL"/"ARE"/"IT"/"ON"/"SO" collision problem above) are logged instead of resolved automatically, and reviewed by the founder during the same session used for topic synthesis and thesis generation. This keeps the gap visible and auditable rather than silently degrading extraction quality. See ADR-0002 for the reinstatement trigger.

**As built (M1b, rule-based path; `jobs/extract/`).** It reads only what ingestion stored (title, the feed's short description and the publisher's tags, never an article page) for the items ingested in the last 48 hours, and writes `content_item_company_mentions` rows for the companies in the `companies` table. The output is that table, not the JSON above, which belongs to the dormant model path. The rules, strongest first, each with a fixed confidence: the publisher's `EXCHANGE:SYMBOL` tag (1.0), where the exchange must be the company's own, so `TSE:T` is TELUS and not AT&T; a symbol written with its exchange, a dollar sign or parentheses (0.9); a company name from `jobs/extract/aliases.py` in the title (0.8) or only in the description (0.6). A bare symbol in running text is never accepted, which is how the "ALL"/"ARE"/"IT"/"ON"/"SO" collisions are avoided; it is reported in the job log by item id (never by headline, since the log is public), as is a tag with no exchange. Ambiguous cases are therefore logged and left unresolved, as the paragraph above requires. The job also prints the tagged tickers that match no company, most frequent first, which is the list to read when deciding which company to add to the prices universe next.

## Agent 2: topic synthesizer

**Responsibility:** identify emerging or trending narratives from a batch of recently ingested content, and resolve each one against the topics already being tracked — deciding whether it's a continuation of an existing narrative or genuinely new. Replaces what would otherwise be a bespoke topic-clustering ML pipeline (BERTopic, LDA, embedding clustering); modern LLMs are good enough at this kind of open-ended synthesis directly, given well-chosen input.

**Model:** Claude Sonnet 5 — this stage carries real judgment (continuity resolution, not just summarization), which justifies a step up from the extraction tier.

**Input:** a batch (roughly 30–100 items) of recent, high-signal `content_items`, run every 6 hours, plus the full set of currently `active` topics (title, summary, most recent supporting content) as context.

**Output:**
```json
{
  "resolution": "update | create",
  "topic_id": "uuid | null",
  "topic_title": "string",
  "summary": "string",
  "why_trending": "string",
  "linked_tickers": ["NVDA"],
  "supporting_content_item_ids": ["..."]
}
```

**Notes:** momentum is not part of this agent's output at all — see Momentum, below.

**Free-tier-first execution mode (ADR-0002, D-20):** during the free-tier-first MVP, this agent doesn't run as a scheduled job calling the API directly. The founder runs the exact prompt above personally, via Claude Code (in Cursor or a terminal, authenticated through the existing Pro subscription — no separate API key) or directly in claude.ai — feeding in the same batch of recent `content_items` and the same active-topics context described under Input, above. Output follows the identical JSON contract and is loaded into `topics` and `topic_content_items` by hand (Supabase Studio's SQL editor, or a small local script using the service-role key) rather than by an automated write. Cadence moves from every 6 hours to whatever the founder sets — weekly is a reasonable starting point given no real reader base yet. Nothing about the continuity-resolution logic below changes; it's the same judgment call, made by a human running the same prompt instead of an unattended job.

### Topic continuity

This is the highest-uncertainty component of the entire pipeline, and it isn't optional: a synthesizer that can't tell "AI datacenter power demand" (detected at T) from "Utilities strained by AI buildout" (detected at T+3h) fragments every downstream narrative into duplicates, and a topic that fragments can't carry a thesis, a portfolio, or a track record (ADR-0001, D-12).

Every `synth/` run receives the full set of currently `active` topics as context, and every output must resolve to exactly one of:

- **Update.** The batch's content continues an existing tracked topic. `resolution: "update"`, with that topic's `topic_id`. `topics.last_updated_at` refreshes; new content links via `topic_content_items`.
- **Create.** The batch's content represents a genuinely new narrative not already being tracked. `resolution: "create"`, `topic_id: null` — the application generates a new id.

**Merge rule.** If two previously-separate active topics are later recognized as the same narrative — a real possibility this early in the pipeline's life — the older topic (by `first_detected_at`) is treated as canonical; the newer one's supporting content is relinked to it via `topic_content_items`, and the newer topic's row flips to `archived` with a note recording the merge. This is a manual or semi-manual review step during the beta, not a fully automated one — a wrong automated merge is worse than a missed one.

**Archive rule.** A topic with no newly linked content for a set number of days (an initial default of 5–7 days, tunable once real data exists) flips from `active` to `archived`. Archiving a topic doesn't touch any thesis or position already generated from it — those continue to run against the fixed 90-day holding rule regardless of the topic's current status (`docs/DATA_MODEL.md`, The 90-day holding rule).

**Escalation path.** If prompt-level continuity — passing active topics as context and asking the model to resolve update-or-create — doesn't hold up against real ingested data, `pgvector`-based embedding similarity is the fallback: embed each new batch of content, compare against embeddings of active topics' summaries, and use similarity as a pre-filter or a second opinion alongside the prompt. This is the one place the "no vector database" architecture decision might need revisiting, and `pgvector` living inside the same Postgres instance means revisiting it doesn't mean standing up new infrastructure (`docs/ARCHITECTURE.md`; `docs/MVP_SCOPE.md`).

### Momentum

Momentum is not something this agent produces — it's a query the application runs, separate from any model call: `count(content_items linked to a topic in the trailing 48h)` compared against a trailing baseline for that same topic. Stored nowhere, computed at read time, trivially auditable (ADR-0001, D-06).

This resolves a real contradiction in the original plan, which paired a persisted `momentum_score` output field with a dedicated `SentimentSnapshot` table, while `docs/RISKS.md` calls mention-and-sentiment tracking commoditized and explicitly warns against disproportionate investment there. There is no sentiment-scoring subsystem anywhere in this pipeline.

## Agent 3: thesis generator

**Responsibility:** given a topic that has crossed a momentum threshold, produce a falsifiable investment thesis in the ten-section structure of ADR-0003 (D-25), as one structured object. Section 10 of that structure, the results at 30, 60 and 90 days, is not model output (see below).

**Model:** Claude Opus 4.8 — reserved for this stage specifically, because thesis quality has the most product impact of anything this pipeline produces (`docs/VISION.md`, Why this is useful before the track record exists).

**Input:** the topic (summary, citations, linked companies); real market data for those companies (recent price action, trailing returns) pulled from `price_snapshots`; an **as-of date** for every price and fact; and the primary sources (company releases and filings, regulator orders, exchange or Treasury data) that the founder-run session has fetched for the claims the thesis rests on (ADR-0004, D-35).

**Output:**
```json
{
  "title": "string",
  "as_of": "YYYY-MM-DD",
  "hypothesis": "string",
  "why_now": "string",
  "market_missing": "string",
  "bull_case": "string",
  "bear_case": "string",
  "valuation": "string",
  "catalysts": [{"date": "YYYY-MM-DD | undated", "event": "string"}],
  "invalidation_conditions": [{"condition": "string", "threshold": "string"}],
  "risks": ["string"],
  "benchmark": {
    "ticker": "SPY",
    "sector_ticker": "string | null",
    "outperformance_pct_points": 5,
    "reason": "string"
  },
  "suggested_basket": [{"ticker": "VZ", "weight": 0.4, "rationale": "string"}],
  "basket_weighting": "equal | conviction",
  "confidence": "low | medium | high",
  "citations": [
    {
      "n": 1,
      "content_item_id": "uuid | null",
      "source_url": "string",
      "publisher": "string",
      "headline": "string",
      "published_at": "timestamp",
      "retrieved_at": "timestamp | null",
      "paraphrase": "string",
      "source_type": "primary | secondary",
      "unverified": false
    }
  ],
  "caveat": "This is a hypothesis for tracking purposes, not a recommendation."
}
```

The fields map onto ADR-0003's sections as follows: `hypothesis` (1), `why_now` (2), `market_missing` (3), `bull_case` (4), `bear_case` (5), `valuation` (6), `catalysts` (7), `invalidation_conditions` (8), `benchmark` and `suggested_basket` (9). Facts in the text fields carry a marker `[n]` that points at `citations[].n`, the convention write-up 13 already uses.

**Rules the output must meet.** Structured-output validation checks what a schema can check; the rest is read by the founder and, from M2 on, by the golden set (below). The checks are implemented in `jobs/thesis/` (`python -m thesis path/to/thesis.json`); write-up 13 converted into this contract is its first fixture (`jobs/tests/fixtures/thesis_13.json`).

- **Hypothesis (D-26).** One sentence, first, naming the basket, the benchmark, the 90-day window, the threshold and the mechanism. Checked as one sentence by validation; whether it is falsifiable is a read, not a schema check.
- **Benchmark (D-27).** A named benchmark, a threshold in percentage points stated in advance, and the reason for that benchmark. `sector_ticker` is the thematic or sector ETF that `performance_snapshots.sector_benchmark_ticker` expects (`docs/DATA_MODEL.md`, Dual benchmarks); it is `null` when no clean ETF exists, as for write-up 13, and `reason` then says so. How `performance_snapshots` records a synthetic comparison basket in that case (write-up 13 would need one, as its secondary comparison) is an open M2 schema question.
- **Valuation (D-28).** What each linked company trades at (a multiple, against history, peers or growth where feasible) and one sentence on what that implies the market already believes.
- **Catalysts (D-29).** At least one, and at least one with a date inside the holding window.
- **Invalidation conditions (D-30).** At least one, each an observable threshold ("wrong if X"), distinct from the risks.
- **Risks (D-31).** Portfolio mechanics and external risks the bear case does not cover; an item that restates the bear case is cut. Read in QA, not checked by schema.
- **Basket (D-32).** Weights sum to 1. `basket_weighting` is `equal` only when the thesis text makes no differentiated claim about its components; otherwise it is `conviction`, each weight has a `rationale` taken from the thesis's own argument, and a name may be left out. The weights are the thesis's own judgment and are the same for every reader: no input, field or prompt carries anything about a reader, so the basket stays impersonal (`docs/RISKS.md`, publisher's exclusion). A pair or relative-value framing needs a short leg, which `positions` does not have (`docs/DATA_MODEL.md`); until it does, differentiated conviction is expressed by weights or by leaving a name out.
- **Sources (D-33, D-35).** Every factual claim is checked against a primary source or labelled unverified, in the form write-up 13 uses for its $8 billion figure (a Wall Street Journal report relayed by Forbes, treated as unconfirmed). Each citation carries `source_type` and `unverified`; a claim backed only by a secondary source has `unverified: true` and is written as unconfirmed. Every `[n]` in the text resolves to a citation and every citation is used. `content_item_id` names a stored item, and is `null` only for a source the session fetched itself (a primary source, or a secondary one that is not in `content_items`, as most of write-up 13's were), and then `retrieved_at` is set. A load-bearing fact older than a few weeks relative to publication is flagged with its as-of date; the threshold for "a few weeks" is fixed when the prompt is written and recorded in `prompt_version`.
- **Paraphrase (ADR-0001, D-15).** Every citation requires a paraphrase, never a quoted excerpt of the source material; the prompt instructs the model to restate the supporting claim in its own words, and validation rejects a citation that looks like a near-verbatim copy of `content_items.body`. This exists so the product never republishes third-party article text it has no license to republish (`docs/RISKS.md`).

**What is not model output.** `starting_value` and `holding_period_days` are fixed system parameters the application attaches when a thesis is published (`docs/DATA_MODEL.md`). The results section (ADR-0003, D-25, section 10) is written after publication: the numbers come from `perf/` against `price_snapshots`, and the four-way explanation (thesis wrong, thesis right but priced in, catalyst did not occur, market moved for unrelated reasons) is written by the founder, never by a model grading its own or another thesis (`AGENTS.md` §7; Evaluation engine below).

**Storage.** The `theses` table has columns for the earlier fields only (`docs/DATA_MODEL.md`). The new fields (`title`, `as_of`, `hypothesis`, `why_now`, `market_missing`, `valuation`, `catalysts`, `invalidation_conditions`, `benchmark`, `basket_weighting`, the `rationale` in each basket item, and the new keys in each citation) need an M2 migration; whether they become columns or one JSONB document is decided with that migration, and `docs/DATA_MODEL.md` is not changed here.

**Free-tier-first execution mode (ADR-0002, D-20):** as with Agent 2, this runs as a founder-triggered session through Claude Code or claude.ai rather than a scheduled Opus 4.8 API call, during the free-tier-first MVP. Same input, same output contract, same citation-as-paraphrase rule. The founder reviewing every thesis before it's loaded into `theses` and published is a natural byproduct of running the prompt personally, not an extra step — it folds directly into the weekly manual QA sampling described below.

## Evaluation engine (not AI)

The mechanism that actually judges whether a thesis was any good is not a model — it's arithmetic. The `perf/` job (`docs/ARCHITECTURE.md`; `docs/DATA_MODEL.md`) tracks each thesis's hypothetical position values against `price_snapshots` going forward, against both fixed benchmarks (`docs/DATA_MODEL.md`, Dual benchmarks) — never against a single benchmark alone, since a rising market by itself would make every thesis look prescient regardless of whether the underlying narrative call was any good. This is deterministic, auditable, and is the entire mechanism behind the product's accountability claim. Do not use an LLM to grade its own — or another thesis's — accuracy; use real subsequent market data as ground truth. This job has no LLM involvement at all, and is unaffected by free-tier-first: it already runs fully automated, on schedule, at zero marginal cost.

The holding rule that governs every position (`docs/DATA_MODEL.md`, The 90-day holding rule) is fixed in advance of the first position ever opening, and is never adjusted retroactively. If the rule itself is ever revisited — a different holding period, a different benchmark pair — the change is written down and logged, and it applies only to theses published after the change. Positions already open finish out under the rule that opened them (ADR-0001, D-13).

This only works as a differentiator if losing theses are shown as prominently as winning ones. Quietly de-emphasizing or stopping updates on theses that didn't pan out defeats the entire premise the product is built on (`docs/VISION.md`, The one rule that makes this real; `docs/RISKS.md`, Survivorship bias).

## Hallucination mitigation

- **Grounding.** Every prompt includes the actual retrieved facts (source excerpts, real price data) and instructs the model to use only what's provided — never to recall unsourced facts about a company from its own training.
- **Structured output.** Every agent output is validated against its JSON schema; invalid output triggers a retry, not a silent pass-through to the database.
- **Citations, not assertions.** Every claim in a thesis is expected to trace back to a `content_item` via the `citations` field — a paraphrase plus source metadata, never a verbatim excerpt (`docs/DATA_MODEL.md`; ADR-0001, D-15). A claim without a citation is a signal something went wrong upstream.
- **Facts vs. inference.** Prompts separate what the source material actually says from what the model is inferring, so the UI can label each differently and readers can calibrate trust accordingly.
- **Falsifiable language, not hedging.** System prompts ask for plain, testable statements. The hypothesis and the invalidation conditions carry the uncertainty as thresholds and dates, not as scattered "could" and "may": a thesis written to be true in almost any outcome defeats the purpose of publishing losers (ADR-0003, Context). A fact the sources do not settle is marked `unverified`, not softened, and every thesis still carries the "hypothesis, not advice" caveat as a first-class field, not just UI copy.
- **Versioning.** Every generation logs `model_used` and `prompt_version` (`docs/DATA_MODEL.md`) — kept deliberately, against the instinct to trim them, because they're the only mechanism making a post-hoc quality regression diagnosable after a model or prompt change (ADR-0001, D-05). During free-tier-first, recording these two fields is the founder's responsibility when loading a generation by hand — there's no automated harness doing it on their behalf, which is exactly why this stays a hard rule rather than a nice-to-have (`docs/ARCHITECTURE.md`, Load-bearing invariants).
- **Golden-set regression testing.** A fixed set of inputs with known-good output characteristics — schema validity and the rule checks of the Agent 3 contract (a one-sentence hypothesis, at least one dated catalyst and one invalidation condition, basket weights that sum to 1, every `[n]` marker resolving to a citation), no fabricated tickers outside the provided context, correct update-or-create resolution against a fixed set of active topics, and citations that read as paraphrases rather than near-verbatim excerpts — is run against the pipeline before any prompt change ships. During free-tier-first (ADR-0002), this check is run by the founder locally before a prompt change, rather than as an automated CI gate — same check, same bar, just not unattended yet. From M2 on, the set is built from the cases in `m0/intervention-log.md`: the five substantive corrections in write-ups 8, 9 and 13 (a stale premise, a favoured carrier that changed, an announcement date and price, a percentage on a dividend-adjusted basis, a consideration stated as cash only) and the support-level removals, so that a prompt change that reintroduces one of them is caught before it ships (ADR-0004, D-35).
- **Manual QA sampling.** During the beta, a sample of generated theses is read manually every week against a short rubric — grounded, non-generic, correctly cited — to catch regressions automated tests won't (`docs/MVP_SCOPE.md`). During free-tier-first, this happens as a natural byproduct of the founder running every generation personally (D-20), rather than as a separate sampling step layered on top of an unattended pipeline.

## Evaluating AI-generated ideas

The performance-tracking loop described above is the primary evaluation mechanism — real subsequent market data, not another model's opinion. During the beta, supplement it with the manual QA rubric above, applied consistently so prompt or model changes can be compared against a stable baseline rather than a moving target.

Historical runs — generating theses against past data to sanity-check the pipeline — are useful and encouraged, but strictly for internal QA: does the output validate against schema, stay grounded in the retrieved facts, avoid generic phrasing? A backtested performance figure is never published, quoted, or shown in-product, under any framing (ADR-0001, D-02). A model generating a thesis about a past event has already read how that event turned out; publishing a performance number built on that is the exact AI-washing pattern `docs/RISKS.md` warns about, not a shortcut around the fact that the real track record takes real elapsed time to accumulate (`docs/VISION.md`, Why this is useful before the track record exists).

## Cost model

**Free-tier-first note (ADR-0002, D-20, D-24):** the estimate below describes the fully automated pipeline's cost once reinstated. During the free-tier-first MVP, `extract/`'s LLM fallback and the `synth/`/`thesis/` calls don't run against the metered API at all — actual spend is $0/month, because these stages run as founder-triggered Claude Code/claude.ai sessions under the existing Pro subscription instead. The figures below stay worth keeping accurate and current regardless, since they define exactly what "reinstated" costs, and that number is one of D-24's own reinstatement signals.

A concrete estimate, not just a qualitative warning — an hour of arithmetic now is what tells us whether this pipeline is a hobby-scale expense or a problem-scale one, once it's running (ADR-0001, D-16).

**Assumptions**, stated explicitly so they can be corrected once M1 produces real ingestion data:

| Stage | Model | Volume | Input tokens/call | Output tokens/call | Calls/day |
|---|---|---|---|---|---|
| Extraction | Haiku 4.5 | ~200 items/day, batched ~25/call | ~20,000 | ~2,000 | ~8 |
| Topic synthesis | Sonnet 5 | Every 6 hours, ~60 items + active-topic context | ~20,000 | ~2,000 | 4 |
| Thesis generation | Opus 4.8 | ~3 theses/day | ~10,000 | ~1,200 | 3 |

**Estimated spend**, at current published API rates as of this writing — Haiku 4.5 $1/$5, Sonnet 5 $3/$15 standard (introductory $2/$10 through August 31, 2026), Opus 4.8 $5/$25, all per million input/output tokens. Reverify against current rates before committing to a cap; these change.

| Stage | Standard rate/day | With Batch API (−50%)/day |
|---|---|---|
| Extraction | ~$0.24 | ~$0.12 |
| Topic synthesis | ~$0.36 | ~$0.18 |
| Thesis generation | ~$0.24 | ~$0.12 |
| **Total** | **~$0.84/day** | **~$0.42/day** |

Roughly **$25/month at standard rates, ~$13/month routed through the Batch API** — every job in this pipeline runs in the background with no latency requirement (`docs/ARCHITECTURE.md`), which is exactly the workload the Batch API's 50% discount exists for, so there's little reason not to use it once this path is reinstated.

This is a hobby-scale expense at the stated assumptions, not a problem-scale one — though, per ADR-0002, "hobby-scale" and "acceptable" are no longer the same test during the free-tier-first MVP specifically. The assumptions are estimates, not commitments, and should be recalibrated the moment real ingestion volume exists.

**The cap, not the estimate, is what actually protects the budget.** A daily spend cap — an initial $10/day, roughly 12–25x the modeled spend above, chosen for headroom rather than precision — is enforced in code, not just monitored by an alert. Every job checks logged spend against the cap before making a call; if the cap is breached, generation halts for the remainder of the day rather than degrading silently, and the halt itself raises a Sentry alert (ADR-0001, D-16). Raising the cap is a deliberate configuration change, never an emergency workaround typed in at 2 a.m. This cap should be written into the codebase now, even while dormant, so it's already in place the moment the automated path is reinstated (ADR-0002, D-24) rather than something to build under time pressure later.

Every generation logs token counts and cost, tagged with the job, the model, and the prompt version, so a cost regression is as traceable as a quality one (`docs/ARCHITECTURE.md`, Load-bearing invariants) — once there's metered spend to log. During free-tier-first there's no token cost to track, since generation runs under the Pro subscription rather than the API; `model_used` and `prompt_version` are still recorded by hand for every generation regardless (see Versioning, above).
