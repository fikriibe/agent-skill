---
name: code-simplification
description: Simplifies existing code for clarity without changing behavior. Use when refactoring code that works but is hard to read, maintain, or extend. Not for new code generation.
version: 1.1.0
---

# Code Simplification

## Before Touching Anything
Understand why the code exists first (Chesterton's Fence):
- What does it do? What calls it? What edge cases exist?
- Check git blame — was there a reason for this complexity?
- If you can't answer these, read more context before proceeding.

## Simplification Signals

**Structure:**
| Pattern | Fix |
|---|---|
| Nested 3+ levels deep | Extract guard clauses or helper functions |
| Function 50+ lines | Split into focused, named functions |
| Nested ternaries | Replace with if/else or lookup object |
| Boolean flag params `fn(true, false)` | Use options object or separate functions |
| Same `if` check in multiple places | Extract to named predicate |

**Naming:**
| Pattern | Fix |
|---|---|
| Generic names: `data`, `result`, `temp` | Rename to describe content: `userProfile`, `validationErrors` |
| Comments explaining *what*: `// increment counter` | Delete — code is clear enough |
| Comments explaining *why*: `// API is flaky under load` | Keep — carries intent code can't express |

**Redundancy:**
| Pattern | Fix |
|---|---|
| Same 5+ lines in multiple places | Extract to shared function |
| Dead code, commented-out blocks | Remove after confirming truly dead |
| Wrapper that adds no value | Inline it |

## Process
1. **One change at a time** — run tests after each
2. **Refactoring PR ≠ feature PR** — never mix them
3. **Verify after**: is it genuinely easier to read? does the diff look clean?
4. **Scope strictly** — don't touch unrelated code unless explicitly asked

> Rule of 500: if change touches 500+ lines, use codemods/AST tools instead of manual edits.

## Never
- Modify tests to make simplification pass (you changed behavior)
- Remove error handling to "clean up"
- Simplify code you don't fully understand
- Rename to match your preferences over project conventions

## Done When
- [ ] All existing tests pass without modification
- [ ] Build + lint clean, no new warnings
- [ ] No unrelated changes in the diff
- [ ] Follows project conventions (CLAUDE.md)
- [ ] A teammate would approve this as a net improvement