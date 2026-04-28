---
name: git-workflow-and-versioning
description: Structures git workflow. Use when making any code change — committing, branching, or organizing parallel work. Use always.
---

# Git Workflow and Versioning

## Core Principles

**Trunk-based development** — keep `main` always deployable. Short-lived feature branches (1–3 days max). Feature flags > long-lived branches.

**Commit = save point** — commit every successful increment. Never accumulate large uncommitted changes.

**Atomic commits** — one logical thing per commit:
```
✅ git log:
a1b2c3 feat: add task creation endpoint with validation
d4e5f6 feat: add task creation form component
h7i8j9 feat: connect form to API with loading state

❌ git log:
x1y2z3 add task feature, fix sidebar, update deps, refactor utils
```

**Separate concerns** — never mix formatting + behavior + refactor in one commit. Each is its own commit.

---

## Commit Message Format

```
<type>: <short description>

<optional body — explain WHY, not what>
```

Types: `feat` · `fix` · `refactor` · `test` · `docs` · `chore`

```
✅ feat: add email validation to registration endpoint

Prevents invalid email formats from reaching the database.
Uses Zod schema, consistent with existing patterns in auth.ts.

❌ update auth.ts
```

---

## Branching

```
main (always deployable)
  ├── feature/task-creation    ← merge within 1-3 days
  ├── fix/duplicate-tasks
  └── chore/update-deps
```

Naming: `feature/` · `fix/` · `refactor/` · `chore/` + short description. Delete after merge.

---

## Change Summary Pattern

After any change, emit a summary before committing:

```
CHANGES MADE:
- src/routes/tasks.ts: added Zod validation to POST endpoint
- src/lib/validation.ts: added TaskCreateSchema

NOT TOUCHED (intentionally):
- src/routes/auth.ts: has similar gap but out of scope

POTENTIAL CONCERNS:
- Zod schema rejects extra fields — confirm this is desired
```

The "NOT TOUCHED" section proves scope discipline. Flag concerns before they become bugs.

---

## Pre-Commit Checklist

```bash
git diff --staged           # review what you're committing
npm test                    # tests pass
npm run lint                # no lint errors
npx tsc --noEmit            # no type errors
# grep for secrets manually or use a hook
```

Automate with `husky` + `lint-staged` for lint/format on staged files.

---

## Git for Debugging

```bash
# Find which commit introduced a bug
git bisect start && git bisect bad HEAD && git bisect good <sha>

# What changed recently
git log --oneline -20
git diff HEAD~5..HEAD -- src/

# Who last changed a line
git blame src/services/task.ts
```

---

## .gitignore Essentials

Always have one. Must cover: `node_modules/` · `dist/` · `.next/` · `.env` · `.env.local` · `*.pem`

---

## Red Flags
- Large uncommitted changes accumulating
- Commit messages: "fix", "update", "misc"
- Formatting mixed with behavior changes
- No `.gitignore`
- Committing `node_modules/`, `.env`, or build artifacts
- Long-lived branches diverging from main
- Force-pushing to shared branches

## Done When (per commit)
- [ ] Commit does one logical thing
- [ ] Message explains the why, uses type convention
- [ ] Tests pass before committing
- [ ] No secrets in the diff
- [ ] No formatting-only changes mixed with behavior changes