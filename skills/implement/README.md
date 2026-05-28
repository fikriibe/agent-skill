# implement

Execution skill for after `/grill-me-spec`. Replaces `/plan` + `/feature-team`.

Reads `spec.md`, generates `plan.md`, then dispatches role subagents in topological waves. Each wave is automatically verified by the `verifier` subagent before the next wave runs.

---

## Usage

| Command | Behavior |
|---|---|
| `/implement` | Generate `plan.md` + execute immediately |
| `/implement --review` | Generate `plan.md`, pause — review/edit first, then `/implement --resume` |
| `/implement --resume` | Skip generation, execute existing `plan.md` |
| `/implement --cleanup` | Delete `teams/{feature}/` folder after completion |
| `/implement --model=<name>` | Override model for all subagents for this run |

---

## Flow

```
spec.md
   ↓
Generate plan.md
   ↓
[--review: pause here] → /implement --resume to continue
   ↓
Wave 1: spawn fe/be tasks in parallel
   ↓
verifier: pnpm test → PASS → continue / FAIL → halt + ask user
   ↓
Wave 2: (tasks whose Depends are all [x])
   ↓
... (repeat until all dev tasks done)
   ↓
Wave QA: spawn qa subagent
   ↓
verifier: full suite
   ↓
Wave Docs: spawn docs subagent
   ↓
Done — review diff, commit manually
```

---

## Subagents

Five subagents are auto-installed to `.claude/agents/` on first run. Existing files are never overwritten.

| Role | Model | Responsibility |
|---|---|---|
| `fe` | sonnet | UI, components, client state — TDD intrinsic |
| `be` | sonnet | API, DB, server logic — TDD intrinsic |
| `qa` | sonnet | Integration tests + edge cases |
| `docs` | haiku | Changelog + README updates |
| `verifier` | haiku | Run test suite, report pass/fail — always-on |

`verifier` is not an explicit role — it runs automatically after every dev/qa wave. No config needed.

Override per-role model by editing `.claude/agents/{role}.md` in your project.

---

## Task format in `plan.md`

```markdown
- [ ] [BE-1] Short title
  Acceptance: testable statement — what must be true
  Verify: pnpm test src/api/auth.test.ts
  Files: src/api/auth.ts, src/api/auth.test.ts
  Depends:
  Interface: (if this task exposes an API used by other tasks — define signature here)

- [ ] [FE-1] Short title
  Acceptance: ...
  Verify: ...
  Files: src/components/Login.tsx, src/components/Login.test.tsx
  Depends: BE-1
```

---

## Path configuration in `CLAUDE.md`

```markdown
## Skill Paths
- context:       docs/context.md
- spec:          teams/{feature}/spec.md
- plan:          teams/{feature}/plan.md
- changelog_dir: docs/changelogs/
```

**Defaults if section is missing:**

| Path | Default |
|---|---|
| `plan.md` | `teams/{feature}/plan.md` |
| Changelogs | `docs/changelogs/` |

---

## Design principles

Based on [Software Fundamentals Matter More Than Ever — Matt Pocock](https://www.youtube.com/watch?v=v4F1gFy-hqg):

- **Strategic control at the lead** — lead (Opus) holds orchestration, subagents (Sonnet/Haiku) handle tactics
- **TDD intrinsic** — every dev task must write a failing test first, then implementation
- **Deep modules** — 5 orthogonal roles, simple interface (task block), implementation delegated
- **Ubiquitous language** — task IDs (`BE-1`, `FE-1`) are the shared language between roles
- **Halt on fail** — verifier fail → halt + ask user, no auto-retry, no auto-fix

---

## Templates

| File | Used for |
|---|---|
| `PLAN-TEMPLATE.md` | Structure of `plan.md` |
| `~/agents/fe.md` | Frontend subagent definition |
| `~/agents/be.md` | Backend subagent definition |
| `~/agents/qa.md` | QA subagent definition |
| `~/agents/docs.md` | Docs subagent definition |
| `~/agents/verifier.md` | Verifier subagent definition |
