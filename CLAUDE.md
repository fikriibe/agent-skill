# Agent Skills Repo

Repo ini berisi koleksi development skills untuk Claude Code. Lihat README.md untuk daftar skills dan cara install.

---

## Design Pipeline Config

Config ini dibaca oleh `/design-pipeline` untuk menentukan behavior design phase.

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
```
