# Round 2 channels (M0, task 3)

*Where to get careful reads from target-persona readers after round 1 produced three skimmers (`m0/reader-feedback-log.md`). Supplements `m0/distribution-list.md`, which stays the persona-fit list; this file adds what was verified about each channel's rules, cost and speed on 2026-10-10, and an execution order. Facts marked **verified** were read from the cited page on that date; anything marked **unverified** is from memory or inference and must be checked before relying on it.*

## 1. What could and could not be verified

| Source | Status on 2026-10-10 |
|---|---|
| Reddit rules pages, sidebars, wikis (reddit.com) | **Not readable** from the research environment (`SITE_BLOCKED`). Mirrors and caches were deliberately not used. Every subreddit rule below is therefore **unverified** until the founder pastes the rules text (§3). |
| Reddit's own site rules and help center (redditinc.com) | Also blocked. Statements about multiple accounts, ban evasion and modmail are **unverified**; check https://www.redditinc.com/policies/reddit-rules directly. |
| Hacker News Show HN rules | **Verified**, https://news.ycombinator.com/showhn.html |
| Prolific pricing, minimum pay, filters, unsuitable studies | **Verified**, Prolific researcher help pages (cited in §2) |
| Value Investors Club FAQ and about page | **Verified**, https://valueinvestorsclub.com/help/faq and `/help/aboutus` |
| X/Fintwit, Substack Notes, LinkedIn, Discord servers, Italian-language communities | **Not researched** to a usable standard (search returned SEO noise, no primary sources). Not recommended for speed in any case: no existing audience means no feedback loop. |

One aggregate data point, **secondary and from a commercial vendor** (redditapis.com, snapshot 2026-09-09): of 100 large subreddits, only 6 publish numeric karma or account-age thresholds in their rules text, while AutoModerator configurations are not visible. Read as: a rules page that says nothing about karma does not mean a new account's post will survive. It names none of our candidate subreddits.

## 2. Channels, ranked by speed and by persona fit

| # | Channel | Speed | Persona fit | Cost | What was verified |
|---|---|---|---|---|---|
| A | **Paid reader panel (Prolific)** | Unverified; the vendor markets "hours, not weeks". Its help pages give only a 40–50% response rate from the eligible pool, no turnaround guarantee | Medium: no investing filter in the documented list, so screening must be a custom question | One-off: see below | Fee 42.857% on top of rewards (corporate rate); minimum pay £6 / $8 per hour, recommended £9 / $12; no surcharge for pre-screeners. Studies collecting names or **emails** are "unlikely to be supported". The documented filters include employment industry but no investing or stock-ownership filter; custom screening questions exist. |
| B | **Reddit, target subreddits** | Days; unpredictable | High if a post survives | Free | Nothing verified (§3). |
| C | **Value Investors Club** | Weeks | Very high | Free | Membership by individual application that must include "a favorite current investment recommendation", judged by an investment manager; "only a select few are chosen". Ideas up to about 25,000 characters; ratings become visible once at least 6 members have rated; authors are expected to answer questions that identify flaws. Scope: value and special-situation equity ideas, so a multi-name basket write-up is a poor fit; a single-name pitch would be needed. |
| D | **Direct outreach to independent analysts and small newsletter authors** | Days | High | Free | Not researched; list to be built. Expected low response rate, high quality per response. |
| E | **Hacker News** | Hours | Low for finance; possible for tech-adjacent narratives | Free | **Correction to `distribution-list.md`:** Show HN excludes blog posts, sign-up pages, newsletters, lists and other reading material, and landing pages (paraphrased from the rules page). A write-up cannot go out as Show HN. Only a regular story submission is possible, and finance theses are off the beaten path there. |

### Channel A in numbers

Reward for a 20-minute read-and-answer task, plus the platform fee (rewards × 1.42857):

| Participants | At the minimum ($8/h) | At the recommended rate ($12/h) |
|---|---|---|
| 10 | about $38 | about $57 |
| 15 | about $57 | about $86 |

Figures are estimates from the pricing page's stated fee and rates; screened-out participants also receive a small payment and the page does not say who pays it. This is one-off spend, not a stack component, so it does not read as a breach of ADR-0002 D-19, but `AGENTS.md` §6 ("Money") makes it the founder's explicit call. If approved, record it as validation spend in `m0/intervention-log.md`.

What a paid panel can and cannot show:

- **Can:** whether a careful reader (they are paid to read) finds the thesis understandable, grounded, falsifiable and non-generic; where they get lost; whether the one-page version beats the long one.
- **Cannot:** demand. "Would you miss this?" asked of paid respondents is inflated and must not feed the M0 gate's "how would you feel if this no longer existed" question. Use it for the quality half of the gate only.
- **Constraints:** no email collection (keep the questionnaire anonymous, no landing-page signup step); say that the text is AI-assisted; whether Prolific accepts feedback on written content is **not covered** by the help pages read, so confirm with Prolific support before launching.

## 3. Reddit protocol

### 3.1 What to paste back (about 5 minutes per subreddit)

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
| A minimum karma or age above the account's | Build history with real comments first, or skip the sub. |
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

## 4. Execution order and review date

| When | Step | Owner |
|---|---|---|
| 2026-10-10/11 | Paste subreddit rules (§3.1); decide on Channel A budget | Founder |
| 2026-10-11/13 | Choose the new topic, verify its facts against primary sources, write the one-page version (ADR-0003 template, D-33 source hierarchy) | Claude, founder review |
| 2026-10-13/14 | Launch Channel A study (if approved) with the one-page version and a six-question anonymous form; send message A or B where needed | Founder |
| by 2026-10-24 | One Reddit post in the best-fitting subreddit; one week of replies | Founder |
| in parallel | Channel D list; Channel C only if a single-name pitch comes out of the new thesis | Claude drafts, founder sends |
| 2026-11-07 | M0 gate verdict written into `PROJECT_STATE.md` from the evidence collected, including "not validated" if that is what it shows | Founder |

## 5. Sources

- Show HN rules: https://news.ycombinator.com/showhn.html (read 2026-10-10)
- Prolific pricing: https://researcher-help.prolific.com/en/articles/445239-what-is-your-pricing (read 2026-10-10; page shows no explicit date)
- Prolific participant pay: https://researcher-help.prolific.com/en/articles/445266-how-much-should-i-pay-participants
- Prolific filters: https://researcher-help.prolific.com/en/articles/445159-how-do-i-use-prolific-s-filters
- Prolific unsuitable studies: https://researcher-help.prolific.com/en/articles/445105-are-there-types-of-studies-that-aren-t-suitable-for-prolific
- Value Investors Club: https://valueinvestorsclub.com/help/faq and https://valueinvestorsclub.com/help/aboutus
- Reddit posting-requirements snapshot (secondary, vendor): https://www.redditapis.com/blogs/subreddit-posting-requirements-measured-2026
