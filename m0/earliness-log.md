# Reddit Searchability Finding (Task 4, M0)

*Originally scoped per docs/ROADMAP.md M0 task 4 as an earliness comparison (Reddit vs. curated RSS/mainstream). Two independent attempts instead surfaced a more fundamental finding about Reddit's native search reliability for narrow financial narratives — documented here since it's more useful to the underlying question (is Reddit ingestion, deferred per ADR-0001, ever worth reinstating) than a clean date comparison would have been.*

## Attempt 1 — manual subreddit search, sorted by "Old"

Searched r/SecurityAnalysis, r/ValueInvesting, r/investing directly via each subreddit's search bar for two write-ups (4, 6), sorted by "Old" to find the earliest relevant result.

Result: found something for both (write-up 4: 74 days ahead of mainstream; write-up 6: 54 days behind) — but even that result carried real caveats: one "hit" was a general single-stock thread only tangentially touching the topic, the other was suspiciously dated the same day as the search itself, and relevant discussion took "a lot of effort" to find, turning up only scattered comments rather than dedicated threads.

## Attempt 2 — broader scrape across 4 search phrases

Went back to the same three subreddits and scraped as much as could be gathered for four phrases — "caterpillar reshoring," "US manufacturing tariffs," "Huntington Bancshares," "regional bank M&A" — after finding that sorting search results by date returned no posts at all.

**Result: the scrape did not reflect filtered, on-topic search results.**

- **"Huntington Bancshares"** returned zero genuine matches. Every single hit was **Huntington Ingalls Industries** — an unrelated shipbuilding/defense company that happens to share the word "Huntington." Not one post about the actual bank.
- **"caterpillar reshoring"** returned almost entirely unrelated posts (title examples: "The SaaS reversal will be glorious," "Time to sell BATS?"), with occasional incidental "$CAT" mentions about the stock generally, never about reshoring specifically.
- **"US manufacturing tariffs"** returned genuinely on-topic tariff/manufacturing discourse, but broad (US-China trade war, semiconductor manufacturing, furniture manufacturing) rather than specifically about the reshoring wave or the write-up's named companies.
- **"regional bank M&A"** was the closest to relevant — genuine regional-banking-sector discussion — but not clearly filtered to the M&A angle specifically.

## Conclusion

Reddit's own search, for phrase-level financial-narrative queries, is not reliable enough to extract clean, dated, on-topic signal — not because the underlying discussion doesn't exist, but because keyword matching alone produces false positives (Huntington Ingalls vs. Huntington Bancshares is unambiguous proof) and sorting-by-date silently fails for lower-volume queries, forcing a fallback to broad, unfiltered browsing.

**This is directly relevant to the Reddit-ingestion reinstatement question (deferred, ADR-0001).** If a careful manual attempt, done twice with different methods, can't cleanly isolate narrative-specific Reddit signal, an automated ingestion pipeline would need real entity-resolution logic (distinguishing companies with overlapping names, filtering topic-adjacent-but-off-target discourse) to be worth building at all — meaningfully more complexity than "subscribe to a feed and keyword-match." This raises, rather than lowers, the bar for ever reinstating this deferred feature.

## Recommendation

Task 4 is complete with this finding, not with a clean earliness number. Worth a short pointer from `docs/RISKS.md` or `docs/MVP_SCOPE.md`'s Reddit-ingestion entry to this file, so the next person evaluating that reinstatement trigger doesn't have to rediscover this from scratch.
