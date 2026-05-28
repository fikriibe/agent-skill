# Agent Skills

> Forked and extended from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — original work by [Addy Osmani](https://github.com/addyosmani).

A curated collection of development skills for Claude Code — encoding workflows, quality gates, and engineering best practices into reusable slash commands.

---

## Install

```bash
# Clone the repo
git clone <repo-url> && cd agent

# Install all skills globally to Claude Code
./install.sh

# Or install a single skill
cp -r skills/grill-me-spec ~/.claude/skills/
```

After install, all skills are available in Claude Code via `/skill-name`.

### External Skills (install separately when needed)

These skills require external dependencies (Stitch MCP, etc.):

```bash
# Taste skill
npx skills add https://github.com/Leonxlnx/taste-skill

# Animate skill
npx skills add https://github.com/delphi-ai/animate-skill --skill animate
```

---

## Development Flow

```
                      +-------------------+
                      |  /grill-me-spec   | (Grills idea → context.md + spec.md)
                      +-------------------+
                                |
                   [GATE: User Approve spec.md]
                                |
                                v
                      +-------------------+
                      |    /implement     | (Generates plan.md → topological wave dispatch)
                      +-------------------+
                                |
                                v
                  [Wave N: spawn fe/be subagents in parallel]
                                |
                                v
                  [verifier subagent: run test suite]
                                |
                       pass? -> next wave
                       fail? -> halt + ask user
                                |
                                v
                       [Wave Q: spawn qa subagent]
                                |
                                v
                  [verifier subagent: full suite]
                                |
                                v
                      [Wave D: spawn docs subagent]
                                |
                                v
                  [Done — review diff, commit manually]
                                |
                                v
                 /implement --cleanup (optional)
```

`--review` mode pauses after plan.md is written so you can inspect or edit it
before execution. `--resume` continues from existing plan.md.

---

## Skills

| Skill | Description |
|---|---|
| `grill-me-spec` | Grill idea into `context.md` + `spec.md` (Mode C adds ADRs). For casual grilling without files, use `grill-me` |
| `grill-me` | Casual ideation grilling — no file output. Local mirror of `anthropic-skills:grill-me` for bundled distribution |
| `implement` | Generates `plan.md` from `spec.md`, dispatches `fe`/`be`/`qa`/`docs` subagents in topological waves with per-wave `verifier` |
| `api-and-interface-design` | Design stable, hard-to-misuse APIs and interfaces |
| `context-engineering` | Optimize agent context setup for consistent output quality |
| `test-driven-development` | RED → GREEN → REFACTOR cycle |
| `debugging-and-error-recovery` | Systematic root-cause debugging |
| `code-simplification` | Refactor for clarity without changing behavior |
| `git-workflow-and-versioning` | Trunk-based development + atomic commits |
| `glossary` | Scan codebase → generate `GLOSSARY.md` (Ubiquitous Language: canonical names, definitions, interface contracts) |

---

## References

Skills in this repo are adapted and extended from:

- **Core skills** — [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main/skills)
- **External skills** (install separately):
  - Taste skill — [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
  - Animate skill — [delphi-ai/animate-skill](https://github.com/delphi-ai/animate-skill)
  - Emil animation principles — [emilkowalski/skill](https://github.com/emilkowalski/skill)
