---
name: spec-driven-development
description: Creates specs before coding. Use when starting a new project, feature, or significant change. Use when requirements are unclear, ambiguous, or only a vague idea. Skip for single-line fixes or unambiguous changes.
version: 1.1.0
---

# Spec-Driven Development

## Gated Workflow — don't advance without human approval at each gate

```
SPECIFY → PLAN → TASKS → IMPLEMENT
   ↓        ↓      ↓        ↓
 human    human  human    human
```

---

### Phase 1: Specify

**Before writing anything**, surface assumptions explicitly:
```
ASSUMPTIONS I'M MAKING:
1. [assumption]
2. [assumption]
→ Correct me now or I'll proceed with these.
```

Then write the spec covering these 6 areas:

```markdown
# Spec: [Name]

## Objective
[What, why, who. Acceptance criteria or user stories.]

## Tech Stack
[Framework, language, key deps + versions]

## Commands
[Full executable commands — build, test, lint, dev]

## Project Structure
[Directory layout with one-line descriptions]

## Code Style
[One real code snippet + key naming/formatting conventions]

## Testing Strategy
[Framework, test locations, coverage expectations, test levels]

## Boundaries
- Always: [run tests before commit, follow naming, validate inputs]
- Ask first: [schema changes, new deps, CI config]
- Never: [commit secrets, edit vendor dirs, remove failing tests]

## Success Criteria
[Specific, testable conditions — not vague goals]

## Open Questions
[Unresolved items needing human input]
```

> Reframe vague requirements as testable success criteria:
> "Make it faster" → "LCP < 2.5s on 4G, initial load < 500ms, CLS < 0.1"

---

### Phase 2: Plan
- Map major components + dependencies
- Define implementation order (what must come first)
- Note risks + mitigations
- Identify parallel vs. sequential work
- Set verification checkpoints between phases

---

### Phase 3: Tasks

Each task:
```markdown
- [ ] Task: [Description]
  - Acceptance: [What must be true when done]
  - Verify: [test command / build / manual check]
  - Files: [files touched]
```
Rules: completable in one session · max ~5 files · ordered by dependency

---

### Phase 4: Implement
Execute tasks one at a time. Update spec when decisions or scope change — the spec lives in version control alongside the code.

---

## Output Flags

Setelah spec selesai dan di-approve, evaluasi:

```
needs_design_phase:  boolean
  true jika:
  - jumlah UI screens baru >= 3
  - spec menyebut "design system", "redesign", atau "visual"
  - greenfield project dengan UI-heavy features

design_complexity:  low | medium | high
  low    → 1-2 screens sederhana, komponen standar
  medium → 3-5 screens, custom komponen
  high   → 6+ screens, design system baru, animasi kompleks
```

Route ke `/design-pipeline` jika `needs_design_phase: true`.

---

## Red Flags
- Writing code before any written requirements
- Making architectural decisions without documenting them
- "I'll write the spec after" — that's documentation, not specification
- Implementing features not in any spec or task list

## Done When
- [ ] All 6 spec areas covered
- [ ] Human reviewed + approved the spec
- [ ] Success criteria are specific and testable
- [ ] Boundaries defined
- [ ] Spec saved to the repo