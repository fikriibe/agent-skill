# grill-me-spec

Digs into an idea with sharp, focused questions one at a time, explores the codebase, then writes `context.md` + `spec.md` ready for `/implement` to consume.

> For casual ideation or stress-testing a plan **without** producing files, use `anthropic-skills:grill-me` instead.

---

## Usage

| Command | Output |
|---|---|
| `/grill-me-spec` | `context.md` + `spec.md` |
| `/grill-me-spec --mode=c` | `context.md` + `spec.md` + ADR files |

Natural language also works: *"spec out X"*, *"let's spec out X"*.

---

## Output files

| File | Cap | Content |
|---|---|---|
| `context.md` | ≤ 80 lines | Domain knowledge — problem, users, constraints, scope, key decisions |
| `spec.md` | ≤ 60 lines | Work package — tech stack, structure, style, testing strategy |
| `docs/adr/NNN-title.md` | ≤ 25 lines | Non-obvious architecture decisions (Mode C only) |

---

## Flow (6 phases)

1. **Challenge premise** — max 3 questions, stop if the idea doesn't hold up
2. **Explore codebase first** — read `CLAUDE.md`, `README.md`, existing `context.md` before asking anything
3. **Grill** — one question per turn, always include a recommended answer
4. **Stop condition** — all sections resolved, user says "enough", or 12-question cap hit
5. **Write docs** — files are written only now, line caps enforced
6. **Hand off** — one-line summary + next step suggestion, no auto-trigger

---

## Path configuration in `CLAUDE.md`

Add this section to your project's `CLAUDE.md`. `{feature}` is auto-slugged from your initial prompt.

```markdown
## Skill Paths
- context:       docs/context.md
- spec:          teams/{feature}/spec.md
- adr_dir:       docs/adr/
```

**Defaults if section is missing:**

| Path | Default |
|---|---|
| `context.md` | `docs/context.md` |
| `spec.md` | `teams/{feature}/spec.md` |
| ADR files | `docs/adr/NNN-title.md` |

---

## Position in workflow

```
/grill-me → [review spec.md] → /implement → [review diff] → commit
```

No auto-chaining. Every transition is a deliberate user decision.

---

## Templates

| File | Used for |
|---|---|
| `CONTEXT-TEMPLATE.md` | Structure of `context.md` |
| `SPEC-TEMPLATE.md` | Structure of `spec.md` |
| `ADR-TEMPLATE.md` | Structure of ADR files (Mode C) |
