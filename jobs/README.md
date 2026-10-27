# jobs/

Scheduled jobs for Topicron, run by GitHub Actions (`docs/ARCHITECTURE.md`, ADR-0001 D-04). Python 3.12, standard library only at runtime. `ruff`, `mypy` and `pytest` are development and CI tools only: they are the lint, type-check and test steps `CONTRIBUTING.md` section 3 asks for, and `CURSOR_RULES.md` section 3 names `ruff`.

```
jobs/
├── common/        shared clients: finnhub.py (/quote), supabase_rest.py (PostgREST)
├── prices/        the daily prices job (M1a)
└── tests/
```

More jobs (`ingest/`, `extract/`, `perf/`, `digest/`) join this folder in later milestones, each with a `main()` the scheduler calls (`CURSOR_RULES.md` section 3).

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

## Checks

```
cd jobs
pip install -r requirements-dev.txt
ruff check . && ruff format --check . && mypy . && pytest
```

CI (`.github/workflows/ci.yml`) runs the same four commands as the `jobs` check, and `npm run lint` plus `tsc` as the `web` check.
