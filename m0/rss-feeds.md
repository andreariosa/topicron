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

Read by Claude through a fetch tool that returns summaries and short excerpts, not the full pages, so the founder confirms the wording of the terms below before any commercial use.

**Result of the first live test, the same day: neither feed from the list above works today.** The first dry run of the Ingest workflow on GitHub failed on MarketBeat with "The read operation timed out" (nothing was written). In the founder's own browser MarketBeat answered "Error 503: Server Error" and Benzinga's host closed the connection (`ERR_CONNECTION_CLOSED`); an earlier attempt on Benzinga returned no response at all. A directory listing confirms a feed *exists*, not that it answers (see "Before M1 wires this in", step 2). Claude's fetch tool still showed a copy of the MarketBeat feed ending on 21 September 2026, which fits a feed that stopped then; one 503 can be transient, so MarketBeat stays in the list, switched off, to be retried.

| Source | Status | What was found |
|---|---|---|
| MarketBeat | In the list, **switched off** (503 and a timeout on 2026-10-29) | The feed is RSS 2.0 with no namespaces. Each item has title, link, a `guid` (`isPermaLink="false"`), `pubDate`, a description of about 190 characters, and one or two `category` elements holding tickers (several tickers in one category, separated by a line break). No author. `robots.txt` has no rule against `/feed/` (its `*/rss-feeds/*` rule concerns the directory page of feeds, which the job never fetches), and it carries the content signals `search=yes, ai-input=yes, ai-train=yes`. `llms.txt` allows use for AI purposes and says: cite MarketBeat as the source and link back to the original page with each citation. The Terms of Service say nothing about RSS or AI; they grant a personal licence and forbid resale, reproduction for commercial purposes and bulk redistribution of MarketBeat's data. |
| Benzinga | In the list, **switched off** | `robots.txt` unread: the host closed the connection in the founder's browser and Claude's tool is blocked from it. Nothing is known about its rules. |
| Financial Times | **Not wired in** | Paywalled, and its terms could not be read. Revisit only if a headline-and-link use is wanted. |

**Candidates for the probe (in `jobs/ingest/feeds.py`, switched off).** These are guesses from public knowledge, not confirmed feeds: each URL is tried once from GitHub's runners in probe mode, and one that does not answer is simply dropped. Yahoo Finance and Nasdaq have a `robots.txt` with no rule against the feed path (read 2026-10-29); for CNBC, MarketWatch, the Federal Reserve and the host of Yahoo's per-ticker feed the file could not be read by Claude's tool. Terms are unread for all of them, and news-site RSS terms commonly allow personal, non-commercial use only, so a feed that answers is still switched on only after its terms are read and the founder decides.

| Source id | URL | Why it is a candidate |
|---|---|---|
| `cnbc-top`, `cnbc-finance` | `https://www.cnbc.com/id/100003114/device/rss/rss.html`, `https://www.cnbc.com/id/10000664/device/rss/rss.html` | Mainstream markets news; named in the M0 list |
| `yahoo-finance` | `https://finance.yahoo.com/news/rssindex` | Broad company coverage; named in the M0 list |
| `yahoo-tickers` | `https://feeds.finance.yahoo.com/rss/2.0/headline?s=VZ,T,TMUS&region=US&lang=en-US` | Headlines for the thesis 13 tickers, useful for ticker extraction |
| `nasdaq-markets` | `https://www.nasdaq.com/feed/rssoutbound?category=Markets` | Markets news from an exchange |
| `marketwatch-top` | `https://feeds.content.dowjones.io/public/rss/mw_topstories` | Mainstream markets news |
| `fed-press` | `https://www.federalreserve.gov/feeds/press_all.xml` | An official, public source, to prove the pipeline end to end if the news feeds refuse GitHub's runners |

**Rule for MarketBeat items (proposed 2026-10-29, confirmed by the founder's merge of the pull request that added it):** store only what the feed publishes (headline, link, short description, tags); never fetch the article page; public pages show a MarketBeat item only as the source name, the headline and a link to the original page, never the description text; a thesis citation names MarketBeat and links to the article, as `docs/AI_SYSTEM.md` already requires of every citation. Do not resell or export the stored items in bulk. The same rule is the default for any news feed added later until its own terms are read.
