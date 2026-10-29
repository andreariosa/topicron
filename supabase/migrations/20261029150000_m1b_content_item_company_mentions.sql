-- M1b (ADR-0004, D-34): which companies each content item mentions (docs/DATA_MODEL.md).
-- Written by the hourly extract job; nothing else in the schema changes.

create table public.content_item_company_mentions (
  -- Cascade so that an item can be deleted (it was, for a feed that was switched off)
  -- without first deleting its mentions by hand.
  content_item_id uuid not null references public.content_items (id) on delete cascade,
  company_id uuid not null references public.companies (id),
  -- The rule that found the mention sets this value (jobs/extract/matching.py): 1.0 the
  -- publisher's tag, 0.9 the symbol in the text, 0.8 the name in the title, 0.6 the name in
  -- the description. A rule level, not a probability.
  confidence numeric not null,
  -- One row per item and company; this is what makes the extract job safe to re-run.
  primary key (content_item_id, company_id),
  constraint content_item_company_mentions_confidence check (confidence > 0 and confidence <= 1)
);

-- Same as the other tables: row-level security with no policy, so the public (anon) key can
-- read and write nothing. The job uses the secret key. A read policy comes with M4.
alter table public.content_item_company_mentions enable row level security;
