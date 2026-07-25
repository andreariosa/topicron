# DECISIONS.md

*The complete index, lifecycle, and naming convention for every Architecture Decision Record in this repository. `AGENTS.md` §9 has the short version — draft, get founder sign-off, apply the listed documentation changes in the same batch; this file is the fuller reference that pointer assumes exists.*

## 1. Index of ADRs

| ID | Title | Status | Purpose | Affected documents |
|---|---|---|---|---|
| **ADR-0001** | MVP scope, architecture, and sequencing | `Accepted` | Adjudicates a skeptical-CTO review of the original plan; sets the frozen scope, architecture shape, schema shape, and milestone sequencing that everything else in this repository implements | `README.md`, `docs/VISION.md`\*, `docs/ARCHITECTURE.md`, `docs/TECH_STACK.md`\*, `docs/DATA_MODEL.md`, `docs/AI_SYSTEM.md`, `docs/ROADMAP.md`, `docs/MVP_SCOPE.md`\*, `docs/RISKS.md` |
| **ADR-0002** | Free-tier-first MVP | `Accepted` | Constrains *how* ADR-0001's plan gets implemented while Topicron is pre-revenue — no component may add a recurring cost beyond the founder's existing Cursor + Claude Pro subscriptions | `docs/AI_SYSTEM.md`, `docs/ARCHITECTURE.md`, `docs/TECH_STACK.md`, `docs/MVP_SCOPE.md`, `README.md`, `docs/RISKS.md` |

\* `docs/VISION.md`, `docs/TECH_STACK.md`, and `docs/MVP_SCOPE.md` postdate ADR-0001's own Part 5 table, which names six documents, not nine — these three were split out from `README.md` / `ARCHITECTURE.md` during implementation, and each states in its own header which ADR-0001 part it implements. A reasonable editorial split, not a deviation from the decision itself; it's just why this column lists the actual current document set rather than transcribing ADR-0001's table verbatim.

**Next ID:** ADR-0003 (continuing the shared decision registry at **D-25** — see §3).

Individual decisions inside an ADR (`D-01` through `D-24`, and onward) are indexed at the end of their own ADR — ADR-0001's "Summary of verdicts" table and ADR-0002's "Summary of decisions" table are the canonical per-decision index. This file indexes ADRs, not the decisions inside them, so there's exactly one place each list lives.

Both ADRs were confirmed `Accepted` by the founder on 2026-07-25, closing a brief gap where their headers read `Proposed` despite every other document already implementing them as settled.

## 2. When a new ADR is required

Required for anything that touches:

- **Product scope** — adding to, or removing from, `docs/MVP_SCOPE.md`'s in-scope, deferred, or explicitly-out lists, other than a deferred item's own trigger firing exactly as written (see below).
- **The frozen architecture** — a new deployed service, a new dependency with a recurring cost, a schema table or field ADR-0001 explicitly cut or deferred (`docs/DATA_MODEL.md`, Deferred entities).
- **A milestone gate** — changing what has to be true to pass M0–M6, or their sequencing (`docs/ROADMAP.md`).
- **An existing decision** — overriding, reversing, or superseding anything already Accepted.

Not required for:

- **Implementation details with no scope, cost, or architecture implication** — a linter, a test runner, a migration-folder name (`CURSOR_RULES.md` §6 draws this line explicitly, for exactly this reason).
- **A deferred item's trigger firing exactly as already written.** The decision was already made, conditionally, in the ADR that deferred it — reinstating it needs a founder confirmation that the trigger genuinely fired (`AGENTS.md` §3, §6) and the corresponding doc updates (`docs/MVP_SCOPE.md`, `docs/TECH_STACK.md`, `PROJECT_STATE.md`), not a new ADR re-arguing a case that was already made. If ADR-0002's D-24 trigger fires, for instance, that's a status change to track in `PROJECT_STATE.md`, not a reason to draft ADR-0003.
- **Prose clarification, typo fixes, or reorganizing existing content** that doesn't change what was decided.

## 3. Naming convention

- **File:** `docs/ADR/ADR-000N-kebab-case-title.md` — four-digit, zero-padded, sequential, matching `ADR-0001-mvp-scope-and-architecture.md` and `ADR-0002-free-tier-first-mvp.md` exactly. Numbers are never reused or renumbered, even once an ADR is Superseded or Rejected.
- **Decisions:** cited as **"ADR-000N, D-XX."** `D-XX` is **one continuous registry shared across every ADR**, not reset per file — ADR-0001 runs `D-01`–`D-18`; ADR-0002 continues the same sequence at `D-19`–`D-24` (ADR-0002 says so explicitly), so the next ADR's first decision is `D-25`, not `D-01`. Always cite the ADR number and the decision number together — `D-19` lives in ADR-0002, not ADR-0001, and the two aren't interchangeable shorthand for each other.

## 4. Lifecycle of an ADR

1. **Proposed** — drafted (by the founder, or by an AI assistant per `AGENTS.md` §9), not yet binding.
2. **Accepted** — the founder has explicitly said so; never inferred, and never self-granted by whichever assistant drafted it (`AGENTS.md` §3). The documentation changes the ADR itself lists get applied in the same batch of work as acceptance, not filed as a follow-up (`AGENTS.md` §9).
3. **Superseded by ADR-000N** — a later ADR explicitly reverses or replaces an earlier decision. The old ADR stays in `docs/ADR/`, unedited except its `Status` line — its original reasoning stays readable, since understanding why something used to be true is often exactly what stops the same debate from happening twice, uninformed.
4. **Rejected** — proposed, considered, declined. Stays in `docs/ADR/` too, for the same reason as Superseded: the reasoning behind a "no" is worth as much as the reasoning behind a "yes," and it's what stops a declined idea from quietly resurfacing months later as if it were new.

Don't confuse an ADR's own **Status** (its lifecycle state, above — one value per document) with a **verdict** on an individual decision *inside* one (`ACCEPT` / `PARTIALLY ACCEPT` / `REJECT`, the per-item rating ADR-0001 gives each of its eighteen responses to the original review). ADR-0001 is `Proposed`-or-`Accepted` as a whole document; `D-05` inside it is separately verdicted `PARTIALLY ACCEPT`. A future ADR responding to a list of criticisms the way ADR-0001 does can reuse that pattern; a future ADR making one clean decision, the way ADR-0002 mostly does, doesn't need it.

## 5. Relationship between ADRs and documentation

Every ADR ends with an explicit list of which `docs/*.md` files change, and how — not a suggestion, the actual mechanism that keeps the rest of the documentation set truthful (`AGENTS.md` §8). For example, ADR-0001's `D-05` names exactly what `docs/DATA_MODEL.md` needed: remove `SentimentSnapshot`, remove `Portfolio.user_id`, collapse both status enums, keep the exit and versioning fields with a one-line justification for each. `docs/DATA_MODEL.md` as currently written already reflects all of it — so `D-05` isn't just Accepted, it's Accepted *and* reflected, and those are different, separately trackable things.

A decision can be Accepted without yet being reflected in the docs it names — that's a real, temporary, legitimate state, not a contradiction to paper over. `PROJECT_STATE.md` is where that gap gets tracked live, if one ever opens up; this file documents the rule that governs it, not a point-in-time snapshot of where things currently stand.

## 6. Template for a new ADR

For a single, clean decision — the shape ADR-0002 uses:

```markdown
# ADR-000N — <title>

**Status:** Proposed
**Date:** <YYYY-MM-DD>
**Context:** <what prompted this — a constraint, a trigger firing, a new problem>
**Decision owners:** founder + technical co-founder
**Relationship to prior ADRs:** <does it reopen anything? reinstate a deferred item? extend without contradicting?>

## Decision

**Decision:** <one or two sentences>

**Why:** <the reasoning>

**Impact:** <what changes in scope, architecture, or process>

**Documentation change:** <exact files, exact edits>
```

For an ADR responding to a list of external criticisms — the shape ADR-0001 uses: give each item its own `### D-XX — <short name>` block with `**Criticism:**`, `**Verdict:**` (`ACCEPT` / `PARTIALLY ACCEPT` / `REJECT`), `**Why:**`, `**Impact:**`, `**Documentation change:**`, and close with a summary table of every verdict.
