-- M1b (ADR-0004, D-34): the table the hourly ingest job writes.
-- The shape follows docs/DATA_MODEL.md. Sources are a config file (jobs/ingest/feeds.py), not a
-- table, so `source` is plain text matched against that list and is not a foreign key.

create table public.content_items (
  id uuid primary key default gen_random_uuid(),
  source text not null,
  -- The publisher's own id for the item (the feed's guid, or its link when it has none).
  external_id text not null,
  title text not null,
  -- The feed's own short description. The job does not fetch article pages.
  body text not null default '',
  author text,
  url text not null,
  published_at timestamptz not null,
  ingested_at timestamptz not null default now(),
  -- Source-specific fields not otherwise modelled (for now: the publisher's category tags).
  raw_metadata jsonb not null default '{}'::jsonb,
  -- This pair is the dedupe key: the ingest job inserts with ON CONFLICT DO NOTHING on it, so the
  -- first copy of an item is never overwritten and a re-run adds nothing.
  constraint content_items_source_external_id_key unique (source, external_id),
  constraint content_items_title_not_empty check (length(btrim(title)) > 0),
  constraint content_items_url_is_http check (url ~ '^https?://')
);

-- Same posture as the M1a tables: row-level security on and no policy, so the public (anon) key
-- can neither read nor write. The jobs use the secret key, which bypasses RLS. A read policy comes
-- with the public pages (M4), and not before.
alter table public.content_items enable row level security;
