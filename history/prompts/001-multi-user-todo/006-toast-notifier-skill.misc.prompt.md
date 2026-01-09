---
id: 006
title: toast-notifier skill
stage: misc
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-multi-user-todo
branch: 001-multi-user-todo
user: user
command: manual
labels: ["skill","sonner","frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/plans/jaunty-leaping-umbrella.md
  - .claude/skills/toast-notifier.md
tests:
  - none
---

## Prompt

Create a simple skill for adding Sonner toast notifications.

Name: toast-notifier
Autonomy Level: Low

Process (4 steps):
1. Determine action type (create, update, delete, complete)
2. Generate appropriate success message
3. Use Sonner toast.success() with optional icon and duration (3s)
4. Integrate into mutation hooks (e.g., after API call)

Output Format:
=== GENERATED TOAST ===
Action: [create | etc.]
Code Snippet:
```tsx
[toast call]
```

## Response snapshot

Added `.claude/skills/toast-notifier.md` capturing persona, questions, principles, four-step workflow, output format, reference snippets, and integration reminders for Sonner success toasts.

## Outcome

- ✅ Impact: Documented toast-notifier skill aligned with Phase II Sonner requirements (messages, icons, duration).
- 🧪 Tests: Not run (docs change only).
- 📁 Files: Plan updated; new skill file created.
- 🔁 Next prompts: None.
- 🧠 Reflection: Centralizing toast snippet guidance ensures consistent UX and faster implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
