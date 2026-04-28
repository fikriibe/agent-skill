---
name: incremental-implementation
description: Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Skip for single-file, single-function changes with obvious scope.
version: 1.1.0
---

# Incremental Implementation

## The Cycle — repeat per slice

```
Implement → Test → Verify → Commit → next slice
```

Never accumulate more than ~100 lines before running tests.

---

## Slicing Strategies

**Vertical (preferred)** — one complete working path per slice:
```
Slice 1: Create task (DB + API + UI) → user can create
Slice 2: List tasks (query + API + UI) → user can see
Slice 3: Edit task → user can modify
Slice 4: Delete task → full CRUD done
```

**Contract-first** — when BE and FE develop in parallel:
```
Slice 0: Define API contract (types + OpenAPI)
Slice 1a: Backend against contract + API tests
Slice 1b: Frontend against mock matching contract
Slice 2: Integrate end-to-end
```

**Risk-first** — tackle the most uncertain piece first. If it fails, you know before investing in the rest.

---

## Rules

**Simplicity first** — ask "what's the simplest thing that could work?" Three similar lines > premature abstraction. Implement the naive correct version, optimize after tests prove it works.

**Scope discipline** — touch only what the task requires. If you notice something worth fixing outside scope, note it, don't fix it:
```
NOTICED BUT NOT TOUCHING:
- src/utils/format.ts has unused import
→ Want me to create a task for this?
```

**One thing per increment** — don't mix feature + refactor + config in one commit.

**Always compilable** — build and existing tests must pass after every slice.

**Feature flags** for incomplete work that needs to merge:
```typescript
const ENABLE_TASK_SHARING = process.env.FEATURE_TASK_SHARING === 'true';
```

**Rollback-friendly** — additive changes first, deletions separate from replacements.

---

## Directing an Agent

Be explicit about scope per increment:
```
"Implement Task 3: only the DB schema + API endpoint.
Don't touch the UI yet.
After implementing, run `npm test` and `npm run build`."
```

---

## Red Flags
- 100+ lines written without running tests
- Multiple unrelated changes in one increment
- "Let me just quickly add this too"
- Build or tests broken between slices
- Large uncommitted changes accumulating
- Abstractions built before the third use case

## Done When
- [ ] Each slice individually tested + committed
- [ ] Full test suite passes
- [ ] Build clean
- [ ] Feature works end-to-end as specified
- [ ] No uncommitted changes remain