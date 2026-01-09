---
id: 004
title: endpoint-generator skill
stage: misc
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-multi-user-todo
branch: 001-multi-user-todo
user: user
command: manual
labels: ["skill","fastapi","phase-ii"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/plans/jaunty-leaping-umbrella.md
  - .claude/skills/endpoint-generator.md
tests:
  - none
---

## Prompt

Create a reusable skill for generating secure FastAPI task endpoints in Phase II.

Name: endpoint-generator
Autonomy Level: Low (human-guided, review at checkpoints)
Invocation: Manual via prompt in /sp.implement

Process (5 steps):
1. Read endpoint spec: HTTP method, path (including {user_id}, {task_id}), description, required auth
2. Generate FastAPI route decorator with correct path and dependencies (including JWT dependency from deps.py)
3. Implement handler logic using SQLModel: query/create/update/delete with user_id filtering
4. Add ownership verification: compare authenticated user_id with path user_id
5. Add proper response models, error handling (404 if not owned, 401 if no auth), validation

Output Format:
=== GENERATED ENDPOINT ===
Method & Path: [e.g., GET /api/v1/users/{user_id}/tasks]
File: [backend/app/api/v1/endpoints/tasks.py]
Code:
```python
[full route code]
```

## Response snapshot

Authored plan plus `.claude/skills/endpoint-generator.md` specifying persona, pre-flight questions, core principles, five-step process, implementation pattern, and output checklist to satisfy the requested reusable skill behavior.

## Outcome

- ✅ Impact: Added documented low-autonomy endpoint-generator skill aligned with Phase II FastAPI security requirements.
- 🧪 Tests: Not run (documentation/codegen guidance only).
- 📁 Files: Plan file and new skill markdown updated.
- 🔁 Next prompts: None.
- 🧠 Reflection: Structured skill guidance will help future endpoint generation stay compliant with JWT + ownership constraints.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
