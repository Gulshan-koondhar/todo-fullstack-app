---
id: 005
title: ui-component-builder skill
stage: misc
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-multi-user-todo
branch: 001-multi-user-todo
user: user
command: manual
labels: ["skill","frontend","shadcn","tailwind"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/plans/jaunty-leaping-umbrella.md
  - .claude/skills/ui-component-builder.md
tests:
  - none
---

## Prompt

Create a skill for generating beautiful, accessible Next.js UI components using shadcn/ui and Tailwind.

Name: ui-component-builder
Autonomy Level: Low
Invocation: Manual

Process (6 steps):
1. Read component spec: purpose, props, responsive needs, dark mode
2. Choose appropriate shadcn/ui primitives (Card, Dialog, Button, Checkbox, etc.)
3. Apply Tailwind styling for premium look (shadows, rounded, hover, spacing)
4. Add Lucide icons and proper ARIA labels
5. Implement interactions (toasts via Sonner, loading states)
6. Ensure responsiveness with Tailwind breakpoints and dark mode classes

Output Format:
=== GENERATED COMPONENT ===
Component: [TaskCard | AddTaskButton | etc.]
File: [path]
Code:
```tsx
[full component]
```

## Response snapshot

Captured plan plus `.claude/skills/ui-component-builder.md` that defines persona, pre-flight questions, core principles, six-step process, output format, example pattern, and review checklist to satisfy the requested low-autonomy skill.

## Outcome

- ✅ Impact: Added documented UI component builder skill aligned with shadcn/ui + Tailwind + Lucide + Sonner conventions.
- 🧪 Tests: Not run (documentation-only change).
- 📁 Files: Plan file updated; new skill markdown created.
- 🔁 Next prompts: None.
- 🧠 Reflection: Having a dedicated skill accelerates premium component generation while preserving accessibility and responsive standards.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
