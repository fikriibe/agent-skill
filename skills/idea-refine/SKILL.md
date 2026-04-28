---
name: idea-refine
description: Refines raw ideas into actionable concepts via structured divergent + convergent thinking. Trigger with "refine this idea", "ideate on X", or "stress-test my plan".
version: 1.1.0
---

# Idea Refine

## Process (3 Phases — don't skip, don't merge)

### Phase 1: Understand & Expand
1. Restate the idea as a **"How Might We"** problem statement
2. Ask **3–5 sharpening questions** (who is this for? what's success? constraints? why now?) — wait for answers before proceeding
3. Generate **5–8 variations** using these lenses:
   - Inversion · Constraint removal · Audience shift · Combination · 10x simpler · 10x scale · Expert blindspot
4. If inside a codebase: scan with Glob/Grep — ground ideas in existing architecture

### Phase 2: Evaluate & Converge
1. Cluster resonating ideas into **2–3 distinct directions**
2. Stress-test each: **User value** (painkiller or vitamin?) · **Feasibility** · **Differentiation**
3. Surface **hidden assumptions** per direction — what you're betting is true, what could kill it, what you're ignoring

> Be honest, not supportive. Push back on weak ideas with kindness and specificity.

### Phase 3: Sharpen & Ship
Produce a markdown one-pager, ask user to confirm before saving to `docs/ideas/[idea-name].md`:

```markdown
# [Idea Name]

## Problem Statement
[One-sentence HMW framing]

## Recommended Direction
[Chosen direction + why — 2–3 paragraphs max]

## Key Assumptions to Validate
- [ ] [Assumption — how to test it]

## MVP Scope
[Minimum version that tests the core assumption]

## Not Doing (and Why)
- [Thing] — [reason]

## Open Questions
- [Unresolved question before building]
```

## Anti-patterns
- Generating 20+ shallow ideas instead of 5–8 considered ones
- Skipping "who is this for"
- No assumptions surfaced before committing to a direction
- Yes-machining weak ideas
- No "Not Doing" list
- Jumping to Phase 3 without running Phases 1 & 2

## Done When
- [ ] Clear HMW problem statement exists
- [ ] Target user + success criteria defined
- [ ] Multiple directions explored
- [ ] Hidden assumptions listed with validation strategies
- [ ] "Not Doing" list makes trade-offs explicit
- [ ] User confirmed direction before any implementation