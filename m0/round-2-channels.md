# Round 2 channels (M0, task 3)

*Where to get careful reads from target-persona readers after round 1 produced three skimmers (`m0/reader-feedback-log.md`). Supplements `m0/distribution-list.md`, which stays the persona-fit list; this file adds what was verified about each channel's rules, cost and speed on 2026-10-10, and an execution order. Facts marked **verified** were read from the cited page on that date; anything marked **unverified** is from memory or inference and must be checked before relying on it.*

## 1. What could and could not be verified

| Source | Status on 2026-10-10 |
|---|---|
| Reddit rules pages, sidebars, wikis (reddit.com) | **Not readable** from the research environment (`SITE_BLOCKED`). Mirrors and caches were deliberately not used. The founder pasted the rules text of ten subreddits on 2026-10-10; §3.0 works from that text. Anything it does not contain (karma thresholds, AutoModerator, wikis) is still **unknown**. |
| Reddit's own site rules and help center (redditinc.com) | Also blocked. Statements about multiple accounts, ban evasion and modmail are **unverified**; check https://www.redditinc.com/policies/reddit-rules directly. |
| Hacker News Show HN rules | **Verified**, https://news.ycombinator.com/showhn.html |
| Prolific pricing, minimum pay, filters, unsuitable studies | **Verified**, Prolific researcher help pages (cited in §2) |
| Prolific attention and rejection policy, Google Forms guide, custom screening, filters and sub-conditions, VAT | **Verified** 2026-10-12, researcher-help.prolific.com (articles 445153, 445183, 445165, 586737, 445218, bf1a70, 445239) |
| Value Investors Club FAQ and about page | **Verified**, https://valueinvestorsclub.com/help/faq and `/help/aboutus` |
| X/Fintwit, Substack Notes, LinkedIn, Discord servers, Italian-language communities | **Not researched** to a usable standard (search returned SEO noise, no primary sources). Not recommended for speed in any case: no existing audience means no feedback loop. |

One aggregate data point, **secondary and from a commercial vendor** (redditapis.com, snapshot 2026-09-09): of 100 large subreddits, only 6 publish numeric karma or account-age thresholds in their rules text, while AutoModerator configurations are not visible. Read as: a rules page that says nothing about karma does not mean a new account's post will survive. It names none of our candidate subreddits.

## 2. Channels, ranked by speed and by persona fit

| # | Channel | Speed | Persona fit | Cost | What was verified |
|---|---|---|---|---|---|
| A | **Paid reader panel (Prolific)** | Hours (observed 2026-10-13: the 3 pilot places filled in about 35 minutes, and all 16 places across two studies were filled the same day). The help pages give a 40–50% response rate from the eligible pool and no turnaround guarantee | Medium to high: investing filters exist in the study setup (observed 2026-10-13) but are self-reported profile data, so the form also screens with two questions | One-off: see below | Fee 42.857% on top of rewards (corporate rate), VAT on the fee only; minimum pay £6 / $8 per hour, recommended £9 / $12; workspaces in GBP or USD. Studies collecting names or **emails** are "unlikely to be supported". No investing filter in the help pages read, but the study setup has them (observed 2026-10-13); custom screening is the documented fallback and screened-out participants receive the reward set at creation. Google Forms works with a manual completion code (no automatic redirect). Rejection only for two failed valid attention checks (studies over 5 minutes), skipped required questions, clear low effort or 3-SD-fast outliers; content questions are not grounds. Read 2026-10-12. |
| B | **Reddit, target subreddits** | Days; unpredictable | High if a post survives | Free | Nothing verified (§3). |
| C | **Value Investors Club** | Weeks | Very high | Free | Membership by individual application that must include "a favorite current investment recommendation", judged by an investment manager; "only a select few are chosen". Ideas up to about 25,000 characters; ratings become visible once at least 6 members have rated; authors are expected to answer questions that identify flaws. Scope: value and special-situation equity ideas, so a multi-name basket write-up is a poor fit; a single-name pitch would be needed. |
| D | **Direct outreach to independent analysts and small newsletter authors** | Days | High | Free | Run on 2026-10-16: 16 candidates from a first list, search leads and Seeking Alpha contributors, then 5 Substack searches (first 20 results each), gave 2 who passed the filter; 2 messages were sent through contact forms. The founder then closed the search (low yield; results mostly AI-written or brand-run). Counts and reasons: `m0/reader-feedback-log.md`, free-reader channels. |
| E | **Hacker News** | Hours | Low for finance; possible for tech-adjacent narratives | Free | **Correction to `distribution-list.md`:** Show HN excludes blog posts, sign-up pages, newsletters, lists and other reading material, and landing pages (paraphrased from the rules page). A write-up cannot go out as Show HN. Only a regular story submission is possible, and finance theses are off the beaten path there. |

### Channel A in numbers

Reward for a 20-minute read-and-answer task, plus the platform fee (rewards × 1.42857):

| Participants | At the minimum ($8/h) | At the recommended rate ($12/h) |
|---|---|---|
| 10 | about $38 | about $57 |
| 15 | about $57 | about $86 |

Figures are estimates from the pricing page's stated fee and rates; screened-out participants also receive a small payment and the page does not say who pays it. This is one-off spend, not a stack component, so it does not read as a breach of ADR-0002 D-19, but `AGENTS.md` §6 ("Money") makes it the founder's explicit call. If approved, record it as validation spend in `m0/intervention-log.md`.

**Approved 2026-10-12 (founder, chat): cap EUR 100.** Design, cost and steps (the first plan was in USD with a worst case of about EUR 83; the workspace turned out to be in GBP): `m0/prolific-study-spec.md`; form text: `m0/prolific-form-text.md`; one-page reading version: `m0/topic-thesis-13-one-page.md`.

**Run 2026-10-13:** two studies, both filled the same day, £72.81 reserved (about EUR 86); about £66.49 actually spent (about EUR 79), derived from the workspace balance on 2026-10-14. Setup, spend and what happened: `m0/prolific-study-spec.md` §3 and §7. Results: `m0/reader-feedback-log.md`, Round 2.

What a paid panel can and cannot show:

- **Can:** whether a careful reader (they are paid to read) finds the thesis understandable, grounded, falsifiable and non-generic; where they get lost; whether the one-page version holds up against the long one.
- **Cannot:** demand. "Would you miss this?" asked of paid respondents is inflated and must not feed the M0 gate's "how would you feel if this no longer existed" question. Use it for the quality half of the gate only.
- **Constraints:** no email collection (keep the questionnaire anonymous, no landing-page signup step); say that the text is AI-assisted; none of the help pages read prohibits feedback on written content, but that is not the same as it being accepted, so the 3-place pilot is also the test.

## 3. Reddit protocol

### 3.0 Subreddit rules as pasted by the founder (2026-10-10), and what they decide

The rules below are the founder's copy of each subreddit's rules page and sidebar; Reddit itself remained unreadable from the research environment. Anything not in the pasted text (karma thresholds, AutoModerator, wikis) is unknown.

| Subreddit | Decision | Rules that decide it |
|---|---|---|
| r/SecurityAnalysis | **Posted, live since 2026-10-16.** It was the first choice (restricted mode; the sidebar invites posting requests, "this isn't a blocker", and the sub has a Request to Post form, which replaces modmail). The request sent on 2026-10-12 had no answer by 15:45 on 2026-10-14, which §3.2 counts as no, so the sub was dropped from the plan. The moderators approved the request on 2026-10-15. The founder posted that evening (about 22:00 Rome) and AutoModerator removed the post at once: the sub requires an account at least 60 days old and u/topicron was about 5 days old. That threshold was not in the pasted rules; it appeared only in the removal message. The founder sent modmail asking the moderators to approve the post from the queue, and they did; the post was visible on 2026-10-16. A dated comment with the AT&T Q3 facts was added under it on 2026-10-21 (the post body and the hypothesis were not edited). Text as submitted: `m0/topic-thesis-13-distribution-copy.md` §1 | Rule 3: no overt self-promotion of blogs, apps, websites, YouTube channels or surveys. Rule 2: factual, unedited titles, written with linked articles in mind. No rule on AI text in the pasted text. Sidebar posting guidelines (pasted 2026-10-15): a post on an individual security must contain analysis, not a recitation of ratios; specific questions are asked for and "Thoughts" posts are discouraged. Flair options: No flair, Long Thesis, Short Thesis, Thesis. |
| r/ValueInvesting | **Blocked for now.** Create Post is refused by an account-age check (u/topicron was 1 day old on 2026-10-11; threshold not shown). It is probably the same kind of check that removed the r/SecurityAnalysis post (60 days); if the threshold is the same, the account would pass about 2026-12-09 (not verified). Skipped on 2026-10-21 (founder): the retry slot of 2026-10-20 passed with no action and the founder confirmed it; no message to the moderators. The r/SecurityAnalysis post is now live and rule 2 bars the same content in several subs, so only different content could go here | Rule 4: authored on-topic articles allowed, ask by modmail if unsure. Rule 5: limited self-promotion for regular participants only. Rule 10: moderators may remove AI-generated content. Rule 2: no content posted to many subs at once. Rule 9: no soliciting contact details. |
| r/stockpitches | **Dropped (2026-10-12).** Dormant: last post and last comment 8 years old, 1 weekly visitor (founder's check) | Sidebar: "post your own ideas". No rules in the pasted text. Format fit, no readers. |
| r/investing | **Excluded** | Rule 1: large amounts of Gen AI text are low effort. Rule 4: (self-)promotion, surveys and blogs: permanent ban. |
| r/StockMarket | **Excluded** | Rule 7: the same AI-text rule. Rule 2: self-promotion and surveys: permanent ban. Rule 3: the same post across several subs is spam. |
| r/ItaliaPersonalFinance | **Excluded** | Rule 7: no fully AI-generated content. Rule 4: no surveys or market research. Also a personal-finance sub, not a thesis sub. |
| r/startups, r/SideProject | **Not for theses** | Feedback on the project, not on reading a thesis. r/startups confines feedback requests and surveys to its stickied thread. Revisit for the landing page. |
| r/wallstreetbets, r/stocks | **Stay excluded** | Anti-persona (`m0/distribution-list.md`); WSB rule 13 bars mentioning anything the poster has a conflict of interest in. |
| r/Fundamentalanalysis | **Not assessed** | Nothing was found to paste. |

**Request to Post text for the r/SecurityAnalysis form** (shorter than message A, and it no longer mentions r/ValueInvesting):

> **Request to post: one original text analysis (equity thesis), AI-assisted, with disclosure**
>
> I'd like to post one original text analysis, about one page, on a small group of listed companies: hypothesis, why now (with an as-of date), what the market may be missing, the strongest bear case, valuation and what is priced in, dated catalysts, and the observable conditions that would prove it wrong. Figures come from primary filings, which are the only links in the post.
>
> Rules check: no links to any site, blog, app or survey of mine (rule 3), and a descriptive, non-promotional title, since rule 2 reads as written for linked articles. The username is the name of a small research project I'm building; I won't link it.
>
> Disclosure, stated in the post: I'm the author, the draft was written with AI assistance (Claude), I check every figure against the filings before posting, and I'll state any positions I hold. I'm after critique of the reasoning, not upvotes. The same analysis may also appear in r/stockpitches. Happy to send the draft here first. If it isn't a fit, I won't post it.

Sent 2026-10-12 as written. It still says the analysis may also appear in r/stockpitches, which turned out to be dormant; the text is kept as sent. The moderators approved it on 2026-10-15, a day after the cut-off that had counted the missing answer as no.

### 3.1 What to paste back (about 5 minutes per subreddit)

*Done on 2026-10-10 for the subreddits in §3.0; use this checklist for any further one.*

For each of r/SecurityAnalysis, r/ValueInvesting, r/investing (all from `distribution-list.md`), plus any other sub considered, copy into one message:

1. The full text of the **Rules** page.
2. The **About / sidebar** text and any wiki page about posting or self-promotion.
3. Whether a **weekly feedback, self-promotion or "what are you working on" thread** is stickied.
4. The **flair list**, and whether a flair is mandatory.
5. Whether the rules mention: minimum **account age or karma**; **self-promotion / own content** (for example a ratio rule); **AI-generated content**; **links vs text posts**; a **DD template**; a **pre-approval** step; how to use **modmail**.

With that text the rules analysis can be done properly and the messages in §3.3 finalized. Until then the following decision rules apply.

### 3.2 Decision rules

| If the rules say | Then |
|---|---|
| A stickied feedback / self-promotion thread exists | Use it; lowest risk, lowest reach. |
| Self-promotion or own content is restricted | Post the analysis itself as text, no link, no mention of a product, with author disclosure; or skip the sub. |
| Pre-approval is required | Send message B (§3.3). No answer in 48 hours counts as no. Do not repost elsewhere from another account to get around it. |
| A minimum karma or age above the account's | Build history with real comments first, or skip the sub. A threshold may not be in the rules text: r/SecurityAnalysis's 60-day account age was visible only in AutoModerator's removal message (2026-10-15). |
| AutoModerator removes a post after an approval (for example for account age) | Send modmail asking the moderators to approve the post from the queue, and wait. Do not delete, edit or repost it, and do not post from another account. This worked on 2026-10-16 (§3.0). |
| AI-generated content is banned or must be flaired | Follow it. A write-up drafted with Claude is AI-assisted; disclose it everywhere, and skip subs that ban it. Never disguise it. |
| Moderators already declined the earlier request from the personal account | Do not retry from `u/topicron`. That reads as circumvention. |

### 3.3 Do the messages have to be private, and can a new account send them?

Unverified (Reddit's help pages were unreadable), stated as working assumptions to confirm:

- The normal route is **modmail** (the subreddit's "message the moderators" link), not a private message to an individual moderator. Individual DMs are often unwelcome.
- Many subreddits do not want permission requests at all and expect you to follow the rules. A message is worth sending only when the rules require pre-approval, or when a specific rule is ambiguous for this kind of post.
- A new account can usually send modmail, but a zero-karma, brand-named account asking for permission carries little credibility. Send it after the account has some real comment history.
- Multiple accounts are generally tolerated by Reddit; evading a ban or a moderator decision is not. Confirm on the Reddit Rules page.

**Message A, rules clarification (use when a rule is ambiguous):**

> **Subject:** Question before posting: original analysis, AI-assisted, with disclosure
>
> Hi mods. I'd like to post a one-page equity analysis and want to check it fits [RULE # / name] rather than guess.
>
> - It is a text post: the full analysis is in the post, with no link to anything I sell or run.
> - It states a falsifiable hypothesis, the strongest bear case, valuation context, dated catalysts and explicit invalidation conditions, with primary sources where they exist.
> - Disclosure in the post: I'm the author, I'm building a small research project (Topicron), the draft was written with AI assistance (Claude) and I checked the figures against the cited filings. [State any position held.]
> - I'm asking for critique of the reasoning, not for upvotes, and it is not investment advice.
>
> Is this within the rules, and is there a flair you want used? If not allowed, I won't post it. Thanks for your time.

**Message B, pre-approval (use only where pre-approval is required):**

> **Subject:** Pre-approval request: analysis post with author disclosure
>
> Hi mods. [Sub] requires pre-approval for [own content / self-promotion]. I'd like to post a one-page, text-only equity analysis on [TICKERS / THEME]. Draft below so you can judge it; it contains no links to my site. It was written with AI assistance and verified by me against primary sources, and the post says so. I'm hoping for critique of the argument. Happy to change flair, title or format, or to withdraw it if it isn't a fit.
>
> [paste the post]

### 3.4 Post skeleton (text post, one page)

1. Title: the claim, not the brand. Example shape: "[Company group]: [one-sentence falsifiable hypothesis] (AI-assisted analysis, as of [date])".
2. Hypothesis (one sentence) · Why now (with the as-of date) · What the market may be missing · Best bear case · Valuation and what is priced in · Catalysts in the next 90 days · What would prove this wrong.
3. Disclosure line (author, AI-assisted, positions, not advice).
4. Three closing questions, which also test the M0 hypothesis directly: (a) what is the weakest assumption here? (b) did you read all of it or skim, and why? (c) would you want this format on a regular cadence?

No link to topicron.vercel.app in the first post; add it only if a moderator or reader asks.

The r/SecurityAnalysis post (§3.0) used one specific closing question instead of the three above, because the sub's posting guidelines ask for specific questions and discourage "Thoughts" posts. It therefore does not ask whether the reader read all of it or would want the format regularly. A reply there says something about attention and critique; it is not a direct answer to the demand question (§4.1).

## 4. Execution order and review date

| When | Step | Owner |
|---|---|---|
| 2026-10-10 | Subreddit rules pasted (§3.0); X account set up | Founder |
| 2026-10-11 | New topic chosen, facts checked against primary sources, thesis and one-page version written (`m0/topic-thesis-13-us-wireless-spacex.md`, `m0/topic-thesis-13-distribution-copy.md`) | Claude |
| 2026-10-12 | Done: write-up 13 committed (12:19) and the Claude Project re-synced; closes confirmed against investing.com; Request to Post sent to r/SecurityAnalysis; Prolific approved up to EUR 100 | Founder |
| 2026-10-13 | Done: Prolific Study A (full text, 10 readers, a pilot of 3 then 7 more) and Study B (one page, 6 readers) built, run and analysed; both filled the same day (`m0/prolific-study-spec.md` §7). Results: `m0/reader-feedback-log.md`, Round 2 | Founder, with Claude |
| 2026-10-14 | Done: no answer from r/SecurityAnalysis by 15:45, counted as no (§3.2), sub dropped from the plan (reversed the next day, see below); X thread posted (first post and four replies, `m0/topic-thesis-13-distribution-copy.md` §2); Prolific spend closed, about £66.49 (`m0/intervention-log.md`) | Founder |
| 2026-10-15 | Done: the moderators approved the Request to Post; the founder posted at about 22:00 and AutoModerator removed the post at once (account under 60 days old, §3.0); modmail sent to the moderators | Founder |
| 2026-10-16 | Done: the moderators approved the post; it is live (§3.0). Next: check the comments the same day and the next morning, reply on substance without links, log them anonymously (`m0/topic-thesis-13-distribution-copy.md` §1.1) | Founder, with Claude |
| 2026-10-16 (outreach) | Done: outreach from the private kit (not in the repository). The search found 2 candidates who passed the filter and was then closed by the founder; 2 messages were sent through contact forms, with the one-page version first and the full text as a second link. One follow-up after 5 days if there is no reply, then stop (`m0/reader-feedback-log.md`) | Founder |
| 2026-10-20 | Skipped: r/ValueInvesting (the retry slot passed with no action; confirmed by the founder on 2026-10-21). The r/SecurityAnalysis post is the only Reddit post of round 2 | Founder |
| 2026-10-21 | Done: round-2 review, three days before the 24 Oct limit. Free-reader signals tallied, all at zero: no comments and no score on the r/SecurityAnalysis post, no replies on X, no reply from the 2 outreach contacts, 0 subscribers (the X profile links to the page). Sent the same day: one follow-up to each outreach contact (no links, one question), a dated AT&T Q3 comment under the r/SecurityAnalysis post and an AT&T Q3 post on X. The "fewer than 2 specific replies out of 10" rule was not applicable (2 messages). The founder has no further free-reader channel to try; replies to the follow-ups are logged as they come (`m0/reader-feedback-log.md`). The reading of the intervention log is in `m0/intervention-log-review.md` | Founder, with Claude |
| 2026-10-26 and 2026-10-28 | X update after the Verizon and the T-Mobile Q3 reports, in the same format as the AT&T post (facts only, hypothesis unchanged) | Founder |
| in parallel | Channel D: private kit, with the list found by the founder using a 60-second filter (a verified list was not possible with the tools available); Channel C only if a single-name pitch comes out of the new thesis | Claude drafts, founder sends |
| 2026-10-26 | M0 gate verdict written into `PROJECT_STATE.md` from the evidence collected, including "not validated" if that is what it shows (wording: §4.1). Brought forward from 2026-11-07 by the founder on 2026-10-21: no further free channel is planned, so no new demand data is expected beyond late replies | Founder |

### 4.1 How the verdict is worded (proposed; the founder accepts or changes it before the data arrives)

The M0 gate in `docs/ROADMAP.md` asks two things, and each is recorded on its own:

- **Quality and intervention delta** ("do target-persona readers find the write-ups genuinely useful, and is the intervention delta small enough that a pipeline could plausibly close it?"). The first part is read from the paid panel against the thresholds in `m0/prolific-study-spec.md` §5 (result: `m0/reader-feedback-log.md`, Round 2); the second from `m0/intervention-log.md` at the gate.
- **Demand** ("how would you feel if this no longer existed", `docs/RISKS.md`). Only readers who read for free count: X, outreach, any Reddit post that goes out, and the landing-page list as a passive signal. Paid readers do not feed it.

A half with no valid signal is recorded as "not tested", never as passed or failed: zero replies to cold outreach measures the cost of getting attention, not the need. Whether the project moves to M1 with a half untested is the founder's call (`AGENTS.md` §6, milestone sequencing). If he decides to proceed, it is written down in a new ADR (`AGENTS.md` §9) together with the condition that would stop the project before M2.

**Status on 2026-10-16 (a record, not part of the proposed wording):** outreach reached 2 people and the search was closed; the r/SecurityAnalysis post has no comments yet; the X thread has no reported reply; the landing-page list is empty (0 subscribers), and it cannot register a signal because the round-2 channels deliberately carry no link to the site. Details: `m0/reader-feedback-log.md`, free-reader channels.

**Status on 2026-10-21 (a record, not part of the proposed wording):** every free-reader source is at zero: no comments and no score on the r/SecurityAnalysis post, no replies on X, no reply from the 2 outreach contacts (a follow-up went to each that day), 0 subscribers (the X profile links to the page). No further free channel is planned. The demand half is therefore "not tested" for the reason given above, the cost of attention. The intervention-delta half is read in `m0/intervention-log-review.md` (reading: "plausible, conditional"); it is recorded as a gate result only when the verdict is written, due on 2026-10-26 (brought forward from 2026-11-07).

## 5. Sources

- Show HN rules: https://news.ycombinator.com/showhn.html (read 2026-10-10)
- Prolific pricing: https://researcher-help.prolific.com/en/articles/445239-what-is-your-pricing (read 2026-10-10; page shows no explicit date)
- Prolific participant pay: https://researcher-help.prolific.com/en/articles/445266-how-much-should-i-pay-participants
- Prolific filters: https://researcher-help.prolific.com/en/articles/445159-how-do-i-use-prolific-s-filters
- Prolific unsuitable studies: https://researcher-help.prolific.com/en/articles/445105-are-there-types-of-studies-that-aren-t-suitable-for-prolific
- Value Investors Club: https://valueinvestorsclub.com/help/faq and https://valueinvestorsclub.com/help/aboutus
- Reddit posting-requirements snapshot (secondary, vendor): https://www.redditapis.com/blogs/subreddit-posting-requirements-measured-2026
