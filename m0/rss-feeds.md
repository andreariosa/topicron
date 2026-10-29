# RSS Feeds (M0, finalized — for M1's ingestion connector)

*A curated, editorially-appropriate source list, not a comprehensive one — commoditized sentiment-tracking tools already aggregate everything; Topicron's edge is in synthesis and accountability, not feed breadth (`docs/VISION.md`).*

**Confidence note:** the sources below are confirmed currently active via a curated, recently-updated RSS directory. A few exact feed URLs were truncated in that source and are marked below — grab the precise URL directly from the publisher (most expose a link or `<link rel="alternate" type="application/rss+xml">` tag on their site) before wiring these into the M1 ingestion connector; don't hand-guess a truncated URL into production code.

## Confirmed, complete feed URLs

| Source | Feed URL | Fit |
|---|---|---|
| MarketBeat | `https://www.marketbeat.com/feed/` | Real-time ratings, earnings, dividend data — good breadth |
| Benzinga | `https://feeds.benzinga.com/benzinga` | Fast-moving market news, sector-taggable |
| Financial Times (International) | `https://www.ft.com/rss/home/international` | High editorial bar, strong macro/markets coverage |

## Confirmed active, exact path needs a quick grab from the publisher

| Source | Why it's worth the extra minute |
|---|---|
| CNBC Market Insider | Daily markets-moving-events digest — strong fit for the "why is this trending" framing Agent 2 needs |
| The Motley Fool (Investing News) | Long-form, thesis-style writing — closest tonal match to Topicron's own voice among mainstream outlets |
| Yahoo Finance | Broad company-level coverage, useful for the ticker-extraction step |
| Wall Street Journal (Business) | High editorial bar; confirm access terms before relying on it for full-text ingestion, not just headlines |

## Deliberately not included (with reason)

- **Reuters, Bloomberg** — both now push users toward "Generate RSS" third-party scraping services rather than offering a stable native feed; fragile as an ingestion dependency and worth revisiting once a name-brand macro source is genuinely needed, not before.
- **Generic "top 100" aggregator lists** — including everything a directory recommends would recreate the same commoditized sentiment-tracking problem `docs/VISION.md` explicitly positions against.

## Before M1 wires this in

1. Pull the exact feed URL for each "needs a quick grab" row above directly from the publisher.
2. Spot-check each feed's actual XML in a browser or `curl` once — a directory listing confirms a feed *exists*, not that its current structure matches what the ingestion connector expects to parse.
3. Revisit this list once M1's dedupe/ticker-extraction step is built — the right feed count depends on how well that step performs, not on maximizing source count up front.

## Checked before wiring in (M1b, 2026-10-29)

Robots.txt and terms were read by Claude through a fetch tool that returns summaries and short excerpts, not the full pages, and that can serve an old cached copy of a page. The founder confirms the wording of the terms below before any commercial use.

**The probe.** A directory listing confirms a feed *exists*, not that it answers (see "Before M1 wires this in", step 2), so each feed was tried once from GitHub's runners with the Ingest workflow's probe mode (`dry_run` and `include_inactive`). A first normal dry run earlier the same day had failed on MarketBeat ("The read operation timed out", nothing written), and in the founder's browser MarketBeat answered 503. Result of the probe, 2026-10-29 about 14:00 Rome:

| Source id | Result | Decision |
|---|---|---|
| `marketbeat` | Answered: 100 items, 21 to 29 October, newest 5 h old. Intermittent (timeout and 503 hours earlier) | **Switched on**, with two retries (5 s and 15 s) on timeouts and 5xx |
| `fed-press` | Answered: 20 items, newest 19 h old (FOMC statement) | **Switched on** |
| `cnbc-top` | Answered: 30 items, fresh | **Switched on by the founder's decision**; robots.txt and terms not read by Claude (its tool could not load them) |
| `yahoo-tickers` | Answered: 19 items, fresh, about T-Mobile and AT&T | **Switched on by the founder's decision**; robots.txt of its host and terms not read by Claude |
| `marketwatch-top` | Answered: 10 items, fresh (the feed holds only the latest ten, about 90 minutes at midday) | **Switched on by the founder's decision**; robots.txt and terms not read by Claude. An hourly run that GitHub delays by a few hours misses some stories |
| `nasdaq-markets` | Timed out | Off: retry in a later probe; its robots.txt has no rule against `/feed/` |
| Benzinga | The server closes the TLS connection (from GitHub and from the founder's browser) | Dropped from the list; its robots.txt stays unread |
| `cnbc-finance` | Answered, but the newest item was 8 days old: a stopped feed | Dropped |
| `yahoo-finance` (`/news/rssindex`) | HTTP 404 | Dropped |
| Financial Times | Not tried | Not wired in: paywalled, terms unreadable. Revisit only for a headline-and-link use |

An earlier version of these notes read a copy of the MarketBeat feed in Claude's fetch tool that ended on 21 September 2026 as a sign the feed had stopped. That was an old cached copy; the live feed is current.

**MarketBeat.** The feed is RSS 2.0 with no namespaces. Each item has title, link, a `guid` (`isPermaLink="false"`), `pubDate`, a description of about 190 characters, and one or two `category` elements holding tickers (several tickers in one category, separated by a line break; some items list a dozen). No author. `robots.txt` has no rule against `/feed/` (its `*/rss-feeds/*` rule concerns the directory page of feeds, which the job never fetches), and it carries the content signals `search=yes, ai-input=yes, ai-train=yes`. `llms.txt` allows use for AI purposes and says: cite MarketBeat as the source and link back to the original page with each citation. The Terms of Service say nothing about RSS or AI; they grant a personal licence and forbid resale, reproduction for commercial purposes and bulk redistribution of MarketBeat's data.

**Federal Reserve.** Its disclaimer page says the information on the Board's website is in the public domain and may be copied and distributed without permission, and asks users to cite the Board as the source. Third-party material on the site and the Board's seals and logos are excluded. The feed is `press_all.xml`, listed on its feeds page; its items carry a category such as "Monetary Policy". It publishes a few items a month, so its age limit is 14 days instead of 72 hours.

**Rule for news items (confirmed by the founder's merge of the pull request that proposed it, 2026-10-29):** store only what the feed publishes (headline, link, short description, tags); never fetch the article page; public pages show an item only as the source name, the headline and a link to the original page, never the description text; a thesis citation names the source and links to the article, as `docs/AI_SYSTEM.md` already requires of every citation. Do not resell or export the stored items in bulk. This is the default for any feed added later until its own terms are read.

**CNBC Top News, Yahoo Finance (VZ, T, TMUS) and MarketWatch (switched on 2026-10-29 by the founder).** Claude could not read their robots.txt or terms (its tool could not load them or was refused), so the reading is the founder's: open `https://www.cnbc.com/robots.txt`, `https://feeds.finance.yahoo.com/robots.txt` and `https://feeds.content.dowjones.io/robots.txt` and check that no rule under `User-agent: *` covers the feed path; if one does, the feed goes back to `active=False`. News-site RSS terms commonly allow personal, non-commercial use only; the founder has decided to proceed, and the rule for news items above is what limits the exposure (private table, no article text, headline and link only in public). Result of the founder's reading: to be recorded here.
