---
name: feature-team
description: Orchestrates the multi-agent execution team (FE, BE, QA, Docs, Architecture) based on spec and plan. Handles manual/auto gates and auto-cleanup.
version: 1.0.0
---

# Feature Team Skill

This skill acts as the orchestrator/router for executing the tasks defined in `plan.md` using specialized roles.

## Input Configuration
Read configuration options from `CLAUDE.md` / `AGENT.md` under `feature_team`:
- `default_roles`: Fallback roles if not defined in spec.
- `testing_strategy`: Dictates verification style (e.g. `manual` vs `unit`).
- `create_docs`: If true, spawns the documentation agent.
- `auto_approve_dev_to_qa`: Auto-approves Gate 3.
- `auto_approve_qa_to_docs`: Auto-approves Gate 4.
- `cleanup_on_done`: If true, deletes `teams/{team-name}/` on completion.

## Role Spawning Rules
When an agent is active, it must:
1. Load and assume the persona in `agents/{role}.md` (e.g., `agents/fe.md`).
2. Load task list from `teams/{team-name}/plan.md` and work exclusively on tasks in its section.
3. Automatically load `CLAUDE.md` and `DESIGN.md` (if present) for project standards and tokens.

## Execution Flow

### 1. Start / Status Check
Run the status command using the required prefix:
`python3 scripts/team_manager.py status <team-name>`
This will output a status dashboard of all agents and tasks.

### 2. Development Phase
- Spawns active developers (`fe`, `be`, `architecture` as listed in `required_agents`).
- Dev agents execute tasks one by one, checking them off in `plan.md`.
- **Gate 3 (Dev Complete)**: Once all development tasks are checked off, the team pauses.
  - If `auto_approve_dev_to_qa` is `true`, it immediately triggers the next phase.
  - If `false`, the agent will output: `Development complete. Proceed to QA?` and wait for the user to approve by running:
    `python3 scripts/team_manager.py approve <team-name>`

### 3. QA Phase (if qa is active)
- Spawns the `qa` agent.
- QA writes/runs tests based on `testing_strategy`.
- **Gate 4 (QA Complete)**: Once QA tasks are checked off, the team pauses.
  - If `auto_approve_qa_to_docs` is `true`, it triggers the next phase.
  - If `false`, wait for user approval by running:
    `python3 scripts/team_manager.py approve <team-name>`

### 4. Docs Phase (if docs is active)
- Spawns the `docs` agent.
- Docs reads git diffs/QA findings to generate a changelog.
- Finalize by running:
  `python3 scripts/team_manager.py approve <team-name>`

### 5. Completion & Cleanup
- The team manager writes `docs/changelogs/{team-name}.md`.
- If `cleanup_on_done` is `true`, the `teams/{team-name}/` folder is deleted.

## Done When
- All tasks in the plan are checked off.
- The changelog is generated under `docs/changelogs/`.
- Team folders are cleaned up or finalized.
