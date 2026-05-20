# Feature Team Skill — Design Notes

> Ideation session: Agent Teams untuk feature development workflow

---

## Core Idea

Skill yang spawn multi-agent team (FE, BE, QA, Docs) secara dinamis berdasarkan spec + plan, dengan phase gates yang membutuhkan manual approval sebelum eksekusi.

---

## Skill Chain (3 Tier)

```
/spec       → spec.md         ("apa yang dibangun")
  ↓
/plan       → plan.md         ("siapa yang bangun + urutan + tasks per agent")
  ↓
⏸️ USER APPROVE plan.md
  ↓
/feature-team → spawn agents  ("eksekusi")
```

**Key insight:** Agent lahir saat `/plan` dijalankan, bukan saat `/spec`. Plan adalah kontrak — semua ambiguity resolved sebelum token mahal dipakai.

---

## Dynamic Role Selection

Agents yang di-spawn ditentukan dari spec, bukan hardcoded. Contoh frontmatter di `plan.md`:

```yaml
---
feature: auth-refresh
required_agents: [fe, architecture]
reason: no new BE endpoints, just token logic refactor
---
```

Feature sederhana → spawn FE saja. Feature full-stack → spawn FE + BE + architecture. Zero waste.

---

## Execution Flow

```
1. SPEC GATE
   spec.md exists? NO → redirect /spec
   YES → parse required_agents

2. SPAWN PHASE (dynamic)
   spawn only needed agents
   tiap agent ambil tasks dari plan.md section miliknya
   self-report done via task list

3. PHASE GATE
   lead monitor task board
   semua tasks done → ⏸️ USER APPROVE → spawn QA

4. QA SPAWN
   lead briefs QA: perubahan + edge cases + concerns
   QA self-report done → ⏸️ USER APPROVE → spawn Docs

5. DOCS SPAWN
   lead briefs Docs: git diff + spec + QA findings
   Docs self-report done

6. FULL CLEAN
   lead nulis final summary → docs/changelogs/{feature}.md
   TeamDelete semua agents
```

---

## QA + Docs: Context Strategy

**Pilihan diputuskan: Lead agent brief langsung (bukan handoff files)**

Lead agent sudah punya full picture dari semua phase sebelumnya. Dia yang brief QA dan Docs saat spawn — kayak PM yang brief QA setelah dev done.

Handoff files (`handoff/{role}.md`) tetap ditulis sebagai **audit trail** kalau feature complex, tapi bukan primary mechanism.

---

## Team Folder Structure

```
~/.claude/teams/{team-name}/
  config.json      ← runtime state (auto-generated, jangan touch)
  inboxes/         ← mailbox per agent
  plan.md          ← tasks + agent assignments
```

Tidak ada role files di sini. Role context di-compose dinamis oleh lead saat spawn.

---

## Role Context: Dynamic Composition (No Static Files)

**Keputusan: Hapus role template files. Lead agent compose role context on-the-fly.**

Dynamism datang dari 3 sumber yang sudah exist:

| Source | Kontribusi |
|---|---|
| CLAUDE.md (project-level) | Tech stack, conventions, project context |
| spec.md + plan.md | Feature-specific tasks + constraints |
| Skill definition (`/feature-team`) | Base identity + skill list per role (hardcoded, stable) |

Lead synthesizes semua itu jadi spawning brief saat spawn. Tidak ada file static yang perlu di-maintain.

**Trade-off:** Lead butuh context window cukup besar di awal spawn — acceptable karena one-time cost.

---

## Skills Needed

| Skill | Status | Notes |
|---|---|---|
| `/spec` | ✅ Exists | Output: `spec.md` |
| `/plan` | 🔨 Extend | Extend dari `planning-and-task-breakdown`, tambah agent assignment + scaffolding team folder |
| `/feature-team` | 🆕 New | Consume `plan.md`, orchestrate spawn + gate + brief |

---

## Open Questions (Resolved)

- ✅ Self-report done via task list? → **Ya**
- ✅ Siapa trigger next phase? → **Manual approval user**
- ✅ QA + Docs dapat context dari mana? → **Lead briefs langsung**
- ✅ Role files global atau per-team? → **Tidak ada role files — dynamic composition**
- ✅ Spawn semua parallel atau sequential? → **Dynamic, dependency-aware. QA + Docs adalah post-process agents**