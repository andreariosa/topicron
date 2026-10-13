# Prolific form text (Google Forms), M0 task 3

*Copy-paste text for the form described in `m0/prolific-study-spec.md`. Make two copies of the form: Study A (full text) and Study B (one page). They differ only where marked **[A]** or **[B]**. Replace `[CONTACT EMAIL]` with the address you want participants to use; that address is deliberately not written here because this repository is public. Form settings: collect no email addresses; require the Prolific ID and the questions marked (required); one question per line unless a grid is stated.*

## Section 1. About this study

**Title:** Reading and critiquing an investment analysis

You will read an investment analysis and then answer questions about it. It takes about **[A] 20 minutes / [B] 12 minutes**.

What you should know before you start:
- The analysis was written with AI assistance (Claude) and checked against company filings and releases by its author. It is a hypothesis being tracked over 90 days, **not investment advice**. Please do not trade on it.
- We want an honest critique. Disagreement and "I don't think this holds" are useful answers.
- We collect your Prolific ID and your answers. We do not ask for your name, email or any other personal details. Answers are used to improve a research project and are reported only in aggregate; raw answers are not published. They are stored in the researcher's Google account.
- You can stop at any time by closing the form and returning your submission on Prolific.
- Questions: [CONTACT EMAIL]

Do you agree to take part on these terms? (required)
- Yes, I agree
- No, I do not agree *(go to the end of the form: "Thank you, you can return your submission on Prolific.")*

## Section 2. Prolific ID

Please enter your Prolific ID. (short answer, required)

## Section 3. Two quick questions

**S1.** Do you personally buy and sell individual company stocks (not only funds or ETFs)? (required)
- Yes
- No *(go to the screen-out page)*

**S2.** How often do you read analysis of individual companies (articles, newsletters, research notes)? (required)
- Weekly or more
- A few times a month
- About once a month *(these three continue)*
- A few times a year or less *(go to the screen-out page)*
- Never *(go to the screen-out page)*

**Screen-out page:** Thank you. This study needs people who regularly buy individual stocks and read company analysis, so we cannot continue with you. Please enter this code on Prolific to be paid for your time: **[SCREEN-OUT CODE from Prolific]**

## Section 4. The reading

Open the link below and read the whole piece. You may keep it open while you answer.

**[A]** https://github.com/andreariosa/topicron/blob/main/m0/topic-thesis-13-us-wireless-spacex.md
Read from the title down to the end of the section called "Basket and benchmark". You may skip the sections called "Results at 30/60/90 days" and "Sources", and the structured data at the very end. (This is about 10 minutes.)

**[B]** https://github.com/andreariosa/topicron/blob/main/m0/topic-thesis-13-one-page.md
Read the whole page. (This is about 3 minutes.)

## Section 5. Questions about what you read

Choose the best answer. Your answers here do not affect your payment.

**C1.** Which company has the smallest weight in the proposed basket? (required)
- Verizon
- AT&T
- T-Mobile
- All three are weighted equally

**C2.** What is the proposed benchmark? (required)
- The S&P 500 (SPY)
- The Nasdaq 100
- A telecom sector fund
- There is no benchmark

**C3.** Which of these is one of the stated conditions that would show the thesis is wrong? (required)
- The Federal Reserve cuts interest rates
- Verizon raises its dividend
- SpaceX publishes Starlink Mobile pricing or a launch date before the end of 2027
- SpaceX launches another batch of satellites

**C4.** On what date does AT&T report its third-quarter results? (required)
- 21 October
- 26 October
- 28 October
- 5 November

**R1.** How much of the piece did you read? (required) *Be honest: this does not affect your payment.*
- All of it, carefully
- Most of it
- I skimmed it
- Very little

## Section 6. Your assessment

**Grid, one answer per row (required). Scale: Strongly disagree, Somewhat disagree, Somewhat agree, Strongly agree.**
1. The piece was clear about what it claims.
2. Its claims were supported by evidence or sources.
3. It was clear what would show the thesis to be wrong.
4. It could have been written about almost any stock.
5. The bear case was a serious challenge, not a token one.
6. To show you are paying attention, please select "Somewhat disagree" for this row. *(attention check 1)*
7. I have never used the internet. *(attention check 2: the correct answers are "Strongly disagree" or "Somewhat disagree")*
8. The tone felt like selling a stock.

**L1.** The length of the piece was: (required)
- Too long
- About right
- Too short

**U1.** Which parts were most useful? Choose up to three.
- The one-sentence hypothesis
- Why now
- What the market may be missing
- The bull case
- The best bear case
- The valuation
- The dated catalysts
- The conditions that would prove it wrong
- The basket and its weights

## Section 7. In your own words

**O1.** What is the weakest assumption in this thesis? Please be specific. (long answer, required)

**O2.** What was confusing or missing? (long answer, optional)

**O3.** Did anything look factually wrong or unsupported? If so, which statement? (long answer, optional)

## Section 8. End of form

Thank you. Please click **Submit** first (answers are lost if you do not), then enter this code on Prolific to be paid: **[COMPLETION CODE from Prolific]**

## Build notes (Google Forms)

*Added 2026-10-13 from Prolific's Google Forms integration guide (researcher-help.prolific.com, article 445183) and Google Forms behaviour; the Google Forms points marked "not from Prolific" are not verified against Google's own help.*

**Google Forms sections (use the "Add section" button), in this order:**

1. About this study and consent (the consent question routes by answer).
2. Prolific ID.
3. S1 on its own section (routes by answer).
4. S2 on its own section (routes by answer). One routing question per section avoids ambiguity about which answer wins.
5. The reading and every remaining question: reading link, C1-C4, R1, the grid, L1, U1, O1-O3. At the bottom set "After section: go to" the end-of-form section.
6. "Does not consent" page: the thank-you line, then "After section: Submit form".
7. Screen-out page with the screen-out code, then "After section: Submit form".
8. End of form with the completion code (last section of the form).

Sections 6 and 7 sit between the main section and the end section on purpose: sections otherwise run in order, so the main section must jump over them to section 8.

**Settings.** Responses: email collection "Do not collect", also under Form defaults. No file-upload question. Do not turn on "Limit to 1 response" (not from Prolific: Google then requires sign-in; Prolific already prevents the same person doing a study twice). Make the form open to anyone with the link and test it in a private window.

**Question types.** Consent, S1, S2, C1-C4, R1, L1: multiple choice, required. Prolific ID: short answer, required. Grid: multiple-choice grid with "Require a response in each row" on and "Limit to one response per column" off. U1: checkboxes with response validation "Select at most 3". O1: paragraph, required; O2 and O3: paragraph, optional.

**Order of work, because the codes come from Prolific.** Build the form with the code placeholders and copy its link; create the Prolific draft with that link; copy the completion code and the "Screened out" code from the study setup; paste them into sections 7 and 8; test the form paths (consent No, S1 No, S2 "Never", and a full pass) with the preview; then publish the study. Study B is a separate Prolific study with its own codes.

**After publishing.** Responses tab: link to Sheets or download CSV. Match each Prolific submission to a form response by the Prolific ID; a typo in the ID is the usual cause of a missing match (compare start time and duration).
