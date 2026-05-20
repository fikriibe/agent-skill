---
name: spec
description: Creates technical specifications before coding. Use when starting a new project, feature, or significant change. Skip for simple bug-fixes.
version: 1.0.0
---

# Spec-driven Development: Phase 1 (Specify)

This skill creates a technical specification (`spec.md`) based on the feature requirements.

## Input Configuration
Read config options from `CLAUDE.md` / `AGENT.md` under `spec`:
- `save_path`: Path to save the spec file (default: `docs/spec.md`).
- `auto_plan`: If true, automatically run `/plan` after spec approval.

## Guidelines
1. **Before writing anything**, surface assumptions explicitly to the user:
   ```
   ASSUMPTIONS I'M MAKING:
   1. [assumption]
   2. [assumption]
   -> Correct me now or I'll proceed with these.
   ```
2. Write the specification inside the file specified by `spec.save_path` (default: `docs/spec.md`) covering these 6 areas:
   - **Objective**: What, why, who. Success criteria or user stories.
   - **Tech Stack**: Framework, language, key dependencies and versions.
   - **Commands**: Build, test, lint, dev commands.
   - **Project Structure**: Directory layout with descriptions.
   - **Code Style**: Key conventions + one real code snippet showing style.
   - **Testing Strategy**: Testing frameworks, paths, and expectation levels.
3. **Important Constraints**:
   - **Do NOT include visual or ASCII layouts** in the spec.
   - Evaluate whether a design phase is needed (`needs_design_phase` = true if UI-heavy, >=3 screens, or redesign/visuals are mentioned).
   - Define the list of `required_agents` in the frontmatter of `spec.md` (e.g. `[fe, be]`, `[fe, be, architecture]`).

## Done When
- All 6 spec areas are covered.
- Success criteria are specific and testable.
- The `spec.md` file is saved to the configured save path.
- **STOP and request human review and approval before proceeding.**
