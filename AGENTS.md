## Config


```yaml
design_pipeline:
  enabled: auto              # auto | true | false
  strategy: hybrid-smart
  triggers:
    - greenfield_project
    - ui_screens_count: ">=3"
    - spec_mentions: ["design system", "redesign", "visual"]
  skip_when:
    - task_type: ["bug-fix", "refactor", "backend"]
    - has_existing_design_system: true

stitch_config:
  motion_intensity: 2        # rendah — animate-skill yang authority untuk motion
  design_variance: 6
  visual_density: 5

skills_priority:
  motion_authority: animate-skill
  taste_authority: taste-skill/stitch-skill
  output_gate: output-skill

spec:
  save_path: docs/spec.md
  auto_plan: true

plan:
  save_path: teams/{team-name}/plan.md

feature_team:
  default_roles: [fe, be]
  testing_strategy: manual # Options: unit, e2e, browser, unit+e2e, all, manual
  create_docs: true # If false, bypasses docs agent spawning entirely
  auto_approve_dev_to_qa: false # If true, auto-approves Gate 3
  auto_approve_qa_to_docs: false # If true, auto-approves Gate 4
  cleanup_on_done: false
```
