---
name: grill-me
description: Replaces /idea-refine + /spec flow. Grills the user with focused questions, explores codebase, then writes context.md + spec.md (+ ADRs in Mode C). Trigger with /grill-me, /grill-me --mode=c, "grill me on X", or "let's spec out X".
version: 1.0.0
---

# Grill Me

Combines premise-challenging, divergent/convergent exploration, and relentless grilling into one skill. Outputs ready-to-consume docs for downstream agents.

**Mode B (default):** `context.md` + `spec.md`
**Mode C:** `context.md` + `spec.md` + ADR files

## Trigger

- `/grill-me` — Mode B
- `/grill-me --mode=c` — Mode C
- Natural language: "grill me on X", "let's spec out X", "discover X"

## Path Configuration

Read from `CLAUDE.md` under `## Skill Paths`:

```markdown
## Skill Paths
- context:       docs/context.md
- spec:          teams/{feature}/spec.md
- plan:          teams/{feature}/plan.md
- adr_dir:       docs/adr/
- changelog_dir: docs/changelogs/
```

`{feature}` is auto-slugged kebab-case from the user's initial prompt.

Defaults if section is missing:
- context → `docs/context.md`
- spec → `teams/{feature}/spec.md`
- plan → `teams/{feature}/plan.md` (consumed by `/implement`)
- adr_dir → `docs/adr/`
- changelog_dir → `docs/changelogs/` (consumed by `/implement`)

`/grill-me` only writes `context.md`, `spec.md`, and (in Mode C) ADR files. `plan.md` and changelogs are written later by `/implement`.

## Language

Mirror the user's language in all output — questions, docs, summaries. If the user writes in Indonesian, respond in Indonesian. Do not drift to English unless the user switches first.

---

## Phase 1 — Challenge Premise

Before anything else, challenge whether this is the right problem to solve.

Ask **at most 3 questions**. Stop if the user can't answer clearly — surface that as a blocker.

Good challenge questions:
- Why now? What changed that makes this worth doing?
- Who specifically has this problem, and how do you know?
- What's the simplest thing that could work instead?

If premise holds up, move to Phase 2. If it collapses, tell the user clearly and stop.

---

## Phase 2 — Explore Codebase First

Before asking the user anything, read what already exists:

1. Check `CLAUDE.md` / `AGENT.md` for project context and constraints
2. Check `README.md` for overview
3. Check for existing `context.md` or `spec.md` — if found, note what's already resolved
4. Grep for relevant symbols, routes, models, or config that relate to the feature

Do not ask the user about things the codebase already answers.

---

## Phase 3 — Grill

Ask **one question at a time**. Never batch questions.

Rules:
- Always include a **recommended answer** (with brief reasoning) after each question
- If a branch has 2+ viable options with real tradeoffs, run idea-refine sub-mode: list options, stress-test each, ask user to pick
- Cover all spec sections: objective, users, success criteria, tech constraints, scope boundaries, integration points, edge cases, "not doing"
- Ground every question in codebase findings from Phase 2

**Stop conditions** (pick first that applies):
- All sections resolved → proceed to Phase 5
- User says "enough" or "skip" → summarize what's unresolved, proceed to Phase 5
- 12-question cap hit → tell the user the scope may be too large, suggest splitting, then proceed to Phase 5

---

## Phase 4 — Hard Gate (No Inline Writing)

**Never write any files during Phase 1–3.**

Do not produce `context.md`, `spec.md`, or any ADR until Phase 5 begins.

If you feel the urge to "draft" or "preview" a doc inline during grilling — resist it. Writing before grilling ends causes the doc to be misused as a PRD before the user is ready.

---

## Phase 5 — Write Docs

Write files only after grilling is complete (or stop condition hit).

### context.md (≤ 80 lines)

Use `CONTEXT-TEMPLATE.md`. Hard cap: 80 lines. Cut ruthlessly. Every line must earn its place.

### spec.md (≤ 60 lines)

Use `SPEC-TEMPLATE.md`. Hard cap: 60 lines. No ASCII layouts. No visual mockups.

### ADR files (Mode C only, ≤ 25 lines each)

Use `ADR-TEMPLATE.md`. One file per key decision. Write only decisions where the "why" is non-obvious or reversing it would be costly.

Write files to paths from Phase 2 path config.

---

## Phase 6 — Hand Off

After writing, output exactly this structure:

```
Done. Wrote:
- [path/context.md]
- [path/spec.md]
(- [path/adr/NNN-title.md] if Mode C)

Unresolved: [list any skipped questions, or "none"]

Next: run /implement to generate plan.md and execute.
```

Do **not** auto-trigger `/implement` or any other skill.

---

## Anti-patterns

- Asking multiple questions at once
- Skipping premise challenge
- Writing docs before Phase 5
- Not recommending an answer per question
- Exceeding line caps
- Auto-chaining to the next skill
- Re-asking what the codebase already answers
- Switching language away from the user's language
