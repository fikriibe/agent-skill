---
name: frontend-ui-engineering
description: Builds production-quality UIs. Use when building or modifying user-facing interfaces — components, layouts, state, or anything visual. Use when output needs to look production-quality, not AI-generated.
---

# Frontend UI Engineering

## Component Architecture

**File structure — colocate everything:**
```
src/components/TaskList/
  TaskList.tsx
  TaskList.test.tsx
  use-task-list.ts   ← custom hook if state is complex
```

**Composition over configuration:**
```tsx
// ✅ Composable
<Card><CardHeader>...</CardHeader><CardBody>...</CardBody></Card>

// ❌ Over-configured
<Card title="..." headerVariant="large" bodyPadding="md" />
```

**Separate data from presentation:**
```tsx
// Container: fetches data
export function TaskListContainer() {
  const { tasks, isLoading, error } = useTasks();
  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorState message="Failed to load tasks" />;
  if (!tasks.length) return <EmptyState message="No tasks yet" />;
  return <TaskList tasks={tasks} />;
}

// Presentation: pure render
export function TaskList({ tasks }: { tasks: Task[] }) {
  return <ul role="list">{tasks.map(t => <TaskItem key={t.id} task={t} />)}</ul>;
}
```

---

## State Management — simplest approach that works

```
useState          → component-local UI state
Lifted state      → 2-3 sibling components
Context           → theme, auth, locale (read-heavy)
URL state         → filters, pagination (shareable)
React Query / SWR → remote data with caching
Zustand / Redux   → complex shared client state
```

Avoid prop drilling deeper than 3 levels.

---

## Avoid the AI Aesthetic

| AI Default | Fix |
|---|---|
| Purple/indigo everything | Use the project's actual color palette |
| Excessive gradients | Flat or subtle, matching design system |
| rounded-2xl everywhere | Consistent radius from design system |
| Oversized padding | Consistent spacing scale |
| Lorem ipsum | Realistic placeholder content |
| Shadow-heavy design | Subtle or none unless design system says so |
| Generic card grids | Purpose-driven layouts |

**Spacing:** use the scale only — no arbitrary pixel values like `13px` or `2.3rem`.

**Typography:** don't skip heading levels, don't use heading styles for non-heading content.

**Color:** use semantic tokens (`text-primary`, `bg-surface`), ensure 4.5:1 contrast ratio, never use color as the sole state indicator.

---

## Accessibility (WCAG 2.1 AA)

```tsx
// Keyboard accessible
<button onClick={handle}>Click</button>       // native, focusable
<div onClick={handle}>Click</div>             // NOT focusable — avoid

// Label inputs
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Label icon-only buttons
<button aria-label="Close dialog"><XIcon /></button>
```

**Focus management** — move focus when content changes (e.g., dialogs open). Trap focus inside modals.

**Always handle all states:**
```tsx
if (tasks.length === 0) return (
  <div role="status" className="text-center py-12">
    <h3>No tasks</h3>
    <p>Get started by creating a new task.</p>
    <Button onClick={onCreateTask}>Create Task</Button>
  </div>
);
```

---

## Responsive Design

Mobile-first. Test at: **320px · 768px · 1024px · 1440px**

```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
```

---

## Loading States

```tsx
// Skeleton > spinner for content areas
function TaskListSkeleton() {
  return (
    <div aria-busy="true" aria-label="Loading tasks" className="space-y-3">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="h-12 bg-muted animate-pulse rounded" />
      ))}
    </div>
  );
}
```

---

## Authority Delegation

Jika project menggunakan `/design-pipeline`, delegasikan ke skill yang tepat — jangan override:

| Domain | Authority | Tindakan skill ini |
|---|---|---|
| Visual taste & layout | `taste-skill` | Ikuti output taste-skill, jangan re-style |
| Motion & animation | `animate-skill` | Jangan tambah animasi manual — serahkan ke animate-skill |
| Component conversion | `stitch-skills/react-components` | Gunakan komponen yang sudah di-generate |
| Integration, state, data flow, a11y | **skill ini** | Fokus di sini |
| Final gate / anti-placeholder | `output-skill` | Dipanggil setelah implementasi selesai |

---

## Red Flags
- Component >200 lines (split it)
- Inline styles or arbitrary pixel values
- Missing loading, error, or empty states
- No keyboard navigation
- Color as sole state indicator
- AI aesthetic (purple gradients, generic card grids)

## Done When
- [ ] Renders without console errors
- [ ] All interactive elements keyboard accessible (Tab through page)
- [ ] Responsive at 320px, 768px, 1024px, 1440px
- [ ] Loading + error + empty states all handled
- [ ] Follows project design system (spacing, colors, typography)
- [ ] No axe-core accessibility warnings