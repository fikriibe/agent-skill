---
name: glossary
description: Scans a codebase and generates GLOSSARY.md — a Ubiquitous Language document mapping domain terms to canonical names, definitions, API paths, and interface contracts. Works on legacy codebases. Trigger with /glossary, /glossary --update, or /glossary --term="X".
version: 1.0.0
---

# Glossary

Generates and maintains `GLOSSARY.md` — a Ubiquitous Language document (Domain-Driven Design) for any codebase. Primary consumer: agents (Claude) reading canonical names and interface contracts when generating code. Secondary: human devs aligning on shared terminology.

Works on legacy codebases with no prior `spec.md` or `context.md`.

## Trigger

- `/glossary` — scan codebase from scratch, generate new `GLOSSARY.md`
- `/glossary --update` — re-scan, add new terms, flag outdated ones
- `/glossary --term="X"` — add or update a single term without full re-scan

## Language

Mirror the user's language in all output and questions.

---

## Entry Structure

Each term in `GLOSSARY.md` follows this format:

```markdown
## Task

- **definition:** Unit kerja yang bisa di-assign ke user dan memiliki status lifecycle.
- **code name:** `Task` (bukan `Todo`, bukan `Item`)
- **api:** `GET /api/v1/tasks`, `POST /api/v1/tasks`, `PATCH /api/v1/tasks/:id`
- **interface:**
  ```typescript
  interface Task {
    id: TaskId;
    title: string;
    status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
    assigneeId: UserId | null;
    completedAt: Date | null;
    createdAt: Date;
    updatedAt: Date;
  }
  ```
```

Field rules:
- `definition` — plain language, domain meaning. Required. Must be confirmed by user.
- `code name` — canonical name used in code. If aliases found (e.g. `Todo`, `Item`), declare which is correct and note alternatives.
- `api` — relevant HTTP endpoints. Omit if term has no API surface.
- `interface` — TypeScript interface or equivalent. Omit if term is not a data structure.

---

## `/glossary` — Fresh Scan

### Step 1: Scan codebase

Extract candidate terms from:
- TypeScript interfaces, types, and enums in `types.ts`, `models.ts`, `schema.ts`, `*.d.ts`
- Prisma schema or ORM model definitions
- Database migration files (table names → domain concepts)
- API route handlers — extract route paths and request/response type names
- Directory names under `src/features/`, `src/domain/`, `src/modules/`, `src/entities/` or equivalent
- Exported class names from service/repository files

### Step 2: Deduplicate and rank

- Group aliases referring to the same concept (`Todo`, `Item`, `Task` → one candidate)
- Rank candidates by frequency of reference across codebase
- Exclude purely technical/infra terms (e.g. `Logger`, `Config`, `Middleware`) unless they appear in API contracts

### Step 3: Confirm one by one

For each candidate, present to user:

```
Found: Task (also seen as: Todo, Item)

Proposed entry:
  code name: Task
  api: GET /api/v1/tasks, POST /api/v1/tasks, PATCH /api/v1/tasks/:id
  interface: { id: TaskId, title: string, status: TaskStatus, assigneeId: UserId | null, completedAt: Date | null }

What does "Task" mean in your domain?
(Type a definition, or press Enter to skip this term)
```

- User provides definition → entry confirmed, queued
- User presses Enter / types nothing → skip, not added to GLOSSARY
- User corrects `code name` → use corrected name in entry
- User corrects interface → use corrected interface

Do not proceed to next term until current one is resolved.

### Step 4: Write GLOSSARY.md

- Sort entries alphabetically by term name
- Overwrite file if it already exists
- Header:

```markdown
# Glossary

Ubiquitous Language for this codebase. Canonical names, definitions, and interface contracts.
Agents: load this file as context before generating code to use correct names and types.

_Last updated: {date}_

---
```

### Step 5: Declare path in CLAUDE.md

Check if `CLAUDE.md` exists in project root. If yes, check if it already has a `## Project Context` section with `glossary:` key.

If missing, append:

```markdown
## Project Context
- glossary: GLOSSARY.md
```

If section exists but `glossary:` key is missing, add the key under the existing section.

If CLAUDE.md does not exist, create it with only the `## Project Context` block.

---

## `/glossary --update`

1. Read existing `GLOSSARY.md` — extract current term names.
2. Re-scan codebase (same as Step 1 above).
3. **New terms:** terms found in codebase but not yet in GLOSSARY → confirm one by one (same flow as Step 3).
4. **Outdated terms:** terms in GLOSSARY whose extracted interface no longer matches codebase → append `⚠️ possibly outdated` to the term's heading:
   ```markdown
   ## Task ⚠️ possibly outdated
   ```
   Do not auto-delete or auto-update definitions — flag only.
5. Write updated `GLOSSARY.md`. Preserve all existing definitions verbatim.

---

## `/glossary --term="X"`

1. Search codebase for `X` — find its interface definition, API routes, and any aliases.
2. Present proposed entry to user (same format as Step 3).
3. User confirms definition.
4. If `X` already exists in `GLOSSARY.md` → update the entry in-place.
5. If `X` is new → append to `GLOSSARY.md` in correct alphabetical position.

---

## Integration with Other Skills

- **`/grill-me-spec`:** If `GLOSSARY.md` exists (check CLAUDE.md for path), load it as context before grilling. If it does not exist, suggest running `/glossary` first.
- **`/implement` subagents:** Load `GLOSSARY.md` when spawning `fe`, `be`, `qa` subagents so they use canonical names in generated code.

---

## Anti-patterns

- Auto-generating definitions without user confirmation — definitions must reflect domain meaning, not code structure
- Adding purely technical/infra terms (Logger, Config, HttpClient) unless they appear in domain contracts
- Overwriting user-edited definitions on `--update`
- Flagging every term as outdated when interface changes slightly (only flag structural breaks, not field additions)
- Creating one giant glossary for all microservices — scope to current project root

---

## Done When

- [ ] `GLOSSARY.md` exists in project root
- [ ] Every entry has a user-confirmed `definition`
- [ ] `code name` is canonical — no ambiguity with aliases
- [ ] `CLAUDE.md` declares `glossary: GLOSSARY.md` under `## Project Context`
- [ ] `/glossary --update` runs without overwriting existing definitions
- [ ] `/glossary --term="X"` adds a single term correctly
