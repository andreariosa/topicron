# Prolific study spec (M0, task 3, channel A)

*A paid panel of readers who say they invest in individual stocks, to get careful reads of write-up 13 and test the one-page version against the full text. Approved by the founder on 2026-10-12 (chat) with a hard cap of EUR 100; `AGENTS.md` §6 ("Money") makes this his call and it is recorded here and in `m0/intervention-log.md`. One-off validation spend, not a stack component, so ADR-0002 D-19 is not touched. Facts about Prolific were read from its researcher help pages on 2026-10-12 and 2026-10-13, or observed in the study setup pages on 2026-10-13; anything not read or observed is marked **unverified**. Both studies ran on 2026-10-13: what happened is in §7 and the results are in `m0/reader-feedback-log.md` (Round 2).*

## 1. What this can and cannot show

- **Can show** (the quality half of the M0 gate): whether a careful, paid reader finds the thesis clear, supported, falsifiable and not generic; where they get lost; which weak assumptions they name; whether the one-page version is understood as well as the full text.
- **Cannot show:** demand. Paid readers are paid to read, so "would you miss this" is inflated and is **not asked**. The gate's "how would you feel if this no longer existed" question must come from channels where people read for free (`docs/RISKS.md`).
- **Cannot change the thesis.** Write-up 13 was published on 2026-10-12 (commit time = `published_at`) and its hypothesis is tracked from the 12 October close. Reader critiques go to the next write-ups and the template; a factual error found by a reader is fixed with a dated note, never by rewording the hypothesis.

## 2. Design

| | Study A (full text) | Study B (one page) |
|---|---|---|
| Reads | `m0/topic-thesis-13-us-wireless-spacex.md` on GitHub (about 2,100 words to read) | `m0/topic-thesis-13-one-page.md` on GitHub (about 700 words) |
| Estimated time | 20 minutes | 10 minutes (the first draft said 12; lowered after Study A's measured median, 12.3 minutes, came in far under its 20-minute estimate) |
| Reward | £3.33 (£9.99 per hour) | £1.67 (£10.02 per hour) |
| Places | 10, published in two steps: 3 as a pilot, then 7 | 6 |
| Screen-out slots (£0.30 each) | 10 | 6 |
| Questionnaire | Identical in both (`m0/prolific-form-text.md`) | Identical in both |

With 10 and 6 readers this is qualitative evidence, not a statistical test. Report counts, not percentages.

The workspace currency is GBP (the first draft assumed USD). The setup page flagged "high study competition" and a competitive band of £15.90 to £27.00 per hour for this audience; the approved cap rules that out, and at about £10 per hour both studies filled the same day (§7).

**Who.** People resident in the United States, fluent in English, who say they invest in the stock market and who, in the form's two screening questions, say they personally buy individual stocks and read company analysis at least monthly. The filters in Prolific's setup page (observed 2026-10-13): Current Country of Residence = United States; Investment = Yes; Types of investment = Stock Market; English speaking = all three options; combined with AND (the default across categories; an AND/OR toggle exists). The eligible pool was about 12,100 people. The filters are profile data that participants entered themselves, hence the two screeners at the start of the form: a participant who fails one is sent to the "Screened out" completion path and paid the screen-out reward (Prolific's custom screening). Study B also excludes the participants of Study A ("Exclude participants from other studies", category "Participation on Prolific").

**Quality rules from Prolific's policy (read 2026-10-12), applied here:**
- Reject only for: two failed valid attention checks (the study is longer than 5 minutes, so one failure is not enough), skipped required questions, clear low effort across the whole study, or a completion time more than 3 standard deviations faster than the mean.
- Content questions about the text (`C1`-`C4`) are **analysis measures only**. Failing them is not a ground for rejection and the person is still paid; Prolific's comprehension-check rules do not allow rejecting on them.
- The form includes one instructional check and one nonsensical item, both on the same page, so that the two-check rule can be applied if someone clicks through.
- Prolific's own "reject exceptionally fast submissions" option (beta) is left off, because it would reject on a ground this list does not include.
- Approve everyone else. Submissions left unreviewed for 21 days are auto-approved.
- Prolific IDs are pseudonymous personal data. Raw responses stay on the founder's computer; only anonymous aggregates enter the repository. The form's consent text promises that answers are reported in aggregate and raw answers are not published, so the repository holds no per-reader rows or quotes.

## 3. Cost

Amounts are Prolific's own totals at the confirmation step, in GBP, VAT included.

| Step | Total |
|---|---|
| Study A pilot: 3 places plus the 10 screen-out slots | £19.67 |
| Study A, 7 more places | £35.26 (rewards £23.31, platform fee £9.96, VAT £1.99) |
| **Study A** (Prolific's own total; the two steps above add to £54.93, a 2p rounding difference) | **£54.91** |
| **Study B**: 6 places plus 6 screen-out slots | **£17.90** |
| **Both studies** | **£72.81** |

How it adds up (observed): the platform fee is between 42.7% and 42.9% of the rewards plus the screen-out budget (Prolific's published corporate rate is 42.857%), and VAT is 20% of the fee, not of the rewards. Screen-out slots are budgeted and charged upfront at publication.

The cap of EUR 100 is £84.48 at 1 EUR = 0.84478 GBP (ECB reference rate, 2026-10-12). The £72.81 above is about EUR 86. When a study is published Prolific sets aside the cost of all its places from the balance; stopping the study returns the money for unfilled places. Screened-out submissions do not count towards the places and are paid the fixed screen-out reward (read 2026-10-13). The workspace balance limits what can be reserved; the cap is enforced by comparing each confirmation total with the estimate before publishing. The amount actually spent, after any refund of unused screen-out slots, is recorded in `m0/intervention-log.md` once the Finance page has been read.

## 4. Steps as run

1. Commit the batch so that `topic-thesis-13-one-page.md` has a live link, and re-sync the Claude Project (done 2026-10-13).
2. Create the Google Form from `m0/prolific-form-text.md` (build notes are at the end of that file). Email collection off, no file-upload question. Study B's form is a copy of Study A's with the reading link and the time statement changed; the copy keeps the routing and the completion codes.
3. Create the Prolific researcher account and workspace (GBP), add funds.
4. Create Study A as an external study (the form link). Record Prolific IDs with "a question in my study". Google Forms cannot redirect to Prolific, so use the completion code: copy the code from Completion paths and show it on the form's last page; add a custom-screening path called "Screened out" with its own code, slots and fixed reward. Add the filters in §2, desktop only, estimated time 20 minutes, 3 places, and publish (scheduled publish 16:00).
5. Pilot: check the median completion time, read the open answers, fix wording problems in the form (after publishing, reward, estimated time, title, description, URL and the prescreening filters cannot be changed; only the internal name and the number of places can).
6. Wave 2: in Study A's Action menu, "Increase places" by 7 (the extra cost is shown before confirming).
7. Study B: once Study A had all 10 places complete, duplicate it with the original participants blocked. The duplicate keeps the filters (including the exclusion of Study A), the screening path and the completion codes. Change the internal name, public title, description, form URL, estimated time, reward, places and screen-out slots, then check the confirmation step line by line: it caught two inherited errors (10 places instead of 6, and a description that still said 20 minutes). Publish.
8. Approve submissions under the rules in §2. Export the responses to a local CSV, keep it out of the repository, analyse, and record only aggregates.

## 5. Analysis rules

Report, for each study: the number of completed and screened-out readers, the median completion time, the share who answered at least 3 of the 4 content questions correctly (a reading-depth measure to set beside the self-report), the median of each 1-4 item (1 = strongly disagree, 4 = strongly agree), the sections picked as most useful, and the open answers grouped by theme.

**Thresholds for the quality half of the gate**, accepted by the founder on 2026-10-13: among readers with at least 3 of 4 correct content answers, a median of at least 3 ("somewhat agree" or better) on "clear" and on "supported by evidence", a median of 2 or lower on "could have been written about almost any stock", and at least half naming a specific weakest assumption instead of "none". An assumption named by two or more readers is carried forward to the next write-ups' bear-case checklist (`m0/reader-feedback-log.md`).

*Limit of the pre-registration:* the first draft of this section assumed a five-point scale (medians of at least 4 and at most 2). The form has four answer options, so the thresholds were mapped to the four-point scale on 2026-10-13 **after the three pilot responses had been read** and before the other thirteen. The mapping was made to fit the scale, not tuned to the pilot, but this is not a pure pre-registration. Whether an assumption is "specific" or vague is the analyst's judgment (Claude's), reported with the borderline cases so the founder can reclassify.

Study B is judged against Study A on clarity, content accuracy and the weakest assumptions named, using the medians and counts above. If B scores within one point of A, the one-page version becomes the default reading format for the public post and the email.

## 6. Open items

- **Verified 2026-10-13** on researcher-help.prolific.com (articles 445183 Google Forms, 445170 completion codes, 445165 screening inside a study, 445164 excluding participants, 445201 increasing places, 445203 what can change after publishing, 445132 publishing, 445134 testing as a participant, 445241 and 445242 adding money, 445230 payment model).
- **Observed in practice, 2026-10-13:** the investing filters exist in the setup page; a duplicated study keeps its filters, screening path and completion codes; the "Median time" tile on a study page shows the estimate, not the measured median; the screen-out reward of £0.30 and VAT of 20% on the fee were accepted; both studies were published and ran to completion, and no objection to a study asking for feedback on written investment content was reported.
- **Unverified:** whether unused screen-out slots are refunded; whether Prolific asks for an extra payment for Study B (measured median 10.2 minutes against a 10-minute estimate); whether Study B's form routes an answer of "No" on the first screening question to the screen-out page (one reader answered "No" and completed the form; check in the form's preview).
- **Risk:** respondents using AI to write the open answers. Read them for specifics (named numbers, named sections); reject only on Prolific's valid grounds. No clear sign found in either study.
- **Not done here:** the Reddit and outreach channels, which run in parallel (`m0/round-2-channels.md`).

## 7. What happened (2026-10-13, Rome time)

- **Study A.** Published at 16:00 with 3 places; the pilot submissions were in by about 16:35. The pilot review found a typo in one form question and the scale mismatch described in §5; 7 places were added in the late afternoon and all 10 were complete by about 19:00. No screen-outs (0 of 10 slots used), one submission returned, no rejections.
- **Study B.** Published at 20:11 as a duplicate of Study A with its participants blocked; all 6 places were complete by about 21:00, 2 of 6 screen-out slots used, no rejections. No participant took both studies (compared by ID, locally).
- **Time.** Measured median completion time: Study A 12.3 minutes (estimate 20), Study B 10.2 minutes (estimate 10).
- **Attention checks.** One reader failed one check; nobody failed two.
- **Anomalies.** One Study B reader answered "No" to the first screening question and still completed the form (see §6). One of Study B's two screen-outs left no form response, probably because the person copied the screen-out code without pressing Submit (inference).
- **Results and spend.** Results: `m0/reader-feedback-log.md`. Spend: §3 and `m0/intervention-log.md`.
