-- M2 (ADR-0005, D-36): the tables the thesis generator writes to, for the Agent 3 output contract
-- (docs/AI_SYSTEM.md, Agent 3; ADR-0003 D-25 to D-33; ADR-0004 D-35).
--
-- Mixed shape, decided by the founder on 2026-11-25: what the system queries or calculates on is a
-- column (the hypothesis, the as-of date, the weighting, the confidence, the benchmark); prose
-- sections are text columns; the nested lists the contract may still change (catalysts,
-- invalidation conditions, the basket, citations) are JSONB, so adjusting the contract does not
-- need a migration each time. The database checks only the outer shape of the JSONB (an array,
-- not empty). The inner shape is checked by the validator in jobs/thesis/ before a row is loaded.
--
-- `topics` comes in the same migration because `theses.topic_id` points at it. Its shape follows
-- docs/DATA_MODEL.md; topic_content_items, positions and performance_snapshots arrive with the
-- tasks that write them.

create table public.topics (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text not null default '',
  status text not null default 'active',
  first_detected_at timestamptz not null default now(),
  -- Drives the archival rule (docs/AI_SYSTEM.md, Topic continuity).
  last_updated_at timestamptz not null default now(),
  constraint topics_title_not_empty check (length(btrim(title)) > 0),
  constraint topics_status check (status in ('active', 'archived'))
);

create table public.theses (
  id uuid primary key default gen_random_uuid(),
  topic_id uuid not null references public.topics (id),
  -- Kept on purpose (ADR-0001, D-05): the only way to diagnose a quality regression afterwards.
  version int not null default 1,
  generated_at timestamptz not null default now(),
  -- Null until the founder publishes it. One publisher, one moment (ADR-0001, D-05).
  published_at timestamptz,
  -- Auditability across model upgrades and prompt changes (ADR-0001, D-05).
  model_used text not null,
  prompt_version text not null,

  title text not null,
  -- The date every price and fact in the thesis is stated as of (ADR-0003, D-25, section 2).
  as_of date not null,
  -- One falsifiable sentence (ADR-0003, D-26).
  hypothesis text not null,
  why_now text not null,
  market_missing text not null,
  bull_case text not null,
  bear_case text not null,
  valuation text not null,
  risks text[] not null,

  -- Benchmark (ADR-0003, D-27). `benchmark_sector_ticker` is null when no clean ETF exists, as
  -- for write-up 13; how performance_snapshots then records a synthetic comparison basket is
  -- still an open question and is not settled by this migration.
  benchmark_ticker text not null,
  benchmark_sector_ticker text,
  benchmark_outperformance_pct_points numeric not null,
  benchmark_reason text not null,

  -- Basket weights are the thesis's own, the same for every reader (ADR-0003, D-32).
  basket_weighting text not null,
  confidence text not null,

  -- Nested lists; the shapes are in docs/AI_SYSTEM.md, Agent 3, and validated by jobs/thesis/.
  catalysts jsonb not null,
  invalidation_conditions jsonb not null,
  suggested_basket jsonb not null,
  citations jsonb not null,

  -- A first-class stored field, not UI copy (docs/DATA_MODEL.md).
  caveat text not null,

  -- Fixed system parameters the application attaches at publication, never model output
  -- (docs/AI_SYSTEM.md). The notional value is not defined anywhere yet, so it has no default
  -- here: it must be set before a thesis is published, and the check below enforces that.
  starting_value numeric,
  holding_period_days int not null default 90,

  constraint theses_topic_version_key unique (topic_id, version),
  constraint theses_version_positive check (version >= 1),
  constraint theses_hypothesis_not_empty check (length(btrim(hypothesis)) > 0),
  constraint theses_basket_weighting check (basket_weighting in ('equal', 'conviction')),
  constraint theses_confidence check (confidence in ('low', 'medium', 'high')),
  constraint theses_benchmark_threshold check (benchmark_outperformance_pct_points > 0),
  constraint theses_risks_not_empty check (cardinality(risks) >= 1),
  constraint theses_catalysts_list
    check (jsonb_typeof(catalysts) = 'array' and jsonb_array_length(catalysts) >= 1),
  constraint theses_invalidation_conditions_list
    check (
      jsonb_typeof(invalidation_conditions) = 'array'
      and jsonb_array_length(invalidation_conditions) >= 1
    ),
  constraint theses_suggested_basket_list
    check (jsonb_typeof(suggested_basket) = 'array' and jsonb_array_length(suggested_basket) >= 1),
  constraint theses_citations_list
    check (jsonb_typeof(citations) = 'array' and jsonb_array_length(citations) >= 1),
  constraint theses_holding_period_positive check (holding_period_days > 0),
  constraint theses_starting_value_positive check (starting_value is null or starting_value > 0),
  constraint theses_published_has_starting_value
    check (published_at is null or starting_value is not null)
);

-- Same posture as every other table: row-level security on and no policy, so the public (anon) key
-- can neither read nor write. The jobs and the founder's loading use the secret key. A read policy
-- comes with the public pages (M4), and not before.
alter table public.topics enable row level security;
alter table public.theses enable row level security;
