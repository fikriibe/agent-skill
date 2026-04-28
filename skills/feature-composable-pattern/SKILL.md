---
name: feature-composable-pattern
description: Enforces component data flow architecture. Use when building any component that needs data or actions. Works with React (hooks), Vue (composables), or any component-based framework.
version: 1.0.0
---

# Feature Composable Pattern

## Data Flow

```
Page/Route → fetch data, own top-level state
  └── Hook/Composable → actions, side effects, shared logic
        └── Component → receive data as props + call hook directly
              └── Child → same hook, no prop drilling
```

**Components never fetch.** Data flows down via props. Actions come from hooks/composables — not props.

---

## Extract a Hook/Composable When

- **3+ functions** related to the same concern, OR
- **Used in 2+ components**, OR
- **Has side effects** — API calls, store mutations, subscriptions

Otherwise inline is fine.

---

## Pattern (framework-agnostic)

```
// 1. Page — fetches, owns state
TasksPage:
  tasks = fetch('/api/tasks')
  render: <TaskList tasks={tasks} />

// 2. Hook/Composable — actions + side effects
useTaskActions():
  complete(id) → API + store update
  remove(id)   → API + store update
  update(id)   → API + store update
  return { complete, remove, update }

// 3. Component — entity props + hook directly
TaskCard(props: { task: Task }):
  { complete, remove } = useTaskActions()

// 4. Child — same hook, no drilling
TaskActions(props: { taskId: string }):
  { complete, remove } = useTaskActions()  ← no prop drilling
```

---

## Decision Guide

```
Need data?
├── Page already fetched? → prop ✅
└── Not fetched? → fetch in page, pass down (never in component)

Need actions?
├── 1-2 fns, used once? → inline
├── 3+ fns / used in 2+ places / has side effect? → extract hook

Props drilling too deep?
└── Child needs entity + actions? → call hook directly in child
```

## Never
- Fetch inside a component — pages only
- Pass action functions as props — use hook/composable instead
- Duplicate logic across components — extract and share