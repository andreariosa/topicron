# BRAND.md

*Working brand notes for Topicron's public presence during M0: palette, type, the mark, the rules public visuals follow, and the X (@topicron) profile copy, assets and post plan. Presentation only — nothing here touches scope, architecture or cost, so no ADR applies (`AGENTS.md` §9). It is not a design system; the real site and its styling are a later decision (M3).*

## 1. Palette

| Token | Hex | Used for | Contrast on ink |
|---|---|---|---|
| Ink | `#0E1424` | Backgrounds | — |
| Paper | `#F3EFE6` | Headlines, marks, primary text | 15.99 : 1 |
| Slate | `#9AA3B5` | Secondary text, numbers, axis labels | 7.24 : 1 |
| Amber | `#E9A23B` | **One meaning only: what would prove the thesis wrong** (invalidation conditions, thresholds) | 8.47 : 1 |

Contrast ratios are WCAG relative-luminance ratios computed on 2026-10-10. Amber is deliberately scarce: if it appears anywhere, it marks an invalidation condition or a threshold, so a reader learns to look at it first.

The palette is not yet aligned with the landing page in `app/`; align one to the other when either is next touched.

## 2. Type

Inter (open source, SIL Open Font License): 700 for headlines, 600 for labels and list items, 500 for body and captions. Fall back to the system sans-serif.

## 3. The mark

A paper-coloured "T" crossed by an amber line that the stem interrupts: the thesis stands on a threshold it has to survive. Geometry lives in `src/avatar.html` (T bar 190 × 44, stem 44 × 158, threshold segments 104 × 7, on a 400 × 400 canvas, cropped to a circle by X).

## 4. Rules for anything public

1. **No performance figures or price charts** until real, tracked data exists. `AGENTS.md` §7 forbids published backtests or historical performance under any framing; a decorative chart that implies results counts. Schematic diagrams of the format are fine (the banner is one).
2. **Disclose AI assistance** wherever the work is described. It is also the project's pitch: transparency.
3. **"Hypotheses, not investment advice."** stays visible in the bio and on image cards (`docs/RISKS.md`, publisher's-exclusion posture).
4. **Do not promise a track record that does not exist yet.** Say how theses are judged (30/60/90 days), not how they have performed.
5. No stock photography, no third-party logos, nothing personal in any image (this repository is public).

## 5. X profile, @topicron

Specifications confirmed on X's help page ("How to customize your profile", read 2026-10-10): profile photo 400 × 400 px; header 1500 × 500 px; bio maximum 160 characters; JPG, GIF or PNG, no animated GIFs; the display-name option appears only after a profile photo and a header photo are uploaded; a post is pinned from its menu ("Pin to your profile"). The page states no limit for display name or location.

| Field | Value |
|---|---|
| Display name | `Topicron` |
| Profile photo | `x/topicron-x-avatar-400x400.png` |
| Header | `x/topicron-x-banner-1500x500.png`. Keep the lower-left corner empty: the profile photo overlaps it. |
| Website | `topicron.vercel.app` |
| Location | Leave empty |

**Bio** (pick one; update the "in use" line when set):

1. `Investment theses with a stated way to be wrong. AI-assisted, source-checked, judged at 30/60/90 days. Early stage. Not investment advice.` (138)
2. `Falsifiable investment theses, written with AI and checked against primary sources. Each one says how it could be wrong. Hypotheses, not advice.` (144)
3. `AI-assisted equity research that states up front how it could be wrong. Early stage, looking for critique. Hypotheses, not investment advice.` (141)

In use: option 1 (recommended). Edit this line if a different one goes live.

## 6. X posts

All texts are under 280 characters. Counts are characters including line breaks.

| # | Post | Text | Image |
|---|---|---|---|
| 1 | Pinned intro (259) | Topicron is an experiment: investment theses written with AI assistance, each stating up front how it could be wrong, checked against primary sources, and judged at 30, 60 and 90 days.<br><br>Early stage. I want critique more than followers. Hypotheses, not advice. | none |
| 2 | Disclosure, as a reply under #1 (155) | Disclosure: the drafts are written with AI (Claude). I check the figures against filings and company releases. If you spot an error, reply and I'll fix it. | none |
| 3 | Format (273) | Every Topicron thesis has the same ten parts: hypothesis, why now, what the market may be missing, bull case, best bear case, valuation, catalysts, invalidation conditions, basket and benchmark, results at 30/60/90 days.<br><br>The one that matters most: invalidation conditions. | `x/post-ten-parts-card-1600x900.png` |
| 4 | Why (211) | Most investment writing can't be proven wrong, because it never says what would prove it wrong.<br><br>Every thesis I publish here names that condition before anything happens, so the result at day 90 means something. | none |
| 5 | First thesis thread (write-up 13, five posts) | Text in `m0/topic-thesis-13-distribution-copy.md` §2. Written 2026-10-11 from a thesis checked against primary sources. Goes out only after the thesis commit is on `main`. | `x/post-thesis-13-card-1600x900.png` on the first post |
| 6 | Project status (262) | Where Topicron stands: 13 theses written by hand, one tested on 16 paid readers, a daily price record since 27 Oct. Not yet known: would anyone miss it? I count that on 16 Nov.<br><br>If you read markets, tell me what would make you come back. AI-assisted. Not advice. | `x/post-status-card-1600x900.png` |
| 6b | Link, as a reply under #6 (52) | If you'd rather follow by email: topicron.vercel.app | none |

**Alt text for the image in #3:** "List of the ten parts of every Topicron thesis: the hypothesis, why now, what the market may be missing, bull case, best bear case, valuation and expectations, catalysts, invalidation conditions (highlighted: what would prove us wrong, stated up front), basket and benchmark, and results at 30, 60 and 90 days."

**Alt text for the image in #6:** "Status card, 28 October 2026. Done: 13 hand-written theses; 16 paid readers tested the format, and the pre-set quality bar was met, narrowly. Running: thesis 13 is being judged, with results at day 30, 60 and 90 (11 November, 11 December, 11 January); closing prices have been saved daily since 27 October. Not yet known, highlighted: would anyone miss it? What would prove this wrong, counted on 16 November."

**Planned slots** (Europe/Rome time; reasoned, not measured):

| Post | Slot | Status |
|---|---|---|
| #1, #2 | Sat 2026-10-10, back to back | to post |
| #3 | Tue 2026-10-13, 16:00 | planned |
| #4 | Thu 2026-10-15, 16:00 | planned |
| #5 | Wed 2026-10-14, 16:00 (after the thesis commit) | to schedule; move to the next Tue–Thu if the commit slips |
| #6, then #6b | Tue 2026-11-03, 16:00 (10:00 in New York after the US clock change on 11-01) | proposed 2026-10-28; the founder scheduled it on X the same evening. The thesis updates after AT&T, Verizon and T-Mobile (10-21, 10-26, 10-28) are not numbered here. Before posting: check that the daily price record is still running (a red Prices run would make the card wrong), and regenerate the card if the post slips past 2026-11-10 (the counts and the date on it are as of 2026-10-28) |

The slots are weekday US-morning times: 16:00 in Rome is 10:00 in New York until 2026-10-25 (Europe's clocks change that day, the US's on 2026-11-01) and 11:00 until 2026-11-01. They are a starting guess for an audience that reads on weekdays, not a measured optimum. After two or three weeks, compare the impressions shown on each post and adjust. Whether X's composer offers scheduling for this account was not verified; if it does not, post by hand at the nearest convenient time.

One post per day at most, two per week until there is a thesis to share. An account with no followers gets almost no reach however good the timing is.

## 7. What X is for in M0

A credibility surface, not a feedback channel: it is what a moderator, a Reddit reader or an independent analyst sees when they check who is asking (`m0/round-2-channels.md`, channels B and D). Feedback is expected from the channels in that file.

## 8. Files

| Path | What |
|---|---|
| `x/topicron-x-avatar-400x400.png` | Profile photo |
| `x/topicron-x-banner-1500x500.png` | Header |
| `x/post-ten-parts-card-1600x900.png` | Image for post #3 |
| `x/post-thesis-13-card-1600x900.png` | Image for the first post of the thesis thread (#5). No price or performance figure |
| `x/post-status-card-1600x900.png` | Image for post #6 (project status). Counts and dates only: no price or performance figure. Amber marks the project's own falsifier (amber's one meaning, section 1), as in the other cards |
| `src/avatar.html`, `src/banner.html`, `src/ten-parts-card.html`, `src/thesis-13-card.html`, `src/status-card.html` | Sources for the five images. Open each at its exact pixel size and take a screenshot at device scale 1 (headless Chromium was used). They expect Inter installed locally. |

Source: https://help.x.com/en/managing-your-account/how-to-customize-your-profile
