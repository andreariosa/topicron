-- M1a (ADR-0004, D-34): the two tables the daily prices job needs.
-- Shapes follow docs/DATA_MODEL.md. Everything else in the schema arrives with its own milestone.

create table public.companies (
  id uuid primary key default gen_random_uuid(),
  ticker text not null,
  name text not null,
  sector text,
  exchange text not null,
  -- The prices job upserts on this pair, so it must be unique.
  constraint companies_ticker_exchange_key unique (ticker, exchange)
);

create table public.price_snapshots (
  company_id uuid not null references public.companies (id),
  date date not null,
  open numeric not null,
  high numeric not null,
  low numeric not null,
  close numeric not null,
  -- Nullable on purpose: Finnhub's free /quote has no volume (docs/DATA_MODEL.md).
  volume bigint,
  -- One bar per company and session; this is what makes the job safe to re-run.
  primary key (company_id, date),
  constraint price_snapshots_positive check (open > 0 and high > 0 and low > 0 and close > 0),
  constraint price_snapshots_range check (low <= high)
);

-- Supabase exposes every table in the public schema through its REST API.
-- Row-level security with no policy means the public (anon) key can read and write nothing.
-- The jobs use the secret key, which bypasses RLS. A read policy is added in M4, when the
-- public pages need one, and not before.
alter table public.companies enable row level security;
alter table public.price_snapshots enable row level security;
