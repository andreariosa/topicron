# AI system design

*This document covers agent responsibilities, input/output contracts, and evaluation. It implements the AI-pipeline decisions in ADR-0001 — D-02, D-05 (versioning fields), D-06, D-12, D-13, D-14, D-15, D-16. System-level job cadence is in [`ARCHITECTURE.md`](ARCHITECTURE.md); schema is in [`DATA_MODEL.md`](DATA_MODEL.md). Decisions are cited inline as "ADR-0001, D-XX."*

## Pipeline shape

Extraction → topic synthesis (with continuity resolution) → thesis generation, all running as background jobs against stored data — the `extract/`, `synth/`, and `thesis/` jobs in `docs/ARCHITECTURE.md`. A separate, non-AI evaluation mechanism (the `perf/` job) closes the loop. No agent framework (LangGraph, CrewAI, AutoGen) — a plain sequential pipeline of typed calls to the Claude API is enough for what is fundamentally a linear process, and is far easier to debug than a framework designed for autonomous multi-step planning.

## Agent 1: entity and ticker extractor

**Responsibility:** identify which companies/tickers a piece of ingested content refers to.

**Model:** Claude Haiku 4.5 — high volume, low complexity per call, the cheapest current tier that handles extraction reliably.

**Input:** raw `content_items` text, run hourly alongside `ingest/`, batched across many items per call rather than issued one at a time.

**Output:**
```json
{
  "tickers": [{"symbol": "NVDA", "confidence": 0.92}],
  "companies_mentioned": ["Nvidia"]
}
```

**Notes:** rule-based matching (ticker regex + a company-alias dictionary) handles most cases cheaply; the model is used only as a fallback for ambiguous cases. Ticker collisions with common words are a real, recurring failure mode here — "ALL", "ARE", "IT", "ON", and "SO" are all real tickers (`docs/RISKS.md`, Entity resolution).

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

**Responsibility:** given a topic that has crossed a momentum threshold, produce a structured investment thesis.

**Model:** Claude Opus 4.8 — reserved for this stage specifically, because thesis quality has the most product impact of anything this pipeline produces (`docs/VISION.md`, Why this is useful before the track record exists).

**Input:** the topic (summary, citations, linked companies) plus real market data for those companies (recent price action, trailing returns) pulled from `price_snapshots`.

**Output:**
```json
{
  "bull_case": "string",
  "bear_case": "string",
  "risks": ["string"],
  "confidence": "low | medium | high",
  "suggested_basket": [{"ticker": "NVDA", "weight": 0.33}],
  "citations": [
    {
      "content_item_id": "uuid",
      "source_url": "string",
      "publisher": "string",
      "headline": "string",
      "published_at": "timestamp",
      "paraphrase": "string"
    }
  ],
  "caveat": "This is a hypothesis for tracking purposes, not a recommendation."
}
```

**Notes:** `suggested_basket` defaults to a naive equal weighting across the linked companies. This is a deliberate choice, not a placeholder for future sophistication: a personalized or conviction-weighted allocation is exactly the kind of tailored, individualized output that risks crossing from "impersonal publisher" into "investment adviser" territory (`docs/RISKS.md`), and a naive equal weight is also simpler to compute and to audit correctly.

Every citation requires a paraphrase, never a quoted excerpt of the source material — the prompt instructs the model to restate the supporting claim in its own words, and structured-output validation rejects a citation object that looks like a near-verbatim copy of `content_items.body` (ADR-0001, D-15). This exists specifically so the product never republishes third-party article text it has no license to republish (`docs/RISKS.md`).

`starting_value` and `holding_period_days` are not part of the model's output — they're fixed system parameters the application attaches when a thesis is published (`docs/DATA_MODEL.md`), not something the model is asked to decide.

## Evaluation engine (not AI)

The mechanism that actually judges whether a thesis was any good is not a model — it's arithmetic. The `perf/` job (`docs/ARCHITECTURE.md`; `docs/DATA_MODEL.md`) tracks each thesis's hypothetical position values against `price_snapshots` going forward, against both fixed benchmarks (`docs/DATA_MODEL.md`, Dual benchmarks) — never against a single benchmark alone, since a rising market by itself would make every thesis look prescient regardless of whether the underlying narrative call was any good. This is deterministic, auditable, and is the entire mechanism behind the product's accountability claim. Do not use an LLM to grade its own — or another thesis's — accuracy; use real subsequent market data as ground truth.

The holding rule that governs every position (`docs/DATA_MODEL.md`, The 90-day holding rule) is fixed in advance of the first position ever opening, and is never adjusted retroactively. If the rule itself is ever revisited — a different holding period, a different benchmark pair — the change is written down and logged, and it applies only to theses published after the change. Positions already open finish out under the rule that opened them (ADR-0001, D-13).

This only works as a differentiator if losing theses are shown as prominently as winning ones. Quietly de-emphasizing or stopping updates on theses that didn't pan out defeats the entire premise the product is built on (`docs/VISION.md`, The one rule that makes this real; `docs/RISKS.md`, Survivorship bias).

## Hallucination mitigation

- **Grounding.** Every prompt includes the actual retrieved facts (source excerpts, real price data) and instructs the model to use only what's provided — never to recall unsourced facts about a company from its own training.
- **Structured output.** Every agent output is validated against its JSON schema; invalid output triggers a retry, not a silent pass-through to the database.
- **Citations, not assertions.** Every claim in a thesis is expected to trace back to a `content_item` via the `citations` field — a paraphrase plus source metadata, never a verbatim excerpt (`docs/DATA_MODEL.md`; ADR-0001, D-15). A claim without a citation is a signal something went wrong upstream.
- **Facts vs. inference.** Prompts separate what the source material actually says from what the model is inferring, so the UI can label each differently and readers can calibrate trust accordingly.
- **Conservative language.** System prompts explicitly avoid confident phrasing ("will," "is going to") in favor of hedged phrasing ("could," "may"), and every thesis carries the "hypothesis, not advice" caveat as a first-class field, not just UI copy.
- **Versioning.** Every generation logs `model_used` and `prompt_version` (`docs/DATA_MODEL.md`) — kept deliberately, against the instinct to trim them, because they're the only mechanism making a post-hoc quality regression diagnosable after a model or prompt change (ADR-0001, D-05).
- **Golden-set regression testing.** A fixed set of inputs with known-good output characteristics — schema validity, no fabricated tickers outside the provided context, correct update-or-create resolution against a fixed set of active topics, and citations that read as paraphrases rather than near-verbatim excerpts — is run against the pipeline before any prompt change ships.
- **Manual QA sampling.** During the beta, a sample of generated theses is read manually every week against a short rubric — grounded, non-generic, correctly cited — to catch regressions automated tests won't (`docs/MVP_SCOPE.md`).

## Evaluating AI-generated ideas

The performance-tracking loop described above is the primary evaluation mechanism — real subsequent market data, not another model's opinion. During the beta, supplement it with the manual QA rubric above, applied consistently so prompt or model changes can be compared against a stable baseline rather than a moving target.

Historical runs — generating theses against past data to sanity-check the pipeline — are useful and encouraged, but strictly for internal QA: does the output validate against schema, stay grounded in the retrieved facts, avoid generic phrasing? A backtested performance figure is never published, quoted, or shown in-product, under any framing (ADR-0001, D-02). A model generating a thesis about a past event has already read how that event turned out; publishing a performance number built on that is the exact AI-washing pattern `docs/RISKS.md` warns about, not a shortcut around the fact that the real track record takes real elapsed time to accumulate (`docs/VISION.md`, Why this is useful before the track record exists).

## Cost model

A concrete estimate, not just a qualitative warning — an hour of arithmetic now is what tells us whether this pipeline is a hobby-scale expense or a problem-scale one, before a single user exists (ADR-0001, D-16).

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

Roughly **$25/month at standard rates, ~$13/month routed through the Batch API** — every job in this pipeline runs in the background with no latency requirement (`docs/ARCHITECTURE.md`), which is exactly the workload the Batch API's 50% discount exists for, so there's little reason not to use it.

This is a hobby-scale expense at the stated assumptions, not a problem-scale one. The assumptions are estimates, not commitments, and should be recalibrated the moment real ingestion volume exists.

**The cap, not the estimate, is what actually protects the budget.** A daily spend cap — an initial $10/day, roughly 12–25x the modeled spend above, chosen for headroom rather than precision — is enforced in code, not just monitored by an alert. Every job checks logged spend against the cap before making a call; if the cap is breached, generation halts for the remainder of the day rather than degrading silently, and the halt itself raises a Sentry alert (ADR-0001, D-16). Raising the cap is a deliberate configuration change, never an emergency workaround typed in at 2 a.m.

Every generation logs token counts and cost, tagged with the job, the model, and the prompt version, so a cost regression is as traceable as a quality one (`docs/ARCHITECTURE.md`, Load-bearing invariants).
