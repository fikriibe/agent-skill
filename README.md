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
cp -r skills/design-pipeline ~/.claude/skills/
```

After install, all skills are available in Claude Code via `/skill-name`.

### External Skills (install separately when needed)

These skills require external dependencies (Stitch MCP, etc.):

```bash
# Stitch skills — requires Stitch MCP: https://stitch.withgoogle.com/docs/mcp/setup
npx skills add google-labs-code/stitch-skills --skill stitch-design --global
npx skills add google-labs-code/stitch-skills --skill enhance-prompt --global
npx skills add google-labs-code/stitch-skills --skill design-md --global
npx skills add google-labs-code/stitch-skills --skill react-components --global

# Taste skill
npx skills add https://github.com/Leonxlnx/taste-skill

# Animate skill
npx skills add https://github.com/delphi-ai/animate-skill --skill animate
```

---

## Development Flow

```
/idea-refine
    Raw idea → problem statement + MVP scope + "not doing" list
    ↓
/spec-driven-development
    Requirements → spec (6 areas) → tasks
    Output flags: needs_design_phase? + design_complexity
    ↓
/design-pipeline  ← only if needs_design_phase: true
    ├── /enhance-prompt       clarify visual intent
    ├── /stitch-design        generate UI via Stitch MCP
    ├── /taste-skill          inject premium design rules
    ├── /design-md            extract design tokens → DESIGN.md
    └── /react-components     convert to React components
    ↓
/context-engineering
    Set up CLAUDE.md + load DESIGN.md as a persistent reference
    ↓
/api-and-interface-design       if API contracts need to be defined
    ↓
/incremental-implementation
    Implement in vertical slices (~100 lines per commit)
    ↓
/frontend-ui-engineering
    ├── integration + state + data flow + accessibility
    ├── /animate-skill        motion layer (Emil's principles)
    └── /output-skill         final gate, no placeholders
```

### Trigger Phrases

| Phrase | Behavior |
|---|---|
| `start project [name]` | Full flow, auto-detect design phase |
| `start project [name] --with-design` | Force design phase |
| `start project [name] --skip-design` | Skip design phase |
| `redesign [feature]` | Jump directly to design-pipeline |
| `polish [component]` | Run animate-skill + output-skill only |

---

## Skills

| Skill | Description |
|---|---|
| `idea-refine` | Structure a raw idea into an actionable concept |
| `spec-driven-development` | Write specs before code — 4-phase gated workflow |
| `api-and-interface-design` | Design stable, hard-to-misuse APIs and interfaces |
| `design-pipeline` | Router/orchestrator for the design phase (Stitch + taste + animate) |
| `context-engineering` | Optimize agent context setup for consistent output quality |
| `incremental-implementation` | Deliver changes in small, testable vertical slices |
| `frontend-ui-engineering` | Build production-quality UIs, not AI-aesthetic ones |
| `feature-composable-pattern` | Component data flow architecture (React / Vue) |
| `test-driven-development` | RED → GREEN → REFACTOR cycle |
| `debugging-and-error-recovery` | Systematic root-cause debugging |
| `code-simplification` | Refactor for clarity without changing behavior |
| `git-workflow-and-versioning` | Trunk-based development + atomic commits |

---

## References

Skills in this repo are adapted and extended from:

- **Core skills (10)** — [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main/skills)
- **design-pipeline** — custom orchestrator built in this repo
- **External skills** (install separately):
  - Stitch skills — [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills)
  - Taste skill — [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
  - Animate skill — [delphi-ai/animate-skill](https://github.com/delphi-ai/animate-skill)
  - Emil animation principles — [emilkowalski/skill](https://github.com/emilkowalski/skill)
