<!--
Claude Code loads this file automatically at the start of every session
(code.claude.com/docs/en/memory). Claude Code reads CLAUDE.md, not
AGENTS.md -- so this file opens with an @AGENTS.md import, Anthropic's
documented pattern for sharing one policy file across multiple agentic
tools without duplicating it. Everything below the import is Claude-
Code-specific: project philosophy and how to reason before touching
code. Keep this file itself lean -- Anthropic's own guidance targets
well under 200 lines per CLAUDE.md file for good adherence, and an
imported file still loads in full, so don't re-explain what AGENTS.md
already covers. This comment is stripped before injection into
context, so it costs nothing per session -- edit it freely.
-->

@AGENTS.md

## Claude Code — Topicron

Everything above this line is `AGENTS.md`, imported in full: the enforceable policy — ownership boundaries, invariants, the ask/refuse lists, the ADR process. This section doesn't repeat any of it. It's the reasoning behind the policy, so a rule reads as a decision made for a reason, not an arbitrary constraint.

### Vision, in one paragraph

Topicron is a research publication with a database behind it: it discovers investment narratives, publishes a structured bull case / bear case / named-risks thesis on a fixed weekly cadence, and tracks — publicly, including the losers — whether each thesis's hypothetical portfolio actually beat the market over a fixed 90-day hold. It is not a stock picker, not a signal service, and not a dashboard. Full version: `docs/VISION.md`.

### Product philosophy

Five things from `docs/VISION.md` that should shape how you weigh a change, not just what you build:

1. **Time-dependent assets get built now; everything else waits.** Price history, positions, the email list compound with elapsed time regardless of code quality — they don't wait for the "right" milestone to feel worth building.
2. **Quality is the gate; code is not.** A generic, hedge-everything thesis is a failure even if it's schema-valid, type-checked, and fully tested.
3. **Publish on schedule, in public, unedited.** Losing theses get the same visual and update treatment as winning ones — always, no exceptions worth writing code for.
4. **Only claim what arithmetic can defend.** Every number a reader sees traces to `price_snapshots` and the pre-committed holding rule — never a backtest, never one model grading another's output.
5. **Defer with a trigger, not a wish.** A deferred feature has a written condition. "We'll want this eventually" doesn't move it into scope; a fired trigger does.

### Engineering philosophy

Polyglot (Python for jobs, TypeScript for the frontend), not multi-service — there's no deployed backend, and there isn't going to be one unless `AGENTS.md` §9's ADR process says otherwise. Full carried-over list: `AGENTS.md` §13.

### Coding philosophy: maintainability and simplicity over cleverness

This is a solo founder's codebase. Every abstraction you add is a tax paid by exactly one person, indefinitely — so the boring option is the default, every time:

- **Duplication beats the wrong abstraction.** Don't unify `jobs/ingest` and `jobs/prices` behind a shared "job runner" base class just because they're both scheduled scripts — they're two scripts until a third one shows the actual shared shape.
- **No framework where a function will do.** The AI pipeline in `docs/AI_SYSTEM.md` is a linear sequence of typed calls on purpose — ADR-0001 rejected LangGraph/CrewAI/AutoGen for exactly this reason. Don't reintroduce that complexity one layer down, in application code.
- **One entrypoint per job.** `jobs/ingest`, `extract`, `prices`, `synth`, `thesis`, `perf`, and `digest` are each a script with a clear start and end, not a class hierarchy or a plugin system.
- **Reach for what's already in `docs/TECH_STACK.md`** before adding a new package for one function's worth of convenience.
- **Write the migration today's `docs/DATA_MODEL.md` actually needs.** Don't add a column, index, or table "while you're in there" for something that isn't built yet.
- **A comment should explain *why*, not *what*.** A market-calendar edge case or a regulatory constraint deserves a comment; a restatement of the code below it doesn't. If code needs the second kind of comment, rewrite the code instead.

### Architectural constraints

The shape is frozen by ADR-0001 Part 3 and ADR-0002: Next.js on Vercel, Supabase (Postgres + unused auth), GitHub Actions for every scheduled job, no deployed backend service. Full detail: `docs/ARCHITECTURE.md`, `docs/TECH_STACK.md`. In practice: never suggest FastAPI, Railway, Celery, or a standalone vector DB as "the right way to do this" — each has a named reinstatement trigger, and none of them have fired.

### MVP boundaries and anti-goals

Boundaries: `docs/MVP_SCOPE.md` is canonical; `AGENTS.md` §11 has the short version.

Anti-goals are the shape of what Topicron has decided *not* to be, and matter as much as what's in scope:

- **Not a signal service.** No real-time alert, no "buy now," nothing engineered to reward the reader who wants a shortcut instead of the argument.
- **Not a personalized advisor.** `suggested_basket` is naive equal-weight, applied identically to every reader — a legal line (`docs/RISKS.md`), not a placeholder for smarter allocation later.
- **Not a broker.** No real trades, ever, in this repository.
- **Not a dashboard, yet.** The publication is the MVP; the interactive layer is real but gated on a retention signal that doesn't exist yet (M5).
- **Not built on Reddit, yet.** Curated RSS proves the pipeline first; Reddit is a licensing-and-revenue decision, not an engineering one.

If a task would make Topicron friendlier to the anti-persona — the signal-seeker (`docs/VISION.md`) — at the expense of the informed generalist, say so out loud rather than just building it.

### Free-tier-first, specifically for this tool

Claude Code is, confusingly, both roles in `AGENTS.md` §1 at once on this project: the coding assistant *and*, per ADR-0002 D-20, the current executor of `synth/` and `thesis/`. Two things follow directly:

- Never let `ANTHROPIC_API_KEY` end up set in this project's environment, a `.env` file, or a CI secret, even for "just testing" — it silently moves Claude Code off the Pro subscription and onto metered billing (`AGENTS.md` §5, invariant 7).
- The instinct to automate away a manual step — wiring `synth/`/`thesis/` into a scheduled job, re-enabling the Haiku extraction fallback — is exactly `AGENTS.md` §6's "stop and ask," not a productivity win to just ship.

### Documentation rules

A change to a schema table, an invariant, a milestone deliverable, or a deferred item's status isn't complete until the matching line in `docs/*.md` changes in the same commit (`AGENTS.md` §8). Not sure a doc needs to change? Check `docs/DATA_MODEL.md`, `docs/ROADMAP.md`, and `docs/MVP_SCOPE.md` first — they're the three most likely to describe whatever you just touched.

### Development workflow

Full workflow: `CONTRIBUTING.md`. Day to day: small, milestone-scoped commits; docs updated alongside code, not after; nothing merges without the founder's review, including changes you're confident about.

### How to reason before changing code

Run this before writing or editing anything — not only when a change feels risky:

1. **What milestone is this?** Check `PROJECT_STATE.md` (once it exists) or `docs/ROADMAP.md`.
2. **Where does it sit in `docs/MVP_SCOPE.md`** — in scope, deferred-with-a-trigger, or explicitly out? If explicitly out, stop before writing code, not after.
3. **Does it touch a repository invariant** (`AGENTS.md` §5)? If yes, that's a fixed constraint to design around, not a trade-off to weigh against convenience.
4. **Is there a version sized for today** — one topic, one thesis, a few dozen readers — rather than the version you'd build if this already had the traffic M5 is gated on?
5. **Does a doc need to change alongside this code?** If yes, do it in the same edit.
6. **Still uncertain after 1–5?** Say specifically what's uncertain, and ask. A wrong guess delivered confidently is worse than a question.

### Instructions vs. enforcement

This file and `AGENTS.md` are context, not enforcement — Claude Code treats them that way, and can pick an arbitrary side if two loaded instructions conflict. For anything in `AGENTS.md` §5 or §7 that must never happen regardless of what gets decided mid-session — an LLM call in a request path, a committed `ANTHROPIC_API_KEY` — the durable fix, once there's a CI pipeline to put it in, is a real check (a grep-based lint rule, a pre-commit hook, a CI step) that fails the build, not another line of prose asking nicely. Until that CI exists, read this file as strictly as if it were one.

### Auto memory vs. this file

Claude Code's own auto-memory (build commands, debugging patterns it notices) is useful and separate from this file — leave it alone. If something auto-memory captures turns out to be an actual project decision rather than a workflow convenience, it doesn't get to live only there: promote it into this file, or into a new ADR if it changes scope or architecture (`AGENTS.md` §9). Auto-memory is scratch space; `CLAUDE.md`, `AGENTS.md`, and the ADRs are the record.
