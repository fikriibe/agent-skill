---
name: design-pipeline
description: >
  Router/orchestrator untuk design phase dalam development workflow. Digunakan setelah
  spec-driven-development menghasilkan needs_design_phase: true. Jalankan ketika membangun
  greenfield project dengan UI, ada >= 3 screens baru, atau spec menyebut "design system",
  "redesign", atau "visual". Skip untuk bug-fix, refactor, backend-only, atau project yang
  sudah punya design system.
  Trigger: "start project [name] --with-design", "redesign [feature]", "polish [component]"
---

# Design Pipeline

Orchestrator untuk design phase. Memastikan visual intent diproses secara berurutan dan setiap authority (taste, motion, output) tidak saling konflik.

## Decision Gate — jalankan di awal

```
Cek kondisi sebelum memulai:

needs_design_phase = true?  → cek DESIGN.md
                    false?  → skip design phase, lanjut ke /plan

Kondisi SKIP (tidak perlu design phase):
- task_type: bug-fix | refactor | backend-only
- DESIGN.md sudah ada di project root atau docs/
- has_existing_design_system: true
- jumlah screens baru < 3
```

---

## Config (dari CLAUDE.md / rules.md)

```
DESIGN_VARIANCE:    6   ← kreativitas layout (1-10)
MOTION_INTENSITY:   2   ← rendah, biar animate-skill yang authority
VISUAL_DENSITY:     5   ← kepadatan elemen visual (1-10)
```

---

## Design Flow (5 tahap berurutan)

```
Step 1: /enhance-prompt
  → Klarifikasi visual intent dari spec
  → Output: prompt yang lebih spesifik untuk Stitch
  → Stop jika intent masih ambigu — tanya user

Step 2: /stitch-design
  → Generate UI via Stitch MCP menggunakan enhanced prompt
  → Config: DESIGN_VARIANCE=6, MOTION_INTENSITY=2, VISUAL_DENSITY=5
  → Output: Stitch-generated layout + komponen

Step 3: /taste-skill (stitch-skill mode)
  → Inject premium design rules ke output Stitch
  → Authority: visual taste dan layout
  → JANGAN touch motion — itu domain animate-skill
  → Output: refined visual design

Step 4: /design-md
  → Ekstrak design tokens dari output Stitch + taste-skill
  → Output: DESIGN.md berisi color tokens, spacing, typography, component specs
  → Simpan ke root project atau docs/DESIGN.md

Step 5: /react-components
  → Konversi Stitch output ke React components
  → Output: siap dipakai di codebase, bukan placeholder
```

---

## Authority Matrix — jangan overlap

| Domain | Authority Skill | Yang lain: hands off |
|---|---|---|
| Visual taste & layout | `taste-skill` | — |
| Motion & animation | `animate-skill` | taste-skill harus set MOTION_INTENSITY rendah |
| Component conversion | `react-components` | — |
| Integration, state, a11y | `frontend-ui-engineering` | — |
| Final gate / anti-placeholder | `output-skill` | Dipanggil terakhir, bukan di tengah |

---

## Output dari Design Pipeline

Setelah design pipeline selesai:

```
docs/DESIGN.md              ← design tokens (color, spacing, typography)
src/components/[generated]/ ← React components dari Stitch

Nanti lanjut ke `/plan` dan `/feature-team`.
- Load `DESIGN.md` sebagai **persistent reference** (bukan inline)
- Load generated components **on-demand** per task, bukan semua sekaligus
```

---

## Trigger Phrases

| Phrase | Behavior |
|---|---|
| `start project [name]` | Auto-detect: jalankan design pipeline jika needs_design_phase=true |
| `start project [name] --with-design` | Force jalankan design pipeline |
| `start project [name] --skip-design` | Skip design pipeline |
| `redesign [feature]` | Langsung masuk design-pipeline (step 1) |
| `polish [component]` | Skip ke animate-skill + output-skill saja |

---

## Pitfalls

- **Naming conflict**: gunakan `taste-skill/stitch-skill`, bukan stitch-skills package punya
- **MCP not connected**: test Stitch MCP connection sebelum step 2
- **Motion conflict**: pastikan MOTION_INTENSITY: 2 di taste-skill config
- **Context bloat**: DESIGN.md jadi reference — jangan inline ke setiap step
- **output-skill di tengah**: dia final gate, hanya dipanggil di akhir frontend-ui-engineering

---

## Red Flags

- Menjalankan design pipeline untuk bug-fix atau refactor
- taste-skill dan animate-skill keduanya mengatur motion (konflik authority)
- output-skill dipanggil sebelum implementasi selesai
- DESIGN.md di-inline ke context — context akan bloat

## Done When

- [ ] DESIGN.md tersimpan di repo dengan color tokens, spacing, typography
- [ ] React components dari Stitch tidak ada placeholder content
- [ ] DESIGN.md di-load sebagai reference in context (bukan inline)
- [ ] Siap dilanjutkan ke /plan -> /feature-team
