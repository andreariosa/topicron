# jobs/

Scheduled jobs for Topicron, run by GitHub Actions (`docs/ARCHITECTURE.md`, ADR-0001 D-04). Python 3.12, standard library only at runtime. `ruff`, `mypy` and `pytest` are development and CI tools only: they are the lint, type-check and test steps `CONTRIBUTING.md` section 3 asks for, and `CURSOR_RULES.md` section 3 names `ruff`.

```
jobs/
├── common/        shared clients: finnhub.py (/quote), supabase_rest.py (PostgREST)
├── prices/        the daily prices job (M1a)
├── ingest/        the hourly RSS ingestion job (M1b)
├── extract/       the hourly company-matching job (M1b)
└── tests/
```

More jobs (`perf/`, `digest/`) join this folder in later milestones, each with a `main()` the scheduler calls (`CURSOR_RULES.md` section 3).

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

Reads the curated RSS feeds listed in `ingest/feeds.py` and stores each item once in `content_items`. Zero LLM cost. Matching the items to companies is a separate job (`extract`, below). It runs hourly (`.github/workflows/ingest.yml`, minute 17), and by hand from the Actions tab. Six feeds are switched on (MarketBeat, the Federal Reserve's press releases, CNBC Top News, MarketWatch and the AT&T and Verizon newsrooms); the others in `feeds.py` are off, among them Yahoo Finance for VZ, T and TMUS, whose robots.txt disallows every robot (see `m0/rss-feeds.md`).

**The feed list is code.** `ingest/feeds.py` holds each feed's `source` id, URL, an age limit and an `active` flag (`docs/DATA_MODEL.md`: sources are a config file, not a table). Adding a feed is a reviewed change that comes after reading the publisher's robots.txt and terms; what was found for each feed is in `m0/rss-feeds.md`. A `source` id is part of the dedupe key and is never renamed.

**What is stored.** Title, link, the feed's own short description (tags stripped, no article page is ever fetched), author when the feed has one, publication time, and the publisher's category tags in `raw_metadata`. The standard-library parser accepts RSS 2.0 only and refuses a document with a DTD or larger than 5 MB. Dates are RFC 2822 as the standard library reads them, plus Verizon's 12-hour form (`09:12:17 AM EDT`) and `Sept`; any other AM/PM form is skipped rather than read with the AM/PM dropped, which the standard library does without an error. A timeout, a dropped connection or a 5xx answer is tried again after 5 and 15 seconds (three tries in all); a 4xx answer is not, because 403 and 404 mean the publisher said no.

**Dedupe.** The key is `(source, external_id)`, where `external_id` is the feed's guid, or its link when there is none. The job inserts with `ON CONFLICT DO NOTHING`: the first copy of an item is kept as ingested, a later edit by the publisher does not change it, and a re-run adds nothing. Matching the same article across two different feeds is not done yet; it comes with the second feed.

**What it refuses to do (and fails loudly instead).**

- Stay green when a feed errors, is not valid RSS 2.0, or parses to no usable item. The error shows how the response started, so a block page is recognisable.
- Stay green when no feed is active at all.
- Stay green when a feed's newest item is older than its `max_age_hours` (72 by default): a feed that went quiet would feed stale news to the pipeline.
- Trust an item dated more than an hour in the future (it is skipped).

Items that cannot be used (no title, no http(s) link, no readable date) are skipped and counted in the log, not hidden. Whatever could be written is written first, then the run raises, so one bad feed does not hide the others. GitHub sends a failed-run email for each failed run (subject to the account's notification settings), so a dead feed means an email on every hourly run until it is fixed or switched off. MarketBeat is known to be intermittent, so an occasional red run is expected; a long series is not.

**Secrets.** `SUPABASE_URL` and `SUPABASE_SECRET_KEY`, the same two as the prices job. No other key.

**Try a feed before switching it on (probe mode).** A feed that works in a browser may still not answer GitHub's runners, and a feed in a directory may be dead (on 2026-10-29, of nine feeds probed, one had stopped, one returned 404, one timed out and one closed the connection). Run the workflow with `dry_run` and `include_inactive` both ticked (locally: `python -m ingest --dry-run --include-inactive`): it fetches every feed in the list, active or not, writes nothing, and ends with one line per feed saying whether it answered, how many items it had and how old the newest one is. A probe never fails the run, because a failing feed is the answer. It only reads, once per feed, as any feed reader does; a feed is switched on only after its robots.txt and terms have been read (`m0/rss-feeds.md`).

**Run it.** In GitHub: Actions, Ingest, Run workflow. The `dry_run` box is ticked by default: it fetches and parses the feeds, prints the counts, the newest and oldest dates and the first three items, and writes nothing (it needs no secret). Untick it for a real run. Locally: `cd jobs && python -m ingest --dry-run`.

## extract (M1b, ADR-0004 D-34)

Looks at the content items ingested in the last 48 hours and records, in `content_item_company_mentions`, which of the companies in the `companies` table each one mentions. Rules only, zero LLM cost (`docs/AI_SYSTEM.md`, Agent 1). It runs hourly (`.github/workflows/extract.yml`, minute 37, after the ingest job) and by hand from the Actions tab.

**What it matches.** In order of strength: the publisher's own `EXCHANGE:SYMBOL` tag (confidence 1.0), where the exchange has to be the company's own; a symbol written with its exchange, a dollar sign or parentheses (0.9); a name from `extract/aliases.py` in the title (0.8) or in the description (0.6). A bare symbol is never accepted, so "ALL", "ARE", "IT", "ON" and "SO" cannot collide with common words; it is only reported. The confidence is the level of the rule, not a probability. Names are matched without regard to case, and a name inside a longer word does not count. The rules are in `extract/matching.py`, a set of pure functions with no database access.

**Which companies.** Only those in the `companies` table, which the prices job fills from `prices/universe.py`: today VZ, T, TMUS and SPY. A tag that names any other company is counted in the log and not stored. To follow a new company, add it to the prices universe and its names to `extract/aliases.py` (both reviewed changes; a test fails if the two lists differ), then run the job by hand with a longer window to cover the items already stored.

**State and repeats.** There is no "processed" flag. Each run reads a window of recent items (48 hours, so that a run GitHub starts hours late loses nothing) and the primary key `(content_item_id, company_id)` makes a repeat harmless: the first copy of a row is kept, and a changed rule needs the old rows deleted. After a longer outage, run it by hand with a wider window (`--hours`, or the `hours` box in Actions).

**What the log shows.** Items scanned; per company, how many items and which rule found them; the ambiguous cases, one line each with the source and the item's id (never the headline, because the log is public); and the ten most frequent tagged tickers that match no company. The run fails when the `companies` table is empty. Cases the rules cannot settle are not resolved by a model: the model path is deferred (ADR-0002, D-20), so they are for the founder to read.

**Secrets.** `SUPABASE_URL` and `SUPABASE_SECRET_KEY`, as for the other jobs. A dry run needs them too, because it reads the stored items; it writes nothing.

**Run it.** In GitHub: Actions, Extract, Run workflow. `dry_run` is ticked by default: it reads, matches and prints, and writes nothing. Untick it for a real run. Locally: `cd jobs && SUPABASE_URL=... SUPABASE_SECRET_KEY=... python -m extract --dry-run --hours 168`, with the two values taken from your own environment and never typed into a chat.

## Checks

```
cd jobs
pip install -r requirements-dev.txt
ruff check . && ruff format --check . && mypy . && pytest
```

CI (`.github/workflows/ci.yml`) runs the same four commands as the `jobs` check, and `npm run lint` plus `tsc` as the `web` check.
