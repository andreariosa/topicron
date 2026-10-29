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

| Source | Status | What was found |
|---|---|---|
| MarketBeat | **Wired in** (`jobs/ingest/feeds.py`, active) | The feed is RSS 2.0 with no namespaces. Each item has title, link, a `guid` (`isPermaLink="false"`), `pubDate`, a description of about 190 characters, and one or two `category` elements holding tickers (several tickers in one category, separated by a line break). No author. `robots.txt` has no rule against `/feed/` (its `*/rss-feeds/*` rule concerns the directory page of feeds, which the job never fetches), and it carries the content signals `search=yes, ai-input=yes, ai-train=yes`. `llms.txt` allows use for AI purposes and says: cite MarketBeat as the source and link back to the original page with each citation. The Terms of Service say nothing about RSS or AI; they grant a personal licence and forbid resale, reproduction for commercial purposes and bulk redistribution of MarketBeat's data. |
| Benzinga | In the list, **switched off** | Its `robots.txt` could not be read by Claude's tool. The founder is to open `https://feeds.benzinga.com/robots.txt` in a browser; the feed is switched on in a later pull request only if it allows the feed. |
| Financial Times | **Not wired in** | Paywalled, and its terms could not be read. Revisit only if a headline-and-link use is wanted. |

**Proposed rule for MarketBeat items (the founder confirms it by merging the pull request that adds this section):** store only what the feed publishes (headline, link, short description, tags); never fetch the article page; public pages show a MarketBeat item only as the source name, the headline and a link to the original page, never the description text; a thesis citation names MarketBeat and links to the article, as `docs/AI_SYSTEM.md` already requires of every citation. Do not resell or export the stored items in bulk.

**Freshness is not confirmed.** Through the fetch tool the feed showed items from 13 to 21 September 2026 and a last-build date of 21 September, which may be an old copy (the same tool has returned old copies of other pages). The first dry run of the Ingest workflow settles it: the log prints the newest and oldest dates. The job also fails any run in which the newest item is more than 72 hours old.

