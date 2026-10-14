# Reader Feedback Log (Task 3, M0)

*Responses from target-persona readers. Round 1 used `m0/reader-questionnaire.md`: readers saw write-ups 8 (cybersecurity) and 9 (airlines), both under the ADR-0003 structure, via the Italian translations; its core question is Q2, the M0 gate question per `docs/RISKS.md`. Round 2 (paid panel) used the form in `m0/prolific-form-text.md` on write-up 13 and is recorded below in aggregate only.*

## Round 1 — personal-network distribution, 2026-07-30/31

3 responses from 5 identified readers; founder does not expect further responses from this batch.

| Reader | Q1 (read carefully?) | Q2 (would miss it?) | Q3 (elements that helped) | Q4 (length) | Q5 (cyber vs airlines) | Q6 (would recommend?) | Q7 (want more?) | Q8 (free text) |
|---|---|---|---|---|---|---|---|---|
| R1 | No — skimmed | D — wouldn't read anyway | None in particular | Too long | Neither in particular | Maybe | No | "Don't know" |
| R2 | No — skimmed | A — would genuinely miss it | Hypothesis sentence; valuation section | Right length | Neither in particular | Yes, definitely | Yes, occasionally | (blank) |
| R3 | No — skimmed | B — mild disappointment | Hypothesis sentence; bull/bear confronting each other | Too long | Neither in particular | Maybe | Yes, regularly | (blank) |

## Round 1 read — this is not a valid gate result

**All three respondents answered Q1 "skimmed, not read carefully."** Q1 was built as a calibration check specifically so this situation would be visible rather than silently averaged away. With zero readers who actually engaged with the content, Q2-Q7 don't test whether the writing itself is convincing — they test something closer to a first-impression reaction. **This round does not resolve the M0 gate question either way.**

**What it does suggest, honestly:** 2 of 3 flagged the pieces as "too long," and all 3 skimmed rather than read. These two facts are plausibly connected rather than separate findings — length may be discouraging the reading itself, before the content quality ever gets tested. Worth treating as a real signal, just not the signal the questionnaire was designed to capture.

**Worth naming directly:** all 5 readers in this round came from the founder's personal network, which is exactly the "polite-acquaintance" bias `m0/distribution-list.md` flagged in advance. Three skims out of three is at least as much a signal about *who* was reached as about *what* was sent.

**Recommendation:** don't try to extract more from n=3 skimmed responses. Pivot to `m0/distribution-list.md`'s self-selected channels (r/SecurityAnalysis, r/ValueInvesting, Show HN) for round 2 — readers who choose to click in are a structurally different (and more relevant) sample than obligated acquaintances. Consider testing a shorter version of one write-up alongside the current length as a lightweight A/B check, given the length signal above.

## Round 2 — paid reader panel (Prolific), 2026-10-13

*Write-up 13 (US wireless carriers and the SpaceX spectrum deal), read in English by people who say they buy individual stocks: Study A the full text (10 readers), Study B the one-page version (6 readers). Setup, cost and rules: `m0/prolific-study-spec.md`. The form's consent text says answers are reported in aggregate and raw answers are not published, so this section holds counts, medians and grouped themes only: no per-reader rows, no quotes, no Prolific IDs. The raw files stay on the founder's computer.*

### Who read, and how

| | Study A (full text) | Study B (one page) |
|---|---|---|
| Completed | 10 | 6 |
| Screened out in the form | 0 | 1 (Prolific counts 2; the second left no form response) |
| Median completion time (estimate) | 12.3 min (20) | 10.2 min (10) |
| All four content questions right | 8 of 10 (one had 3, one had 2) | 6 of 6 |
| Read "all of it, carefully" / "most of it" | 7 / 3 | 4 / 2 |
| Failed an attention check | 1 failed one; nobody failed two | none |
| Rejected | 0 | 0 |

### Ratings (1 = strongly disagree, 4 = strongly agree; median, and how many agreed)

Study A is the 9 readers with at least 3 of 4 content answers right (the spec's rule); Study B is all 6.

| Statement | Study A (n=9) | Study B (n=6) |
|---|---|---|
| The piece was clear about what it claims | 3 (9 agreed) | 4 (6) |
| Its claims were supported by evidence or sources | 4 (9) | 3.5 (6) |
| It was clear what would show the thesis to be wrong | 4 (8) | 4 (6) |
| It could have been written about almost any stock | 2 (4) | 3 (4) |
| The bear case was a serious challenge, not a token one | 4 (8) | 3 (4) |
| The tone felt like selling a stock | 2 (2) | 2 (2) |

Study B without the one reader who answered "No" to the first screening question (n=5): the same medians, except "supported", which is 4. Study A with all 10 readers: 3.5, 4, 4, 2.5, 3.5, 2.

### Against the thresholds (spec §5), Study A

| Threshold | Result | Met |
|---|---|---|
| Median of at least 3 on "clear" | 3 | Yes, at the limit |
| Median of at least 3 on "supported by evidence" | 4 | Yes |
| Median of 2 or lower on "could have been written about almost any stock" | 2 (4 of 9 agreed it could be about any stock) | Yes, at the limit |
| At least half name a specific weakest assumption | 5 of 9, or 6 counting one borderline answer that attributes the market's fear to the thesis itself | Yes, at the limit |

"Specific" is the analyst's judgment (Claude's) from the open answers.

### Most useful parts (each reader picked up to three)

| Part | Study A (10) | Study B (6) |
|---|---|---|
| The conditions that would prove it wrong | 7 | 6 |
| What the market may be missing | 6 | 2 |
| The valuation | 5 | 2 |
| The one-sentence hypothesis | 3 | 0 |
| The dated catalysts | 3 | 2 |
| The best bear case | 2 | 2 |
| The basket and its weights | 2 | 1 |
| Why now | 0 | 2 |
| The bull case | 0 | 0 |

13 of 16 readers picked the invalidation conditions.

### What readers said, grouped

- **The weakest assumption, the same in both studies: that a good Q3 reverses the sell-off.** 8 of 16 (5 of 10, 3 of 6) named some form of it: the market may keep re-rating on long-run value whatever the quarter shows. The write-up already says so in its best bear case and in invalidation condition 3, so readers found the crux, not a gap.
- **The benchmark side (Study B only, 2 of 6).** Nothing in the piece about what could move the S&P 500 itself, for example index concentration in AI-related stocks.
- **The size and timing of the SpaceX threat (3 of 10 in Study A).** Named as the weakest assumption, but in vague terms.
- **More evidence wanted (4 of 10 in Study A, 1 of 6 in Study B).** More proof that the market overreacted, a deeper look at the numbers, or the valuation assumptions felt abstract (the 9-10% required return is labelled in the piece as the author's assumption). One reader asked for examples of how similar sell-offs recovered in the past.
- **Clarity (Study B).** One reader found the page dense; one wanted the competitive dynamics between satellite and terrestrial carriers clarified; one wanted the difference between the spectrum valuations explained.
- **Facts.** No reader identified a factual error. One flagged the $8 billion figure as unsupported, which the piece already labels as an unconfirmed press report.
- **Dates.** 2 of 10 in Study A gave 28 October (T-Mobile's report and the FOMC decision) as AT&T's date, although the catalysts section lists each date separately; one of them also chose the wrong invalidation condition.
- **Length.** 9 of 10 in Study A called the full text about right; 2 of 6 in Study B called the one-pager too long.

### Study B against Study A

The spec's rule: if B scores within one point of A on clarity, content accuracy and the weakest assumptions named, the one-page version becomes the default reading format for the public post and the email. B matched or beat A on clarity (median 4 against 3), on content accuracy (6 of 6 with all four right against 8 of 10) and on naming a specific weakest assumption (5 of 6 against 5 of 9). The largest gaps against B are one point each, on "could have been written about almost any stock" (3 against 2) and on "serious bear case" (3 against 4). **The rule is met.** Those two are the measures a compressed version should be expected to hurt, so they are the ones to watch; the full text stays linked from the one-pager.

### Limits and anomalies

- Paid readers. The persona match rests on Prolific's profile filters and on the answers to two screening questions in the form.
- 16 readers in total: counts, not percentages.
- One reader per study gave the top rating to every statement, including the reversed ones ("any stock", "selling a stock"). Both are kept, because the pre-set rule excludes only readers with fewer than 3 of 4 content answers right; they add to the "any stock" counts.
- One Study B reader answered "No" to "do you personally buy and sell individual company stocks" and still completed the form, which should have sent them to the screen-out page. The routing needs a check in the form's preview. They are counted in Study B's numbers; the alternative is shown above.
- The thresholds were mapped from a five-point to the form's four-point scale after the three pilot responses had been read (spec §5).

### Carry-forward to the next write-ups: bear-case checklist

An assumption named by two or more readers goes on the checklist (spec §5). No checklist file existed. It is kept here until the thesis template changes through an ADR (ADR-0003 governs the structure). Write-up 13 is not changed.

1. **Catalyst to price.** If the catalyst happens as hoped, what else must be true for the price to respond? Say what you would conclude if the catalyst is good and the price does not move. (8 of 16 readers)
2. **Benchmark.** What could make the benchmark beat the basket (index concentration, a rally in its largest holdings), and does the threshold allow for it? (2 of 6, Study B)
3. **Threat size and timing.** Separate how large the named threat could become from when it could bite, and tie each to a dated, observable event. (3 of 10, Study A, in vague terms)

### Open question for the founder: precedent examples

One reader asked for examples of how similar sell-offs recovered in the past. ADR-0001 D-02 bars published backtests of generated theses (lookahead contamination) and `AGENTS.md` §7 words the refusal as "a published backtest or historical performance figure, under any framing". Whether third-party precedents, which are not a backtest of Topicron's own theses, count is not stated in either text. Write-up 13 contains one precedent, labelled as a single observation with the causal link marked as inference. Nothing was changed; a founder reading is needed before precedent examples are added to new write-ups.

### Round 2 read

The quality half of the gate can now be read. The thresholds are met, three of four at the limit. The strongest signal is that 13 of 16 careful readers picked the invalidation conditions among the most useful parts; the weakest is genericity (4 of 9 in Study A and 4 of 6 in Study B agree the piece could be about almost any stock). The one-page version holds up against the full text. **The demand half is untested:** paid readers cannot answer "would you miss this" without inflation (`m0/prolific-study-spec.md` §1) and round 1 was three skimmers. Nothing here changes the hypothesis of write-up 13.
