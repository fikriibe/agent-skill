---
name: plan
description: Scaffolds the task plan and feature team folders. Runs automatically after spec approval.
version: 1.0.0
---

# Spec-driven Development: Phase 2 & 3 (Planning & Task Breakdown)

This skill creates the task breakdown plan and scaffolds the workspace directories for the feature team agents.

## Input Configuration
Read configuration options from `CLAUDE.md` / `AGENT.md`:
- `plan.save_path`: Path to save the plan file (default: `teams/{team-name}/plan.md`).
- `feature_team.default_roles`: Default roles if spec doesn't define `required_agents`.

## Guidelines
1. Parse the approved `spec.md` (e.g. `docs/spec.md`) to extract:
   - The feature name.
   - The list of `required_agents` (e.g. `[fe, be]`).
2. Run `python3 scripts/team_manager.py init <team-name> [required_agents...]` using the required `rtk` prefix.
   - This creates `teams/{team-name}/` and initializes the template `plan.md` at `teams/{team-name}/plan.md` (or the customized `plan.save_path`).
3. Fill out the `plan.md` file with specific tasks under the heading-based role sections:
   - `## Architecture Tasks`
   - `## Frontend Tasks`
   - `## Backend Tasks`
   - `## QA Tasks`
   - `## Documentation Tasks`
4. Each task must follow this exact format:
   ```markdown
   - [ ] Task: [Description]
     Acceptance: [What must be true when done]
     Verify: [Verification command or checks]
     Files: [List of files touched]
   ```
5. **No User Gate**: Do not ask the user for approval. Once `plan.md` is populated, proceed directly to run `/feature-team`.

## Done When
- `teams/{team-name}/` directory and inboxes are fully scaffolded.
- Specific tasks are divided under the correct role headings in `plan.md`.
- Ready to execute via `/feature-team`.
