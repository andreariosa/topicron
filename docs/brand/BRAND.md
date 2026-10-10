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
| 5 | First thesis thread | Written when the first new thesis is verified against primary sources. Not scheduled. | to be decided |

**Alt text for the image in #3:** "List of the ten parts of every Topicron thesis: the hypothesis, why now, what the market may be missing, bull case, best bear case, valuation and expectations, catalysts, invalidation conditions (highlighted: what would prove us wrong, stated up front), basket and benchmark, and results at 30, 60 and 90 days."

**Planned slots** (Europe/Rome time; reasoned, not measured):

| Post | Slot | Status |
|---|---|---|
| #1, #2 | Sat 2026-10-10, back to back | to post |
| #3 | Tue 2026-10-13, 16:00 | planned |
| #4 | Thu 2026-10-15, 16:00 | planned |
| #5 | Tue–Thu, when verified | not scheduled |

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
| `src/avatar.html`, `src/banner.html`, `src/ten-parts-card.html` | Sources for the three images. Open each at its exact pixel size and take a screenshot at device scale 1 (headless Chromium was used). They expect Inter installed locally. |

Source: https://help.x.com/en/managing-your-account/how-to-customize-your-profile
