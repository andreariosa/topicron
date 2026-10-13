# Prolific study spec (M0, task 3, channel A)

*A paid panel of readers who say they invest in individual stocks, to get careful reads of write-up 13 and test the one-page version against the full text. Approved by the founder on 2026-10-12 (chat) with a hard cap of EUR 100; `AGENTS.md` §6 ("Money") makes this his call and it is recorded here and in `m0/intervention-log.md`. One-off validation spend, not a stack component, so ADR-0002 D-19 is not touched. Facts about Prolific were read from its researcher help pages on 2026-10-12; anything not read is marked **unverified**.*

## 1. What this can and cannot show

- **Can show** (the quality half of the M0 gate): whether a careful, paid reader finds the thesis clear, supported, falsifiable and not generic; where they get lost; which weak assumptions they name; whether the one-page version is understood as well as the full text.
- **Cannot show:** demand. Paid readers are paid to read, so "would you miss this" is inflated and is **not asked**. The gate's "how would you feel if this no longer existed" question must come from channels where people read for free (`docs/RISKS.md`).
- **Cannot change the thesis.** Write-up 13 was published on 2026-10-12 (commit time = `published_at`) and its hypothesis is tracked from the 12 October close. Reader critiques go to the next write-ups and the template; a factual error found by a reader is fixed with a dated note, never by rewording the hypothesis.

## 2. Design

| | Study A (full text) | Study B (one page) |
|---|---|---|
| Reads | `m0/topic-thesis-13-us-wireless-spacex.md` on GitHub (about 2,100 words to read) | `m0/topic-thesis-13-one-page.md` on GitHub (about 700 words) |
| Estimated time | 20 minutes | 12 minutes |
| Reward | $4.00 ($12.00 per hour, Prolific's recommended rate) | $2.40 ($12.00 per hour) |
| Places | 10, published in two steps: 3 as a pilot, then 7 | 6 |
| Questionnaire | Identical in both (`m0/prolific-form-text.md`) | Identical in both |

With 10 and 6 readers this is qualitative evidence, not a statistical test. Report counts, not percentages.

**Who.** People in the United States, fluent in English, who personally buy individual stocks and read company analysis at least monthly. Prolific's help pages list no investing filter (they list country, age, job role, education and languages as examples, and call custom screening the fallback for niche groups). So: open the filter list in the study setup and search for "invest", "stock" and "share"; if a matching filter exists, use it. If not, use the two screener questions at the start of the form and send non-matching people to the "screened out" path (Prolific then pays them the screen-out reward you set at creation).

**Quality rules from Prolific's policy (read 2026-10-12), applied here:**
- Reject only for: two failed valid attention checks (the study is longer than 5 minutes, so one failure is not enough), skipped required questions, clear low effort across the whole study, or a completion time more than 3 standard deviations faster than the mean.
- Content questions about the text (`C1`-`C4`) are **analysis measures only**. Failing them is not a ground for rejection and the person is still paid; Prolific's comprehension-check rules do not allow rejecting on them.
- The form includes one instructional check and one nonsensical item, both on the same page, so that the two-check rule can be applied if someone clicks through.
- Approve everyone else. Submissions left unreviewed for 21 days are auto-approved.
- Prolific IDs are pseudonymous personal data. Raw responses stay on your computer; only anonymous aggregates enter the repository.

## 3. Cost (one calculation, USD per EUR 1.1206 on 2026-10-09, Banca d'Italia)

| Item | USD | EUR |
|---|---|---|
| Rewards: 10 x $4.00 + 6 x $2.40 | 54.40 | 48.55 |
| Platform fee, 42.857% (corporate rate; the account is not academic or non-profit) | 23.31 | 20.80 |
| **Subtotal** | **77.71** | **69.35** |
| VAT on the fee, worst case 22% (VAT applies to the fee only; the rate for you is **unverified**) | 5.13 | 4.58 |
| Screen-outs, worst case: 16 people x $0.40 plus fee and VAT (assumes about half of entrants fail the screener; the screen-out amount is set by you at creation) | 9.75 | 8.70 |
| **Worst case** | **92.59** | **82.63** |

The cap of EUR 100 is $112.06. **Top up $100 (about EUR 89), not more.** The workspace balance is a hard ceiling on spending. Before publishing each study, read the total the Prolific setup page shows and stop if it disagrees with this table. Card or currency-conversion fees on the top-up are not included. Workspaces are in GBP or USD; this spec uses USD.

## 4. Steps (you; Prolific needs your account and card)

1. Commit this batch to `main` so that `topic-thesis-13-one-page.md` has a live link. Re-sync the Claude Project.
2. Create the Google Form from `m0/prolific-form-text.md`. Turn email collection off for both responses and form defaults. Make a second copy for Study B and change only the reading link and the time statement.
3. Create the Prolific researcher account and workspace in USD; top up $100.
4. Create Study A as an external study (the form link). Prolific cannot be redirected to from Google Forms, so use the **completion code** method, show the code on the form's last page, and add the Prolific ID question in the form. Set up the "screened out" path and put its code in the form's screen-out page. Set filters (country, language, any investing filter), desktop only, estimated time 20 minutes, reward $4.00, **3 places**. Read the price shown, then publish.
5. Pilot: when the 3 submissions arrive, check the median completion time against 20 minutes, read the open answers, and fix wording problems in the form. If the real time is far from the estimate, change the estimate and reward in the later study (keep the hourly rate at $12.00, Prolific's recommended rate; its minimum is $8.00).
6. Wave 2: raise Study A to 10 places, and create Study B with 6 places, excluding the people who did Study A (use Prolific's option to exclude participants of previous studies; **check it exists in the UI**).
7. Approve submissions as described in §2. Export the responses to a local CSV, remove the Prolific ID column, and send me the file. I will return the analysis and the draft log entry.

Timeline: pilot Tuesday 13 October, second wave by Wednesday 14 October, analysis by about Monday 19 October. The M0 gate date (proposed 2026-11-07) does not move.

## 5. Analysis rules, fixed before any data

Report, for each study: number of completed and screened-out readers, median completion time, the share who answered at least 3 of the 4 content questions correctly (a reading-depth measure to set beside the self-report), the median of each 1-5 item, the sections picked as most useful, and the open answers grouped by theme.

**Proposed thresholds for the quality half of the gate (your decision to accept or change before the data arrives):** among readers with at least 3 of 4 correct content answers, a median of at least 4 on "clear" and on "supported by evidence", a median of 2 or lower on "could have been written about almost any stock", and at least half naming a specific weakest assumption instead of "none". An assumption named by two or more readers is added to the next write-ups' bear-case checklist.

Study B is judged against Study A on clarity, content accuracy and the weakest assumptions named. If B scores within one point of A, the one-page version becomes the default reading format for the public post and the email.

## 6. Open items

- **Unverified:** whether Prolific reviews or objects to a study asking for feedback on written investment content (no page read prohibits it; the pilot is also the test); the VAT rate charged to you; the screen-out reward minimum; whether the exclusion option and an investing filter exist in the current UI.
- **Risk:** respondents using AI to write the open answers. Read them for specifics (named numbers, named sections); reject only on Prolific's valid grounds.
- **Not done here:** the Reddit and outreach channels, which run in parallel (`m0/round-2-channels.md`).
