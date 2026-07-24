# Vision

*This document is the full expansion of the positioning summarized in [`README.md`](../README.md). It implements [`ADR-0001`](../ADR-0001-mvp-scope-and-architecture.md); decisions are cited inline as "ADR-0001, D-XX."*

## Why this exists

Reddit and social-sentiment tools are commoditized. Free tools already track mention counts and compute a bullish-or-bearish score for whatever ticker is trending — that capability is real and useful, and it is also no longer a differentiator for anyone building on it in 2026 (`docs/RISKS.md`, Product risks: Commoditized entry point).

What no free tool pairs with a mention count is a structured investment thesis — a bull case, a bear case, named risks — and, more importantly, a public, unedited record of how that thesis's hypothetical portfolio actually performed against real subsequent market data. That combination — narrative discovery, a structured argument, and an honest scoreboard — is the bet this product is testing. Sentiment tracking is the on-ramp; it was never meant to be the destination.

This is also why topic discovery has to come before stock picking, not the other way around. A product that starts from "here's a ticker, here's why it might move" is a stock-tip service with extra steps. A product that starts from "here's a narrative gaining traction, and here's the structured case for and against it" is a research product. The entry point is the whole positioning, not an implementation detail.

## Who this is for

**Primary persona: the informed generalist.** They follow markets closely without trading for a living, and they already read long-form business and finance writing elsewhere. They read far more than they trade: a headline about AI datacenter power demand, or a supply chain reshaped by GLP-1 drugs, catches their attention, and what they want is the shape of the argument — not just the fact that a ticker moved.

They are, deliberately, unlikely to mistake a structured, hedged thesis for a trade signal, which matters as much for the reading experience as for the product's legal footing (`docs/RISKS.md`, Regulatory considerations). This persona is not a marketing detail; it recurs as the deciding factor behind thesis depth and tone (`docs/AI_SYSTEM.md`), publishing cadence (`docs/ROADMAP.md`), and exactly who gets recruited for every quality gate between here and launch (`docs/ROADMAP.md`, M0) (ADR-0001, D-17).

**Anti-persona: the signal-seeker.** Someone who wants a real-time buy/sell alert, a shortcut to picking winners without reading the reasoning behind them, or advice tailored to their own portfolio, goals, or risk tolerance. This isn't a judgment on that reader — it's a statement that Topicron, as scoped, will serve them badly, and that chasing their engagement would pull the product toward the two things it has explicitly committed not to be: a signal service, and a personalized adviser. The second of those is more than a positioning choice — a personalized recommendation is exactly the kind of tailoring `docs/RISKS.md` identifies as risking the shift from "impersonal publisher" to "investment adviser" status under the Investment Advisers Act. (That analysis is not a substitute for advice from a securities attorney; see `docs/RISKS.md` in full.) Every product decision — a feature, a tone choice, a line of marketing copy — should be checked against whether it serves the informed generalist or drifts toward the signal-seeker. Drift toward the signal-seeker is a warning sign, not a growth opportunity.

## Why this is useful before the track record exists

The product's headline claim — a public, unedited track record of how AI-generated theses actually performed — is a compounding asset. It takes six to twelve months of elapsed calendar time before it says anything statistically meaningful, and on launch day it says nothing at all: zero theses, zero history. Even the three-month mark is closer to noise than signal — on the order of fifteen theses, concentrated in high-beta narrative stocks, spanning a single quarter, isn't enough data to distinguish skill from a rising market (ADR-0001, D-01).

That's a real problem for a product whose stated differentiator is exactly that track record: it means the track record cannot be the pitch for the first six months, and the plan needs an honest answer for what *is* worth reading in the meantime. The answer is the thesis itself, on its own terms, before any performance number exists to validate or undercut it.

Concretely, a single Topicron thesis gives a reader something a headline doesn't, independent of how the hypothetical portfolio eventually performs: a bull case and a bear case argued with equal seriousness, a named list of risks instead of a vague caveat, citations back to the actual source material a claim is grounded in, and hedged rather than confident language because the model is estimating, not asserting (`docs/AI_SYSTEM.md`, Hallucination mitigation). That's real, deliverable value in week one — a smaller promise than "we called it," but one the product can keep from day one. It's also the thing the accountability loop needs to be built *on*, not built *instead of*: a thesis that isn't worth reading on its own merits will not become worth reading once a performance chart is attached to it.

The track record is the year-two moat. It is not, and cannot be, the launch pitch.

## What this is

- **A research publication, not a dashboard.** The primary artifact a reader encounters is a published topic-and-thesis page, plus a weekly email that summarizes and links to it — not a logged-in app with filters and a trending feed. That interactive layer is real and coming; it's sequenced after publication proves people read, return, and share, not before (ADR-0001, D-18; `docs/ROADMAP.md`, M5).
- **A research assistant, not a financial advisor.** Every thesis carries a caveat field stating exactly that — not UI copy that can be missed, but a first-class piece of the generated output itself (`docs/AI_SYSTEM.md`).
- **Topic discovery first, stock picking second.** The entry point into every piece of content is a narrative gaining traction, never a ticker with a "buy" or "sell" attached. Company names and tickers are downstream of the narrative, not the starting point.
- **Accountability as the product, not a feature of it.** Every published thesis gets exactly one system-generated hypothetical portfolio, opened at the next close after publication, held for a fixed 90 days with no discretionary exits, and tracked daily against two benchmarks — a broad index and a sector-matched one (ADR-0001, D-13, D-14; `docs/DATA_MODEL.md`). The rule is fixed before the first position ever opens, specifically so it can't be adjusted after the fact to flatter a result.

## What this isn't

- **Not investment advice, and not offered by a registered investment adviser.** `docs/RISKS.md` has the full regulatory framework this positioning depends on.
- **Not a broker.** No real money and no real trades, in the MVP or afterward, until a specific, counsel-reviewed decision changes that (`docs/MVP_SCOPE.md`, Explicitly out of scope).
- **Not a Reddit-sentiment tracker.** That space is commoditized — see "Why this exists," above — and Topicron isn't built on Reddit at all in the MVP regardless, since the Reddit Data API's free tier is restricted to non-commercial use: a licensing question as much as a product one (`docs/MVP_SCOPE.md`; `docs/TECH_STACK.md`).
- **Not personalized, and not going to become personalized without legal review first.** The `suggested_basket` on every thesis is a naive equal weighting applied identically to every reader — never tailored to anyone's holdings, goals, or risk tolerance — because personalization is specifically the boundary between "publisher" and "adviser" (`docs/RISKS.md`, Regulatory considerations; `docs/AI_SYSTEM.md`).
- **Not an interactive dashboard, not at launch.** Filtering, sorting, a trending feed, and watchlists are real, deferred parts of the product, gated on a retention signal from the publication itself (`docs/ROADMAP.md`, M5).

## Why publication, before dashboard

An interactive dashboard is expensive to build well, and it's only measurable at whatever scale the user base happens to be — twenty beta users clicking around a trending feed produces anecdotes, not evidence. A scheduled publication is cheaper to build, measurable at a scale that produces real signal (open and click-through rates across hundreds of subscribers, not dozens), and — as a matter of the regulatory posture described in `docs/RISKS.md` — a fixed weekly cadence fits the "general and regular circulation" language from *Lowe v. SEC* more naturally than a dashboard a reader visits, or doesn't, whenever the market happens to move. Publishing on schedule regardless of whether anything dramatic happened that week is itself part of what keeps this a publication rather than a reaction to hot moments (ADR-0001, D-18; `docs/RISKS.md`).

The rejected alternative was email-only. Theses carry citations, linked companies, and — starting at M4 — performance charts, and none of that renders reliably or attractively in an email client. The actual M3 deliverable is a public, indexable, shareable web page for every topic and thesis, plus a weekly email that summarizes recent publications and links back to those pages. The page is the artifact; the email is the habit-forming delivery mechanism and the one owned channel that survives any single platform's algorithm changing out from under it (`docs/ROADMAP.md`, M3; see also the missing-distribution-plan finding in `docs/RISKS.md`, ADR-0001, D-11).

## The one rule that makes this real

Every mechanism described above is only as good as one commitment: losing theses are shown exactly as prominently as winning ones, forever, with no editorial thumb on the scale. The moment a thesis quietly stops getting daily updates, or a losing position gets less visual weight than a winning one, the "public, unedited track record" claim stops being true — and with it, the entire differentiator this product is testing (`docs/RISKS.md`, Product risks: Survivorship bias). This is a discipline problem more than an engineering one, which is exactly why it's written down here rather than left as an assumed norm.

## MVP philosophy

Five operating principles translate the vision above into concrete build and scope decisions throughout the rest of this documentation set (ADR-0001, Part V — Updated MVP philosophy):

1. **Time-dependent assets start now; everything else waits.** Anything whose value compounds with elapsed calendar time — price history, positions, the track record, the email list — gets built as early as possible, even if no one sees it for months. Anything whose value is available on demand — dashboards, filters, charts, auth — gets built last.
2. **Quality is the gate; code is not.** The project's existential risk is generic, "could go either way" output, and no amount of infrastructure fixes that. Build weeks are estimated up front; quality gates are not, and any gate is allowed to stop the project (`docs/ROADMAP.md`).
3. **Publish on a schedule, in public, unedited.** A fixed cadence serves the reader, the habit, and the regulatory posture at the same time — see "Why publication, before dashboard," above.
4. **Only claim what arithmetic can defend.** Every performance number traces to cached daily price data and the pre-committed 90-day holding rule — never a backtest, never one model grading another model's thesis, never a capability claim the product can't currently demonstrate (`docs/AI_SYSTEM.md`; `docs/RISKS.md`).
5. **Defer with a trigger, not a wish.** Every deferred component — Reddit, a separately deployed backend service, Celery, a vector database, user portfolios — carries a written condition that brings it back (`docs/MVP_SCOPE.md`; `docs/TECH_STACK.md`). "Later," without a stated trigger, is how deferral quietly becomes denial.

`docs/MVP_SCOPE.md` applies these five principles to produce the concrete in-scope, deferred, and out-of-scope lists that follow from them.
