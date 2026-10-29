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
| `cnbc-top` | Answered: 30 items, fresh | **Switched on by the founder's decision**; the founder read its robots.txt (feed path not covered, Topicron not named, AI and finance bots blocked by name); terms unread |
| `yahoo-tickers` | Answered: 19 items, fresh, about T-Mobile and AT&T | **Switched off on 2026-10-29** after the founder read the robots.txt of its host: `User-agent: *` and `Disallow: /`. It had been switched on and 17 rows were stored before the reading; the founder deleted them the same day |
| `marketwatch-top` | Answered: 10 items, fresh (the feed holds only the latest ten, about 90 minutes at midday) | **Switched on by the founder's decision**; the robots.txt URL of its host answers AccessDenied (read as no file); terms unread. An hourly run that GitHub delays by a few hours misses some stories |
| `nasdaq-markets` | Timed out | Off: retry in a later probe; its robots.txt has no rule against `/feed/` |
| Benzinga | The server closes the TLS connection (from GitHub and from the founder's browser) | Dropped from the list; its robots.txt stays unread |
| `cnbc-finance` | Answered, but the newest item was 8 days old: a stopped feed | Dropped |
| `yahoo-finance` (`/news/rssindex`) | HTTP 404 | Dropped |
| Financial Times | Not tried | Not wired in: paywalled, terms unreadable. Revisit only for a headline-and-link use |

An earlier version of these notes read a copy of the MarketBeat feed in Claude's fetch tool that ended on 21 September 2026 as a sign the feed had stopped. That was an old cached copy; the live feed is current.

**MarketBeat.** The feed is RSS 2.0 with no namespaces. Each item has title, link, a `guid` (`isPermaLink="false"`), `pubDate`, a description of about 190 characters, and one or two `category` elements holding tickers (several tickers in one category, separated by a line break; some items list a dozen). No author. `robots.txt` has no rule against `/feed/` (its `*/rss-feeds/*` rule concerns the directory page of feeds, which the job never fetches), and it carries the content signals `search=yes, ai-input=yes, ai-train=yes`. `llms.txt` allows use for AI purposes and says: cite MarketBeat as the source and link back to the original page with each citation. The Terms of Service say nothing about RSS or AI; they grant a personal licence and forbid resale, reproduction for commercial purposes and bulk redistribution of MarketBeat's data.

**Federal Reserve.** Its disclaimer page says the information on the Board's website is in the public domain and may be copied and distributed without permission, and asks users to cite the Board as the source. Third-party material on the site and the Board's seals and logos are excluded. The feed is `press_all.xml`, listed on its feeds page; its items carry a category such as "Monetary Policy". It publishes a few items a month, so its age limit is 14 days instead of 72 hours.

**Rule for news items (confirmed by the founder's merge of the pull request that proposed it, 2026-10-29):** store only what the feed publishes (headline, link, short description, tags); never fetch the article page; public pages show an item only as the source name, the headline and a link to the original page, never the description text; a thesis citation names the source and links to the article, as `docs/AI_SYSTEM.md` already requires of every citation. Do not resell or export the stored items in bulk. This is the default for any feed added later until its own terms are read.

**CNBC Top News, Yahoo Finance (VZ, T, TMUS) and MarketWatch (switched on 2026-10-29 by the founder).** Claude could not read their robots.txt or terms (its tool could not load them or was refused), so the reading is the founder's: open `https://www.cnbc.com/robots.txt`, `https://feeds.finance.yahoo.com/robots.txt` and `https://feeds.content.dowjones.io/robots.txt` and check that no rule under `User-agent: *` covers the feed path; if one does, the feed goes back to `active=False`. News-site RSS terms commonly allow personal, non-commercial use only; the founder has decided to proceed, and the rule for news items above is what limits the exposure (private table, no article text, headline and link only in public).

**Result of the founder's reading (2026-10-29, robots.txt pasted into the chat):**

- **Yahoo Finance (`feeds.finance.yahoo.com`).** The file is `User-agent: *` and `Disallow: /`: no robot may fetch anything on that host, the feed included. Under the rule above the feed is off (`active=False`), and nothing is fetched from it from now on. The founder deleted the 17 rows stored from it on 2026-10-29.
- **CNBC (`www.cnbc.com`).** The rules for every robot (`User-agent: *`) disallow only `/preview/`, `/undefined/`, `/proplayer`, `/appchart/`, `/search`, `/zephr/` and `/blaize/`, so the feed path `/id/100003114/device/rss/rss.html` is open, and no group names Topicron (the job's user agent). A long list of named robots, among them AI crawlers and finance bots (`TradingBot`, `trading-pipeline`, `investment-dashboard`, `StockMarketAnalyser`, `FinanceApp`), is disallowed from everything (`Disallow: /`): the file allows the fetch and shows CNBC's stance towards automated finance and AI pipelines. CNBC's terms are still unread. On 2026-10-29, none of the 31 CNBC rows mentioned Verizon, AT&T or T-Mobile. The founder decided on 2026-10-29 to keep the feed on, knowing both of these points.
- **Dow Jones (`feeds.content.dowjones.io`, MarketWatch).** The robots.txt URL answers an XML `AccessDenied` error instead of a file. This is read as no robots.txt: RFC 9309 (section 2.3.1.3) lets a crawler access any resource when the file is unavailable (a 4xx answer). It is the absence of a rule, not a permission. The status code was not reported (a 5xx answer would mean the opposite, RFC 9309 section 2.3.1.4). MarketWatch's terms are still unread.

**What the first stored rows showed (2026-10-29, 178 rows from two real runs).** The first run (13:23 UTC) wrote 177 rows; the second (13:32 UTC) added 1 new item and found 176 already stored, so the dedupe key holds. There is no duplicate on `(source, external_id)`, `id` or `url`; two Fed releases share the same title, so the title is not a dedupe key. The one new item, a CNBC story published two minutes before the run, has an empty description (the feed had none yet) and keeps it, because the first copy of an item is never updated. Every MarketBeat item has tags, but one of the 100 has malformed ones (`:QBKV`, a bare `QBKV` and `XX` next to well-formed `NYSEARCA:SBAR`), so ticker extraction cannot assume `EXCHANGE:SYMBOL`. The Yahoo feed had no tags, and 7 of its 17 items were written by other publishers (TheStreet, Trefis, StockTwits, 24/7 Wall St., Motley Fool, MarketBeat): an item from an aggregator feed says nothing about its publisher or its relevance. A rough keyword match found 16 of the 178 items about Verizon, AT&T or T-Mobile, 13 of them from Yahoo and 3 from MarketBeat, so switching Yahoo off leaves the thesis 13 companies thinly covered (3 of the other 161 rows).

## The carriers' own newsrooms (checked 2026-10-29, afternoon)

**Why.** After Yahoo went off, the three carriers of thesis 13 almost never appear in the live feeds (the extraction table holds T 2 and VZ 3 and no TMUS). Each company publishes its own press releases, so those pages were looked at first. Robots.txt files were read through a summarising fetch tool. The AT&T terms were read in full from the founder's paste; the Verizon terms through the same tool, which returned quoted excerpts, not the full text.

| Source | Feed | robots.txt | Terms | State |
|---|---|---|---|---|
| AT&T newsroom (`about.att.com`) | `https://about.att.com/aboutus/rss/rssfeed.html?category=all`: RSS 2.0, 25 items, newest 28 Oct 2026, descriptions present, standard dates; the channel text says it is for reporters, analysts and consumers | `User-agent: *` disallows `/system/` only | The AT&T Web Services Terms of Use (effective January 2020, pasted by the founder): section 14 bans any robot, spider or other programmatic device used to get information from the Site, systematic collection and data mining, republishing or distributing Content to third parties, derivative uses and framing; section 6 grants personal, non-commercial use only "except as otherwise permitted". No word on RSS | `att-newsroom`: switched on by the founder's decision of 2026-10-29 and **off again** the same day after an HTTP 403 (below) |
| Verizon financial news (`www.verizon.com`) | `https://www.verizon.com/about/news/financial-news.xml`: RSS 2.0, 10 items, 24 Jul to 29 Oct 2026, newest 29 Oct 2026, no DTD. `pubDate` is written `Thu, 29 Oct 2026 09:12:17 AM EDT` and `29 Sept 2026`; `guid` is, per the summary, the headline (`isPermaLink="false"`). Verizon's RSS page (`/about/news/rss-feeds`, saved by the founder) lists thirteen feed addresses, among them `verizon-news-releases.xml` ("News releases only"), `financial-news.xml`, `quarterly-reports.xml` and `investor-events.xml`, and links to RSS reader apps | `User-agent: *` does not disallow `/about/news/*.xml`; only the `?category=All` and `?field_news_corporate_categories` variants of `/about/news/` are | The Verizon Website Terms of Use: under Acceptable use, no access "through any automated script or routine", with "robots", "spiders", "offline readers", bots and crawlers named, no data-mining or data-gathering tools, no redisplaying or framing of the Resources, and no commercial use. No word on RSS. They cover websites "operated by Verizon Communications", so the news center falls under them by the general wording | `verizon-financial`, on by the founder's decision of 2026-10-29; the first dry run read it right |
| Verizon, other feeds | `verizon-news-releases.xml` is RSS 2.0 with 10 items from 29 Sep to 29 Oct 2026 and shares two of them with the financial feed; `/about/rss.xml` has 5 items, newest 3 Aug 2026; `business-tech-news.xml` ends in 2021 | as above | as above | Not listed: overlap with the financial feed until cross-feed dedupe exists, or stale |
| T-Mobile newsroom (`www.t-mobile.com/news`) | No feed link on the page (the head holds only a canonical link) | The generic group does not disallow `/news` (it blocks accounts, checkout, search and similar) | Unread | No source. Its press releases also go out through a wire service (not read) |
| SEC EDGAR (`www.sec.gov`) | The Latest Filings Atom feed (8-K filings of each company) | `User-agent: *` disallows `/cgi-bin`, where those feeds live; `/Archives/edgar/data` is allowed | The SEC's webmaster FAQ allows scripted access at up to 10 requests a second, asks for a declared user agent with a contact, and says filing content is free to reuse | Out under the rule that a robots.txt rule covering the feed turns it off. `data.sec.gov` (JSON, another host) is unread; a contact in the user agent would put an address in a public repository |
| GlobeNewswire (Verizon's wire service for earnings) | Feeds under `/RssFeed/` (the per-company address pattern is not confirmed) | The file blocks `/SubscribeToRss/` and `/newsroom/rss/`, not `/RssFeed/` | Unread; Verizon's organisation feed address not found | Open, not listed |

**One correction.** Earlier today Claude described the att.com terms as excluding about.att.com. The full text shows the sentence ("if you are using the about.att.com site ... use of those sites are governed by a different policy") sits in section 5, Privacy Notice, so it most likely concerns privacy; the terms do not say that about.att.com is outside them.

**What the two terms have in common.** Both ban robots and automated scripts in plain words, and neither mentions RSS, although both companies advertise the feeds to be read by feed readers. Two readings are possible: a feed the company publishes for readers is an access route it invites, or the clause means what it says and covers any program. The text does not decide it, and Claude is not a lawyer. What the project's own rules give: `AGENTS.md` §7 refuses scraping "as a workaround for cost or rate limits", which this is not, so it is not an automatic refusal; the default of this document is that a feed whose terms were read and forbid robots stays off until the founder decides, and the founder has now decided (below).

**Decision (founder, 2026-10-29).** Both feeds were switched on. The written options were to ask each press office for a yes, to switch the feeds on by decision as CNBC was, or to leave them off; the founder chose the second, to stay consistent with the CNBC choice, knowing what the terms say, and did not ask the press offices. This section is the record of what the terms say. What the choice risks: either company can object, and the answer is then to set `active=False` and delete that source's rows, as was done for Yahoo. No probe was run first; the first look at the live data is a dry run of Ingest by hand on the merged code (it fetches the active feeds, prints the counts, the newest and oldest dates and the first three items, and writes nothing), where Verizon's `09:12 AM EDT` must read as 13:12 UTC.

**First dry run on the merged code (2026-10-29, 15:26 UTC).** Verizon: 10 items parsed, none skipped, newest 13:12:17 UTC, which is `09:12:17 AM EDT` read correctly. AT&T: the server answered HTTP 403 to the job, which sends its own honest user agent (`Topicron/0.1 (+https://topicron.vercel.app)`), although it had answered a page-reading tool earlier the same day. The job does not retry a 403 (`ingest/rss.py`: 403 and 404 mean the publisher said no) and neither do we: no change of user agent, no other route. A feed that errors makes the run fail after the other feeds are written, so `att-newsroom` is `active=False` again. The reason for the 403 is unknown (a block of cloud addresses and a refusal of non-browser user agents look the same from here). The way back is option (a) above: a written yes from AT&T's press office.

**What is now in the code.** `verizon-financial` is `active=True` in `jobs/ingest/feeds.py`; `att-newsroom` is listed with `active=False` and the reason. `ingest.rss` reads Verizon's date form (it converts `h:mm:ss AM/PM` to 24 hours, maps `Sept` to `Sep`, and skips any other AM/PM form instead of reading it with the AM/PM dropped, which the standard library does without an error). Not done: the raw XML of Verizon's feed has not been seen (its `guid` is, per a page-reader summary, the headline, so a repeated headline would be dropped as already stored), and `verizon-news-releases.xml` stays unlisted until cross-feed dedupe exists.
