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
