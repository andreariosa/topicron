# CURSOR_RULES.md

*How Cursor's Agent works inside this repository, and how this document itself is meant to be used — read §1 before anything else, since it changes how the rest of the file functions.*

## 1. How this actually loads in Cursor

Cursor already reads `AGENTS.md` automatically — at the project root and in any subdirectory, with a more specific nested `AGENTS.md` taking precedence over a parent one (Cursor's own documentation confirms this). That means the policy layer — decision hierarchy, ownership boundaries, repository invariants, the ask/refuse lists, the ADR process — is already loaded into every Cursor session with nothing from this file. Nothing below repeats it. (This is separate from Cursor's personal, cross-project "User Rules" in Settings → Rules — those aren't version-controlled and aren't what this document is about.)

What Cursor does *not* load automatically is a plain file named `CURSOR_RULES.md`. Cursor's real mechanism for scoped, always-on engineering rules is a directory: `.cursor/rules/*.mdc`, each file carrying its own YAML frontmatter (`description`, `globs`, `alwaysApply`). This document is written so each numbered section below can become one `.mdc` file with almost no editing — the heading names the intended filename and activation mode. §7 has the literal directory layout and one fully worked example. Until that split happens, this is the correct, readable content; it just isn't live inside Cursor yet.

## 2. Non-negotiables → `general.mdc` (`alwaysApply: true`)

- **Never violate ADR-0001 or ADR-0002.** Both are frozen (`AGENTS.md` §2). If a task seems to require it, that's a signal the task needs a new ADR, not a workaround.
- **Never modify the architecture — deployed services, schema shape, job cadence, the frozen tech stack — without first drafting a new ADR.** Implement inside the current shape, or stop and draft `docs/ADR/ADR-000N-*.md` (`AGENTS.md` §9). Don't do both at once and call it a compromise.
- **Never add a dependency, service, or tool without a one-line justification in the PR description**, and never one that introduces a new recurring cost beyond Cursor + Claude Pro (`docs/TECH_STACK.md`; ADR-0002, D-19).
- **Never implement a feature that isn't in `docs/MVP_SCOPE.md`'s "In scope" table.** A deferred item needs its written trigger to have fired; an explicitly-out item needs a new ADR. Neither needs "it's small" or "while I'm in here."
- **Never optimize prematurely.** This project has zero users. A caching layer, a queue, a "for scale" refactor, or a generalized plugin interface solves a problem that doesn't exist yet — build the version sized for one topic and a few dozen readers.
- **Never leave `docs/*.md` behind a code change that affects an invariant, a schema table, a milestone deliverable, or a deferred item's status.** Same commit, not a follow-up (`AGENTS.md` §8).
- **Stop and ask, don't guess, when uncertainty is genuinely high.** The concrete trigger list — money, schema reintroduction, milestone sequencing, regulatory-adjacent copy, anything Reddit-shaped — is `AGENTS.md` §6. A wrong guess delivered confidently costs more than a question.

## 3. Coding conventions — Python (`jobs/**/*.py`) → `python-jobs.mdc` (`globs: jobs/**/*.py`)

- Type hints on every function signature — this is a small codebase maintained by one person, and types are cheaper than the bugs they'd otherwise cost.
- One clear entrypoint per job (`jobs/ingest`, `extract`, `prices`, `synth`, `thesis`, `perf`, `digest`) — a `main()` a scheduler can call, not a class hierarchy.
- Raise on failure; don't swallow an exception to keep a job "green." A job that fails loudly once is cheaper than one that silently drops data for a month.
- A docstring explains *why* a function exists or names a non-obvious edge case (market-calendar handling, a ticker-collision workaround) — not what the code already says plainly.
- Reach for the standard library and the dependencies already named in `docs/TECH_STACK.md` before adding a new package for one function's worth of convenience.
- Lint/format: `ruff` covers both and is the standard modern choice at this project's size — pick it and move on; it's not worth more deliberation than this sentence (`docs/TECH_STACK.md` treats comparable low-stakes picks, like Resend vs. Postmark, the same way).

## 4. Coding conventions — TypeScript / Next.js (`app/**/*.{ts,tsx}`) → `frontend.mdc` (`globs: app/**/*.{ts,tsx}`)

- Server components by default (App Router); reach for a client component only when the interactivity genuinely requires it.
- Tailwind + shadcn/ui, per `docs/ARCHITECTURE.md` — no second component library "just for this one screen."
- Data fetching reads Postgres through the Supabase client with row-level security, per the frozen architecture (`docs/ARCHITECTURE.md`). There is no backend service to call instead, and suggesting one is out of scope without an ADR (`AGENTS.md` §9).
- No `any`. A type that's genuinely hard to express is a signal to simplify the function, not to escape-hatch around it.
- No LLM call anywhere in this directory, client- or server-side, that a page load would wait on. This is repository invariant 1 (`AGENTS.md` §5) and it applies here without exception.

## 5. Testable business logic → `testing.mdc`

Three things in this codebase are the arithmetic the entire accountability claim rests on, and deserve tests before almost anything else does:

- **The 90-day holding rule's exit-date math** (`docs/DATA_MODEL.md`) — including the weekend/holiday roll-forward. Write the market-calendar edge cases as explicit test cases, not just the happy path.
- **The momentum query** (trailing 48h mention count vs. a trailing baseline, `docs/AI_SYSTEM.md`) — it's read-time computed and stored nowhere, which makes a silent regression here invisible until someone notices a topic never crosses the momentum threshold.
- **The portfolio return calculation** (`Σ(weight × price_now / price_entry) − 1`, `docs/ARCHITECTURE.md`) — simple arithmetic, and simple arithmetic is exactly the kind of thing that's easy to get subtly wrong once and never notice.

Test runner: `pytest` for the Python jobs, `Vitest` or `Jest` for the frontend — pick one the first time a test is actually needed, and don't spend longer on the choice than it takes to read this sentence.

## 6. Project organization

```
topicron/
├── AGENTS.md, CLAUDE.md, CURSOR_RULES.md, CONTRIBUTING.md,
│   PROJECT_STATE.md, DECISIONS.md, README.md
├── docs/
│   ├── ADR/ADR-0001-...md, ADR-0002-...md, ADR-000N-...md
│   └── VISION.md, MVP_SCOPE.md, ARCHITECTURE.md, TECH_STACK.md,
│       DATA_MODEL.md, AI_SYSTEM.md, ROADMAP.md, RISKS.md
├── jobs/
│   ├── ingest/  extract/  prices/  perf/  digest/   (fully automated)
│   └── synth/   thesis/                              (founder-run prompts + loader script — ADR-0002, D-20)
├── app/                     Next.js App Router frontend
├── supabase/
│   └── migrations/          sensible default given Supabase is already the Postgres provider — no separate ORM/migration tool unless a real need appears
└── .github/workflows/       CI, plus the scheduled jobs' cron triggers
```

New code goes where this tree already implies it goes. If a file doesn't obviously belong anywhere here, that's a signal to ask before creating a new top-level directory — a new directory is a structural decision, and `AGENTS.md` §6 applies to structure as much as to features.

Not every technical choice above needs an ADR. Picking `ruff` or `pytest` is an implementation detail — cheap to change, and not what `AGENTS.md` §9 means by "architectural change." An ADR is for anything touching scope, cost, data flow, or the frozen shape in `docs/ARCHITECTURE.md` / `docs/TECH_STACK.md` — not for a linter.

## 7. Wiring this into Cursor

To make sections 2–5 actually load into every session, rather than sitting as a reference document, split them into:

```
.cursor/
└── rules/
    ├── general.mdc        alwaysApply: true          (section 2)
    ├── python-jobs.mdc     globs: jobs/**/*.py         (section 3)
    ├── frontend.mdc        globs: app/**/*.{ts,tsx}    (section 4)
    └── testing.mdc         description-based           (section 5)
```

One fully worked example — `general.mdc`, ready to save as-is:

```markdown
---
description: Topicron non-negotiables
alwaysApply: true
---

# Non-negotiables

- Never violate ADR-0001 or ADR-0002. Both are frozen (AGENTS.md §2).
- Never modify architecture (services, schema shape, job cadence, stack)
  without first drafting a new ADR (AGENTS.md §9).
- Never add a dependency or service without a one-line justification, and
  never one with a new recurring cost beyond Cursor + Claude Pro (ADR-0002).
- Never implement a feature outside docs/MVP_SCOPE.md's in-scope table.
- Never optimize prematurely — this project has zero users.
- Never leave docs/*.md behind a code change that affects an invariant,
  a schema table, a milestone deliverable, or a deferred item's status.
- Stop and ask, don't guess, when uncertainty is genuinely high
  (AGENTS.md §6: money, schema reintroduction, sequencing, regulatory
  copy, anything Reddit-shaped).
```

The other three sections convert the same way: drop the code fence, add frontmatter with the `globs` noted in its heading, save under the filename the heading names.
