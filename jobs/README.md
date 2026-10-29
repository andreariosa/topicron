# jobs/

Scheduled jobs for Topicron, run by GitHub Actions (`docs/ARCHITECTURE.md`, ADR-0001 D-04). Python 3.12, standard library only at runtime. `ruff`, `mypy` and `pytest` are development and CI tools only: they are the lint, type-check and test steps `CONTRIBUTING.md` section 3 asks for, and `CURSOR_RULES.md` section 3 names `ruff`.

```
jobs/
├── common/        shared clients: finnhub.py (/quote), supabase_rest.py (PostgREST)
├── prices/        the daily prices job (M1a)
├── ingest/        the hourly RSS ingestion job (M1b)
└── tests/
```

More jobs (`extract/`, `perf/`, `digest/`) join this folder in later milestones, each with a `main()` the scheduler calls (`CURSOR_RULES.md` section 3).

## prices (M1a, ADR-0004 D-34)

Records one daily bar per tracked company in `price_snapshots`. The tracked set is `prices/universe.py` (VZ, T, TMUS and the SPY benchmark): adding a ticker is a reviewed change, and it must be US-listed (Finnhub's free plan has no non-US quotes).

**Where the bar comes from.** Finnhub's free plan has no daily candles, so the bar is built from `/quote`: open, high, low, current price, previous close and the time of the last trade. The quote has no volume, so `volume` stays empty.

**Which date a row gets.** The New York date of the quote's own timestamp, not the date the job runs. That makes every run idempotent and needs no market calendar: a run on a weekend, on a holiday or the next morning sees the last session again and upserts the same row. The 06:30 UTC run exists for that reason: it refills an evening run that was dropped.

**What it refuses to do (and fails loudly instead).**

- Write while the US session is open (weekdays 09:30 to 16:00 New York): that quote is not a close.
- Write a quote whose close or open is outside the day's high-low range, or whose open, high or low is zero.
- Stay green when the next day's previous close differs from the close it stored for that session (only checked when the stored row is the immediately preceding weekday). The rows are written first, then the run fails, so the problem shows up in GitHub's failed-run email.

Holidays are not modelled. A manual run inside the session window on a holiday is refused, which is harmless.

**Secrets.** Only as GitHub Actions secrets (repository settings), never in the repository, the logs or the chat:

| Secret | Used for |
|---|---|
| `FINNHUB_API_KEY` | Finnhub `/quote`, sent in a header |
| `SUPABASE_URL` | the project URL (`https://...supabase.co`) |
| `SUPABASE_SECRET_KEY` | the new `sb_secret_...` key; it bypasses row-level security |

**Run it.** In GitHub: Actions, Prices, Run workflow. The `dry_run` box is ticked by default: it fetches and prints the rows and writes nothing (it needs only `FINNHUB_API_KEY`). Untick it for a real run. Locally, with the key exported in your own shell:

```
cd jobs
FINNHUB_API_KEY=... python -m prices --dry-run
```

## ingest (M1b, ADR-0004 D-34)

Reads the curated RSS feeds listed in `ingest/feeds.py` and stores each item once in `content_items`. Hourly (`.github/workflows/ingest.yml`), zero LLM cost. Ticker extraction is a separate, later step.

**The feed list is code.** `ingest/feeds.py` holds each feed's `source` id, URL, an age limit and an `active` flag (`docs/DATA_MODEL.md`: sources are a config file, not a table). Adding a feed is a reviewed change that comes after reading the publisher's robots.txt and terms; what was found for each feed is in `m0/rss-feeds.md`. A `source` id is part of the dedupe key and is never renamed.

**What is stored.** Title, link, the feed's own short description (tags stripped, no article page is ever fetched), author when the feed has one, publication time, and the publisher's category tags in `raw_metadata`. The standard-library parser accepts RSS 2.0 only and refuses a document with a DTD or larger than 5 MB.

**Dedupe.** The key is `(source, external_id)`, where `external_id` is the feed's guid, or its link when there is none. The job inserts with `ON CONFLICT DO NOTHING`: the first copy of an item is kept as ingested, a later edit by the publisher does not change it, and a re-run adds nothing. Matching the same article across two different feeds is not done yet; it comes with the second feed.

**What it refuses to do (and fails loudly instead).**

- Stay green when a feed errors, is not valid RSS 2.0, or parses to no usable item.
- Stay green when a feed's newest item is older than its `max_age_hours` (72 by default): a feed that went quiet would feed stale news to the pipeline.
- Trust an item dated more than an hour in the future (it is skipped).

Items that cannot be used (no title, no http(s) link, no readable date) are skipped and counted in the log, not hidden. Whatever could be written is written first, then the run raises, so one bad feed does not hide the others. GitHub sends a failed-run email for each failed run (subject to the account's notification settings), so a dead feed means an email on every hourly run until it is fixed or switched off.

**Secrets.** `SUPABASE_URL` and `SUPABASE_SECRET_KEY`, the same two as the prices job. No other key.

**Run it.** In GitHub: Actions, Ingest, Run workflow. The `dry_run` box is ticked by default: it fetches and parses the feeds, prints the counts, the newest and oldest dates and the first three items, and writes nothing (it needs no secret). Untick it for a real run. Locally: `cd jobs && python -m ingest --dry-run`.

## Checks

```
cd jobs
pip install -r requirements-dev.txt
ruff check . && ruff format --check . && mypy . && pytest
```

CI (`.github/workflows/ci.yml`) runs the same four commands as the `jobs` check, and `npm run lint` plus `tsc` as the `web` check.
