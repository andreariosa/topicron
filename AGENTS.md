# AGENTS.md

*How AI coding assistants — Claude Code, Cursor, or any other agentic tool — collaborate inside this repository. A process document, not a product document: what Topicron* is *lives in `docs/VISION.md`; what its AI pipeline* does *lives in `docs/AI_SYSTEM.md`; how Topicron gets built lives here. Sits below ADR-0001, ADR-0002, and ADR-0003 in the decision hierarchy (§2) — this file operationalizes those frozen decision records, it doesn't add to them.*

As of this writing the repository is pre-code (`README.md`, Status: Pre-build). Every rule below takes effect from M1's first scaffolding commit onward, and applies equally to a human-authored PR and an AI-authored one.

## 1. Two different "AI"s — do not conflate them

Topicron is unusual in that AI shows up in this repository in two structurally different roles, and the same tool — Claude Code, in the same terminal — can plausibly occupy either one in the same session.

| | AI as **product** | AI as **development tool** |
|---|---|---|
| What it does | Generates topics and theses — the real `synth/` and `thesis/` work in `docs/AI_SYSTEM.md` | Writes, reviews, and refactors the code Topicron runs on |
| Governed by | `docs/AI_SYSTEM.md`, `docs/DATA_MODEL.md`, ADR-0001 (D-12–D-16) | This file, `CLAUDE.md`, `CURSOR_RULES.md` |
| Output | A `topics` row, a `theses` row, `positions` — real data a reader will see | A diff, a migration, a test, a doc edit |
| Current executor (ADR-0002, D-20) | The founder, running the exact prompts in `AI_SYSTEM.md` via Claude Code / claude.ai | Also usually the founder, also often via Claude Code — same tool, different job |

**The failure mode this guards against:** an assistant scaffolding `jobs/synth/` decides to "generate a few example theses to test the schema with," and those examples end up indistinguishable, in a diff or a seed script, from real pipeline output. Anything generated for testing must be unambiguously marked as fixture data (a `tests/fixtures/` path, a flag production queries never read) and must never land in a table a public page renders from.

The reverse matters too: if an assistant is asked to actually *perform* a `synth/` or `thesis/` run, it's acting as Agent 2 or Agent 3 from `AI_SYSTEM.md`, not as a coding assistant, and should say so plainly — "this is a thesis-generation run, not a code change" — so a generation is never mistaken for reviewed, already-loaded output.

## 2. Decision hierarchy

When instructions conflict, higher wins, and the conflict gets surfaced, not silently resolved in either direction.

1. **ADR-0001, ADR-0002, and ADR-0003** — frozen. ADR-0002 governs execution mode; ADR-0003 governs thesis content structure; neither reopens ADR-0001's Parts I–V, and ADR-0003 doesn't reopen either prior ADR's scope or architecture decisions.
2. **`docs/*.md`** — implementation detail. If a doc and an ADR disagree, the ADR is right and the doc has a bug.
3. **`AGENTS.md`, `CLAUDE.md`, `CURSOR_RULES.md`** — process, consistent with 1 and 2.
4. **A single chat instruction or PR description** — the most local, most overridable layer. Fine for scoping one task; not a license to contradict 1–3 without first proposing the ADR change that would justify it (§9).

## 3. Roles

One human decision-maker (the founder), any number of AI contributors. No assistant:

- moves its own ADR proposal from `Proposed` to `Accepted` (`DECISIONS.md`),
- merges its own PR without founder review,
- decides, on its own initiative, that a deferred item's reinstatement trigger has fired — even when it correctly spots that the condition looks met, firing the trigger is a founder call (§6, §11).

## 4. Ownership boundaries

| Area | Free to edit | Needs sign-off for |
|---|---|---|
| `jobs/ingest`, `jobs/extract` (rule-based path), `jobs/prices`, `jobs/perf`, `jobs/digest` | Implementation, refactors, tests — fully automated, zero-LLM-cost jobs | Changing their GitHub Actions cadence, which is a documented product decision (`docs/ARCHITECTURE.md`), not a free variable |
| `jobs/synth`, `jobs/thesis` (prompts + manual-loading scripts) | Refining prompt text against the contracts in `docs/AI_SYSTEM.md`; the script that loads founder-reviewed output into Supabase | Wiring either into a scheduled job calling the Claude API directly — that specific change *is* ADR-0002's D-24 reinstatement (§6) |
| `jobs/extract`'s LLM fallback | Leaving it deferred, as designed | Re-enabling it — same D-24 gate |
| Frontend | Building and editing freely | A login wall, a personalized view, or any user-specific state ahead of M5 (D-07) |
| Database migrations | Implementing anything already specified in `docs/DATA_MODEL.md` | Anything in the Deferred-entities appendix (`portfolios.user_id`, `thesis_citations`, a real `sources` table, any sentiment/momentum table) without confirming its trigger fired |
| `docs/*.md`, `README.md` | Edits for accuracy, clarity, or to reflect an already-accepted ADR | Changing a stated decision, gate, or scope boundary — that's an ADR amendment (§9), not a doc fix |
| ADR files | Drafting a new one as `Proposed` | Marking any ADR `Accepted`, `Superseded`, or `Rejected` |
| Cost-cap / kill-switch code | Implementing and testing it now, dormant or not | Skipping it "because nothing calls the API yet" — it has to exist before D-24 fires, not get written under pressure after |

## 5. Repository invariants

Hold regardless of milestone:

1. **No LLM call in a request path, ever** (`docs/ARCHITECTURE.md`).
2. **Every performance figure derives from `price_snapshots` and the fixed 90-day holding rule** — never a backtest, never a discretionary exit (ADR-0001, D-13).
3. **Every thesis claim carries a paraphrased citation with a source id; no verbatim source text is stored or displayed** (ADR-0001, D-15).
4. **Every generation logs `model_used` and `prompt_version`** — by hand during free-tier-first, automatically once D-24 fires.
5. **A daily spend cap is enforced in code, not just alerted on**, even while dormant (ADR-0001, D-16; ADR-0002, D-24).
6. **The repository stays public.** GitHub Actions' free, uncapped scheduled-job minutes hold specifically because the repo is public (`docs/TECH_STACK.md`, ADR-0002 D-21); going private silently reintroduces a cost this project has deliberately avoided.
7. **`ANTHROPIC_API_KEY` stays unset** anywhere Claude Code runs for this project. Its presence silently switches Claude Code from the Pro subscription to metered billing — precisely the new recurring cost ADR-0002 exists to prevent.

## 6. When to stop and ask

- **Money.** Anything adding a new metered or subscription service beyond Cursor + Claude Pro (D-19). "It's only $13/month" *is* the D-24 question — firing it is the founder's call, explicitly, even when the assistant thinks the condition is met.
- **Schema reintroduction.** Any field or table ADR-0001 D-05 cut, or anything under `docs/DATA_MODEL.md`'s Deferred entities.
- **Milestone sequencing.** Building ahead of a stated gate (`docs/ROADMAP.md`) — dashboard work before M5's retention threshold, auth before user-specific state exists.
- **Regulatory-adjacent copy.** The `caveat` field, `suggested_basket`'s equal-weighting, any language describing what Topicron promises. This touches the publisher's-exclusion posture in `docs/RISKS.md`; not a place for a confident rewrite.
- **The Reddit question, in any form.** Even a "quick script to check subreddit activity" gets checked against the scraping boundary in `docs/MVP_SCOPE.md` first (ADR-0001, D-10).

## 7. When to refuse

Refuse here means: decline to implement via an ordinary chat request, and point at §9 instead — the founder can still change any of these, but only by writing (or directing) the ADR that would justify it, not by a one-line ask.

- **An LLM call inside a request path.** Breaks invariant 1, no exceptions.
- **Scraping Reddit, or any source whose terms prohibit it**, as a workaround for cost or rate limits.
- **Real trade execution or brokerage integration**, in any form.
- **A personalized or conviction-weighted `suggested_basket`.** Stays naive equal-weight — a legal boundary, not a placeholder (`docs/RISKS.md`).
- **Verbatim source text in a citation.** Paraphrase plus source id, never a quoted excerpt (ADR-0001, D-15).
- **A published backtest or historical performance figure**, under any framing, including "just for the demo" (ADR-0001, D-02).
- **An LLM grading another LLM's thesis for accuracy.** The only judge is `perf/` against real market data (`docs/AI_SYSTEM.md`, Evaluation engine).

## 8. Keeping documentation and code in sync

A PR changing a load-bearing invariant, a schema table, a milestone deliverable, or a deferred item's status isn't done until the matching line in `docs/*.md` changes in the *same* PR. "Docs after" is exactly how the seven-tables-plus-two-joins count in `docs/ARCHITECTURE.md` quietly stops being true. `docs/DECISIONS.md` and `PROJECT_STATE.md` are the two documents most likely to go stale first — check both before closing out milestone-level work.

## 9. Introducing architectural change

Nothing in ADR-0001, ADR-0002, or ADR-0003 changes by editing prose in `docs/`. It changes by a new, numbered ADR:

1. Draft `docs/ADR/ADR-000N-kebab-title.md`, continuing the sequence (next is ADR-0004), with the header block ADR-0001/0002/0003 already establish: `Status`, `Date`, `Context`, `Decision owners`, `Relationship to prior ADRs`.
2. State the criticism or trigger being responded to, the verdict, the reasoning, the MVP impact, and the exact docs that need to change — the format existing ADRs already use.
3. Status starts `Proposed`. An assistant may draft it; only the founder moves it to `Accepted`.
4. Once accepted, apply the listed documentation changes in the same batch of work, not as a follow-up — an accepted ADR whose docs haven't caught up is a tracked, temporary state (`PROJECT_STATE.md`), not a resting one.

Full lifecycle and naming convention: `DECISIONS.md`.

## 10. Quality bar

The project's stated existential risk is generic output, not a bug (`docs/RISKS.md`). A schema-valid, well-tested thesis generator that produces bland, hedge-everything prose hasn't met the bar, and no code quality compensates for that. Two mechanisms exist specifically to catch this, and neither gets skipped for feeling slow:

- The golden-set regression check (`docs/AI_SYSTEM.md`), run by hand before any prompt change during free-tier-first.
- Weekly manual QA sampling against the grounded / non-generic / correctly-cited rubric.

Everywhere else — jobs, schema, frontend — normal engineering quality applies: small functions, explicit code over clever code, and business logic that's actually tested. The 90-day exit-date math and the momentum query deserve the most test attention of anything in the codebase, since they're the arithmetic the entire accountability claim rests on.

## 11. MVP boundaries

`docs/MVP_SCOPE.md` is canonical — this is a pointer, so it can't drift out of sync with it.

- **In scope** → that doc's "In scope" table.
- **Deferred** → that doc's "Deferred" table, with a written trigger. Believe a trigger fired? Say so and ask (§6) — don't build ahead of confirmation.
- **Explicitly out** → not trigger-gated at all. Building these needs a new ADR, not a milestone passing.

Doesn't obviously map to one of the three? That's the signal to ask, not to assume "probably fine, it's small."

## 12. Free-tier-first philosophy

Per ADR-0002: nothing gets added that introduces a new recurring, metered, or subscription cost beyond Cursor and Claude Pro, for as long as Topicron is pre-revenue. This is a bright line, not a budget — small and free are different categories here, not points on the same scale. The one accepted exception is the annual domain registration (D-22). Everything else in `docs/TECH_STACK.md` already clears the bar on a genuine, indefinite free tier; a new tool gets checked against this rule first, not against whether it's a good tool.

## 13. Engineering principles, translated into code-level defaults

- **Defer with a trigger, not a wish.** "We'll need this eventually" doesn't justify building it now; a fired trigger does.
- **Boring and defensible beats clever and unfalsifiable** — said of the holding-period rule, and a good default everywhere else too.
- **Only claim what arithmetic can defend.** Every number a reader sees traces to cached data and a pre-committed rule.
- **Polyglot, not multi-service.** Python for jobs, TypeScript for the frontend, is a language choice, not a standing-service choice (D-04) — don't reintroduce a deployed backend to solve what a scheduled job or a Supabase RPC already solves.
- **Quality is the gate; code is not.** A build-week estimate says nothing about how long a quality gate takes to pass.

## 14. Worked examples

**"Add Slack notifications when a new thesis publishes."**
Not in `docs/MVP_SCOPE.md` either way; free, no invariant touched. Check the cadence implication before building it, though: a real-time ping per thesis reads as reactive rather than the fixed weekly cadence the publisher's-exclusion posture depends on. Ask whether this belongs pre-M3 at all, and if so, whether it should batch to the weekly cadence rather than fire per-thesis.

**"Add live/streaming quotes so the dashboard feels less static."**
Refuse and explain: pulls M5's dashboard ahead of its own retention gate, and free-tier Finnhub is explicitly delayed data that should never be presented as real-time.

**"Just call the Claude API directly from a GitHub Action for thesis generation — it's cheap, let's stop doing this by hand."**
Stop and ask. This is ADR-0002's D-24 decision by another name. "The founder decides the cost is worth it" is a legitimate trigger — but it needs to be an explicit yes, not an assumption that convenience is reason enough.

**"Add a `user_id` to `positions` so we're ready for user portfolios later."**
Refuse: exactly the field ADR-0001 D-05 cut, gated on a trigger (M6, validated retention, a personalization-risk review) that hasn't fired. Building it "to be ready" is the overengineering ADR-0001 exists to stop.

**"Store the full RSS article body next to the citation for more context."**
Refuse: citations are a paraphrase plus a source id, never source body text (ADR-0001, D-15). If more context is genuinely needed at generation time, pass the fuller text into the prompt — just don't persist or render it.

**"Today's synth/ run produced two topics that are obviously the same narrative."**
Not a bug to quietly patch — it's the named highest-uncertainty risk in the pipeline (ADR-0001, D-12). Apply the merge rule as written (older topic canonical, newer archived with a note) and flag the occurrence rather than treating it as one-off cleanup; repeated fragmentation is the signal that the `pgvector` escalation is due.

## 15. Related process documentation

This file is the policy layer; the rest defer to it rather than re-stating it:

| File | Covers |
|---|---|
| `CLAUDE.md` | Persistent context for Claude Code specifically — project philosophy, and how it should reason before changing code |
| `CURSOR_RULES.md` | Strict, enforceable coding rules for Cursor — conventions, project layout, explicit dos/don'ts |
| `DECISIONS.md` | The ADR index, lifecycle, and naming convention referenced in §9 |
| `CONTRIBUTING.md` | The actual development workflow — branching, commits, PRs, releases |
| `PROJECT_STATE.md` | Current phase, active milestone, implemented ADRs, known debt — the live status reference this file assumes is kept current (§8) |
