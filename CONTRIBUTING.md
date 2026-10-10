# CONTRIBUTING.md

*The development workflow for this repository — optimized for exactly what this project actually is: one developer, heavily assisted by Claude Code and Cursor, building toward the milestones in `docs/ROADMAP.md`. Not a multi-contributor open-source process; "external contributor" isn't a real concept here yet, even on a public repo — if that ever changes, this document is the first thing to revisit, not the last. Applies from M1's first scaffolding commit onward, same as `AGENTS.md` and `CLAUDE.md` — except §11 (Claude Project sync), which applies now.*

## 1. Branching strategy

`main` is always deployable and protected — no direct pushes, PRs only, and that applies to the founder too. The point isn't hierarchy, it's guaranteeing every change gets a reviewable diff and a CI run before it lands. Enable GitHub branch protection on `main`: require the CI check, require a pull request, disallow force-push.

Work happens on short-lived branches off `main`, named for what they contain, not for a role: `m1-rss-ingestion`, `m2-topic-continuity`, `adr-0003-governance-layer` — a milestone or ADR prefix where one applies, a short description otherwise. No `develop`, no `release/*`, no `hotfix/*`: those solve a multi-contributor coordination problem this project doesn't have, and a permanent parallel branch is exactly the kind of complexity this project's overengineering isn't (`docs/VISION.md`, MVP philosophy).

Merge with squash — one commit per PR on `main`'s history, regardless of how many small commits happened on the branch while iterating with an assistant.

Why bother with branches and PRs at all for one contributor? Three reasons specific to this project, not branching dogma:

1. **A PR is a diff you actually read before it lands**, and that matters more, not less, when a large share of its lines were written by an assistant instead of typed by hand.
2. **CI needs something to gate.** Lint, type-check, and tests on every push (`docs/ARCHITECTURE.md`) are only a real gate if they run *before* a merge, not as a status light on `main` after the fact.
3. **A branch is a natural unit for a milestone-scoped chunk of work** (`docs/ROADMAP.md`'s build-weeks), which keeps `main`'s history readable as "here's M1," not an undifferentiated stream of commits.

## 2. Commit message conventions

A short, standard prefix — `feat`, `fix`, `docs`, `test`, `chore`, `refactor` — with a scope in parentheses where it adds information: `feat(jobs/ingest)`, `docs(data-model)`.

What's specific to this repo: **cite the milestone and, where one exists, the decision** in the commit body — not ceremony, but so "why does this function exist" is answerable from `git blame` six months from now without reconstructing the conversation that produced it.

```
feat(jobs/prices): add weekend/holiday roll-forward for exit dates

M1. Implements the market-calendar handling docs/DATA_MODEL.md's
90-day holding rule requires (docs/RISKS.md, Market calendar handling).
```

```
docs(data-model): apply ADR-0001 D-05 schema cuts

Removes SentimentSnapshot, removes Portfolio.user_id, collapses both
status enums. ADR-0001, D-05.
```

A commit that touches an invariant, a schema table, or a scope boundary with no milestone or decision reference in its body is a signal the change wasn't checked against `AGENTS.md` first — not just a style miss.

## 3. Pull request checklist

Before merging:

- [ ] The PR title or description names the milestone (`M0`–`M6`) or ADR it belongs to.
- [ ] `docs/*.md` is updated in the same PR if this touches an invariant, a schema table, a milestone deliverable, or a deferred item's status (`AGENTS.md` §8) — not filed as a follow-up.
- [ ] No repository invariant is violated (`AGENTS.md` §5) — in particular: no LLM call added to a request path, no new recurring cost, and `ANTHROPIC_API_KEY` doesn't appear anywhere in the diff.
- [ ] If this touches scope or architecture, there's a linked ADR — at minimum `Proposed`, not just a decision made in chat and never written down.
- [ ] Tests exist for any arithmetic-critical logic touched (`CURSOR_RULES.md` §5).
- [ ] CI is green: lint, type-check, tests.
- [ ] If the diff is AI-generated: the founder has actually read it — see §9, not just skimmed the changed-file list.

## 4. Issue workflow

GitHub Issues, used lightly — for anything that needs to outlive a single sitting or hand off cleanly to a future session, not as mandatory process for its own sake. Skip an issue for something you're doing right now in one sitting; open one for:

- A known bug or regression not being fixed immediately, so it's tracked rather than just remembered.
- A quality-gate finding worth a paper trail — a golden-set failure, a topic-fragmentation incident (`docs/AI_SYSTEM.md`, Topic continuity), a manual-QA rubric miss.
- A clean handoff to a future Claude Code or Cursor session — an issue with full context is a better starting point than reconstructing it from memory.
- A deferred item worth checking on — "has ADR-0002 D-24's trigger fired yet" is a perfectly good issue to leave open and revisit.

Suggested labels, matched to this project's own vocabulary rather than generic defaults: `milestone:M0`…`milestone:M6`, `adr`, `deferred-trigger`, `quality-gate`, `founder-review-needed`.

## 5. Testing expectations

Required, before merge:

- Tests for the arithmetic-critical logic named in `CURSOR_RULES.md` §5 (the 90-day exit-date math, the momentum query, the portfolio return calculation) — including the market-calendar edge cases, not just the happy path.
- A regression test alongside any bug fix, so the same bug can't silently come back.

Not required, at this stage:

- Exhaustive coverage of ingestion parsing, frontend components, or anything else with zero users depending on it yet — the same "never optimize prematurely" instinct (`CURSOR_RULES.md` §2), applied to test suites instead of code.

Separately, and not a substitute for the above: the **golden-set regression check** (`docs/AI_SYSTEM.md`) runs by hand, before any prompt change to `synth/` or `thesis/`, for as long as free-tier-first holds (ADR-0002). It isn't a unit test and doesn't live in CI — it's a manual workflow step, and skipping it because a prompt tweak "looks small" is exactly the failure mode it exists to catch.

## 6. Documentation expectations

Already the law, not a suggestion (`AGENTS.md` §8): a PR touching an invariant, a schema table, a milestone deliverable, or a deferred item's status includes the matching `docs/*.md` edit in the same PR. §3's checklist is where this actually gets enforced in practice — if it isn't checked there, it didn't happen.

## 7. Release process

There isn't a traditional release process yet, and forcing one onto a project with no package consumers and no version-pinned API would be process for its own sake. What actually happens:

- **Vercel deploys `main` continuously.** Every merge is a release of the frontend; there's no separate "cut a release" step.
- **The scheduled jobs run on whatever's on `main`** at their next scheduled trigger — no versioned job artifact to publish either.
- **A lightweight git tag at each milestone boundary** (`m1-complete`, `m2-complete`, …) is worth doing purely for historical reference and easy rollback — not a SemVer scheme, not release notes, not a changelog generator.

Revisit this the moment any of that stops being true — a public API someone else builds against, a package published for others to install, or real users who need to know what changed and when. None of those exist yet.

## 8. Milestone workflow

A milestone starts once the previous one's gate has passed, per `docs/ROADMAP.md` — and a gate is usually a judgment call by the founder (or the target-persona readers, at M0), not a CI check, since the project's stated existential risk is generic output, not a wiring bug (`docs/RISKS.md`).

Within a milestone: branches and PRs are scoped to its deliverables (`docs/ROADMAP.md`'s table), not to arbitrary chunks of time. When a milestone's gate is evaluated and passes, update `PROJECT_STATE.md` to reflect the transition — the active milestone, what's now implemented, and the next one's starting point — in the same sitting the gate passes, not as a later cleanup pass.

A gate that doesn't pass is not a missed estimate — `docs/ROADMAP.md` is explicit that a quality gate is allowed to stop or reroute the project. Treat a failed gate as a real finding worth an issue (§4) and a `PROJECT_STATE.md` update of its own, not a thing to quietly retry until it looks like it passed.

## 9. Reviewing AI-generated code

This is about code — `jobs/`, the frontend, migrations — written by Claude Code or Cursor. It's a different concern from reviewing *thesis and topic output*, which has its own process already (`docs/AI_SYSTEM.md`'s golden-set check and weekly manual QA); don't conflate the two, the way `AGENTS.md` §1 warns against.

The specific thing to guard against: an assistant's own narration of what it did and the actual diff can diverge, especially on the things this repository cares about most — an invariant, a dependency, a scope boundary. A confident explanation is not evidence the explanation is accurate. Concretely, before merging:

- **Read the diff, not the summary.** The assistant's description of a change is a starting point for review, not a substitute for it.
- **Grep for the specific danger signals** before merging anything touching `jobs/` or the frontend: any reference to `ANTHROPIC_API_KEY`; any LLM call reachable from a route handler or page render; any new import not already named in `docs/TECH_STACK.md`.
- **If the change touches something `AGENTS.md` §6 lists as "stop and ask" and the assistant didn't ask** — that's a specific signal to slow down, not a "well, it's already done" shrug.
- **For a large AI-authored diff, review it in chunks** (per file, per logical piece) rather than approving one big diff in a single pass — the odds of a real, subtle violation rise with diff size, and an assistant can produce a large diff faster than a fast review can responsibly happen.
- **A second, fresh Claude Code or Cursor session reviewing the first session's diff is a legitimate, cheap extra check** — a session that wrote itself into a design choice can rationalize it; a fresh one reading the diff cold often won't. This augments the founder's review; it never replaces it. No assistant merges its own PR, and no assistant reviewing a diff gets to be the final approval either (`AGENTS.md` §3).

## 10. Definition of done

"Done" is not the same thing as "merged," and for anything touching the AI pipeline specifically, it's not the same thing as "code-complete" either — `docs/VISION.md`'s MVP philosophy #2 (quality is the gate, code is not) governs how work gets closed out, not just what gets built.

**For an application-code change:**
- Merged to `main`, CI green.
- `docs/*.md` updated wherever `AGENTS.md` §8 requires it.
- Tests exist for any arithmetic-critical logic touched (`CURSOR_RULES.md` §5).

**For pipeline output — a topic, a thesis:**
- Code-complete is not done. It's done once it's passed the golden-set check and/or the weekly manual QA rubric (`docs/AI_SYSTEM.md`) — a schema-valid, well-cited thesis that reads generic hasn't met the bar, no matter how clean the code that produced it is.

**For a milestone task:**
- All of the above, plus `PROJECT_STATE.md` reflects it (§8).

**For any change that lands on `main`:**
- The Claude Project has been re-synced from GitHub (§11) — a commit the Claude Project hasn't seen is only half-landed.

## 11. Claude Project sync

*Unlike the rest of this file, this section applies now, during M0 — documentation commits are already landing on `main`; it doesn't wait for M1's first scaffolding commit.*

Architecture and review work happens in a Claude Project on claude.ai, attached to this repository through its GitHub sync source: `andreariosa/topicron`, branch `main`, whole repository (`/`) included. The rule this section exists to state:

**GitHub `main` is the single source of truth for every project file. The Claude Project holds a copy of it, refreshed by hand.**

### After every commit pushed to `main`

1. Push the commit.
2. In the Claude Project, run the sync on the GitHub source (project knowledge panel). It is not automatic — a commit stays invisible to Claude until this step happens.
3. Before the next Claude session that depends on the change, check that it landed: `PROJECT_STATE.md`'s "Last updated" line, as Claude sees it, should match the commit you just made.

Skipping this fails quietly: Claude reasons from the previous version — an old `PROJECT_STATE.md`, an ADR before its amendment — and sounds exactly as confident as it would on the current one.

### What lives where

| Place | Holds | How it changes |
|---|---|---|
| GitHub `main` | Every project file: `docs/`, ADRs, process files, `m0/`, code | Commit and push |
| Claude Project → synced GitHub source | A copy of the above — never edited directly | Manual sync after each commit |
| Claude Project → Instructions | A short, stable standing prompt (text below). Not synced from GitHub | Change the text in this file first, commit, then paste it into the Project's settings |
| Claude Project → uploaded docs | Nothing. Never upload copies of repo files — they go stale silently and compete with the synced version | — |

Anything worth keeping — a decision, a finding, a revised file — gets committed. If it exists only in a Claude chat or an uploaded document, it isn't project state (same principle as `CLAUDE.md`'s auto-memory note).

### Detecting a stale copy

- `PROJECT_STATE.md`'s "Last updated" line is the freshness marker: if the copy Claude has loaded lags the commit you just made, the sync hasn't run or hasn't finished.
- Claude is instructed (Instructions below; `AGENTS.md` §15) to say so and ask for a re-sync, not to guess. Limit of this check: a commit that doesn't touch `PROJECT_STATE.md` doesn't move the marker. When in doubt, re-sync — it's cheap.
- Claude Code and Cursor read the checkout directly and don't need the sync. Their commits still make the Claude Project stale, and neither can run the sync (it's a UI action), so Claude Code ends its commit reports with a reminder (`CLAUDE.md`).

### Project Instructions (canonical text)

Kept here so it has history and a single editing point. Paste it into the Claude Project's Instructions field; re-paste only when this block changes.

```
Act as my technical co-founder and senior software architect.
Help me design and build Topicron, an AI-powered investment research laboratory.
Project repo: https://github.com/andreariosa/topicron

Source of truth
- GitHub, branch main, is the single source of truth for every project file. The
  Project's GitHub source is a copy that I re-sync by hand after each commit
  (CONTRIBUTING.md section 11), so it can be stale.
- Do not treat uploaded Project docs as canonical.
- Start from PROJECT_STATE.md (where the project is now), then AGENTS.md section 2
  (decision hierarchy). ADR-0001, ADR-0002 and ADR-0003 are frozen: they change
  only through a new numbered ADR, never by editing prose. PROJECT_STATE.md is a
  fast summary, not a source of truth.
- If a loaded file contradicts what I say I just committed, or PROJECT_STATE.md's
  "Last updated" lags my latest commit, tell me and ask for a re-sync before relying
  on it. Do not guess which version is right.

Prioritize:
- pragmatic MVP decisions
- scalable architecture
- avoiding overengineering
- strong product thinking
- measurable user value

Challenge my assumptions when needed, and flag judgment calls explicitly.

Working rules
- Reply in my language (Italian by default); write documents and code in English.
- Verify against the actual files or a real test instead of answering from memory.
- Free-tier-first (ADR-0002): propose no new recurring cost without my explicit yes.
- When you change documents, give me the complete updated files plus a commit
  message that cites the milestone and decision (CONTRIBUTING.md section 2). I commit
  and push myself, then re-sync.
- Never ask me to paste secrets or API keys into the chat.
```
