---
name: implement
description: Generates plan.md from spec.md, then orchestrates role-based subagents (fe, be, qa, docs) in topological waves to execute it. Replaces /plan + /feature-team. Trigger with /implement, /implement --review, /implement --resume, /implement --cleanup.
version: 1.0.0
---

# Implement

Merged planning + execution skill. Lead session reads `spec.md`, generates `plan.md`, then dispatches role subagents to execute it in topological waves with per-wave test verification.

Aligned with Matt Pocock's *"Software Fundamentals Matter More Than Ever"* — lead holds strategic control, subagents are tactical executors.

## Trigger

- `/implement` — generate plan + execute immediately (default)
- `/implement --review` — generate plan, halt, wait for manual review → user runs `/implement --resume` to execute
- `/implement --resume` — skip plan generation, execute existing `plan.md`
- `/implement --cleanup` — after completion, delete `teams/{feature}/` folder

## Path Configuration

Read from `CLAUDE.md` under `## Skill Paths`:

```markdown
## Skill Paths
- context:       docs/context.md
- spec:          teams/{feature}/spec.md
- plan:          teams/{feature}/plan.md
- changelog_dir: docs/changelogs/
```

Defaults if missing:
- plan → `teams/{feature}/plan.md`
- changelog_dir → `docs/changelogs/`

`{feature}` is the slug detected from the closest existing `spec.md` (or passed via CLI args).

## Language

Mirror the user's language in all output. Subagent spawn prompts can be English (technical), but reports to the user mirror user language.

---

## Phase 1 — Detect Mode & Locate Spec

1. Parse args: `--review`, `--resume`, `--cleanup`
2. Find `spec.md` (path from config). If multiple `teams/*/spec.md` exist, ask user which feature.
3. If `--resume`: skip to Phase 4
4. If `--cleanup`: skip to Phase 7
5. Verify spec is approved (no `TODO`/`?` markers in critical sections). If not, halt and tell user to finish grilling.

---

## Phase 2 — Install Role Subagents (Idempotent)

For each role in `fe`, `be`, `qa`, `docs`, `verifier`:

1. Check if `.claude/agents/{role}.md` exists in project root
2. If missing, copy from this skill's bundled `agents/{role}.md` to `.claude/agents/{role}.md`
3. Do not overwrite existing files — users may have customized them

This makes the skill self-installing per project.

---

## Phase 3 — Generate `plan.md`

Read `spec.md` and `context.md`. Generate `plan.md` using `PLAN-TEMPLATE.md`.

Rules for plan generation:

1. **Role sections** — emit only sections that have actual work. If a feature has no UI changes, do not write a `## FE Tasks` section at all.
2. **Task IDs** — every task gets a stable ID: `[FE-1]`, `[BE-2]`, `[QA-1]`, `[DOCS-1]`. Use these as ubiquitous language.
3. **Required fields per task:**
   - `Acceptance:` — testable, not "works correctly"
   - `Verify:` — concrete command (e.g. `pnpm test src/api/auth.test.ts`)
   - `Files:` — every file the task will touch (no overlap between tasks in the same wave)
   - `Depends:` — task IDs this task waits for (optional, empty = ready immediately)
4. **TDD intrinsic** — every dev task (FE/BE) MUST include both the test file and the implementation file in `Files:`. The task itself does RED → GREEN within its single execution.
5. **Interface contracts** — if a task exposes an API/component used by another task, define the signature inline in the task body. Subagents follow the contract; they don't redesign it.

If `--review` mode: write `plan.md`, then output:

```
Plan written to {plan-path}.
Review it, then run /implement --resume to execute.
```

And halt. Do not proceed to Phase 4.

If default mode: proceed to Phase 4.

---

## Phase 4 — Execute via Topological Wave Dispatch

Repeat until all unchecked tasks `[ ]` in `plan.md` are completed:

### 4.1 Compute current wave

Scan `plan.md`. A task is **ready** if:
- Status is `[ ]` (unchecked)
- All IDs in its `Depends:` are `[x]` (completed) or the `Depends:` field is empty

Collect all ready tasks. These form the current wave.

If no ready tasks exist but unchecked tasks remain → there's a dependency cycle or typo. Halt and report.

### 4.2 Spawn subagents in parallel

For each ready task in the wave, spawn the corresponding role subagent via the `Agent` tool. Use parallel tool calls in a single message — one `Agent` call per task.

Spawn prompt template:

```
You are the {role} subagent for feature {feature-slug}.

Read these files for context:
- {context-path}
- {spec-path}
- {plan-path}
- CLAUDE.md (if exists)

Your task: {task-ID}

Full task body:
{paste task block from plan.md}

Rules:
1. Touch ONLY the files listed in Files:
2. If this is a dev task (FE/BE), write the failing test FIRST, then implementation.
3. Run the Verify: command. It must pass before you finish.
4. When done, mark the task complete in plan.md by changing [ ] to [x].
5. Report back: "Done: {task-ID}" or "Blocked: {reason}".
```

### 4.3 Wait for all subagents in wave to finish

Collect results.

### 4.4 Run verifier (always-on)

If the wave contained any FE/BE/QA tasks, spawn the `verifier` subagent:

```
You are the verifier. Run the full test suite.

Verify command: {detect from spec.md "Commands" → test, or default `pnpm test`}

Report ONLY:
- PASS or FAIL
- If FAIL: which tests failed, error messages (first 20 lines per failure), and which test files
- Do NOT attempt to fix anything.
```

Skip verifier if wave was pure DOCS.

### 4.5 Handle verifier result

- **PASS** → loop back to 4.1 for next wave
- **FAIL** → halt. Surface failures to user with these options:

```
Verifier failed after wave {N}.

Failed tests:
{verifier report}

Options:
(a) Retry the last wave's tasks — type "retry"
(b) Edit plan.md manually (add fix tasks, adjust deps) — type "edit"
(c) Abort — type "abort"
```

Wait for user. Do not auto-retry, do not auto-fix.

### 4.6 Subagent failure (Blocked)

If any subagent reports "Blocked: ...", treat like verifier fail — halt + ask user.

---

## Phase 5 — Final Verification

After all tasks are `[x]`:

1. Spawn `verifier` one last time — full test suite must pass cleanly
2. If pass → proceed to Phase 6
3. If fail → halt + ask user (same options as 4.5)

---

## Phase 6 — Hand Off

Output:

```
Done. All tasks completed for {feature-slug}.

Files changed: (run `git diff --stat`, paste summary)

Changelog: {changelog-dir}/{feature}.md

Next:
- Review the diff
- Run /code-review or /security-review if needed
- Commit and ship when ready

Run /implement --cleanup to remove teams/{feature}/ when done.
```

Do **not** auto-commit. Do **not** auto-push. Manual gate at the end too.

---

## Phase 7 — Cleanup (Only on --cleanup)

If invoked with `--cleanup`:
1. Confirm with user: "Delete teams/{feature}/? [y/N]"
2. On yes: delete the folder
3. Report deleted paths

---

## Role → Model Mapping

Set in each subagent definition's frontmatter:

| Role     | Model  | Why |
|----------|--------|-----|
| fe       | sonnet | Component design needs reasoning |
| be       | sonnet | API/DB logic needs reasoning |
| qa       | sonnet | Integration tests + edge cases need reasoning |
| docs     | haiku  | Changelog/README is templated |
| verifier | haiku  | Just runs tests, parses output |

Lead `/implement` itself runs on whatever model the user has selected (typically Opus for orchestration).

To override per-invocation: `/implement --model=sonnet` sets all subagents to that model for this run.

---

## Anti-patterns

- Spawning subagents sequentially when wave allows parallel
- Editing `plan.md` task body during execution (only allowed: `[ ]` → `[x]`)
- Lead writing implementation code itself instead of delegating
- Skipping verifier between waves
- Auto-retrying or auto-fixing on verifier fail
- Generating tasks without `Verify:` or `Files:`
- Auto-committing or auto-pushing after completion
