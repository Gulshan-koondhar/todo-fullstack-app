---
id: 007
title: auth-integrator subagent
stage: misc
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-multi-user-todo
branch: 001-multi-user-todo
user: user
command: manual
labels: ["subagent","security","auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/plans/jaunty-leaping-umbrella.md
  - .claude/agents/auth-integrator.md
tests:
  - none
---

## Prompt

Create a reusable subagent for full Better Auth + JWT integration across frontend and backend.

Name: auth-integrator
Autonomy Level: High (makes judgments on security correctness)
Invocation: Automatic for auth tasks or manual

Role: Autonomous guardian of user authentication and data isolation

Process (9 steps):
1. Configure Better Auth in frontend with JWT plugin and shared secret
2. Generate/validate BETTER_AUTH_SECRET in both .env files
3. Implement FastAPI JWT verification middleware using python-jose
4. Create dependency to extract and validate user_id from token
5. Ensure all protected routes use the JWT dependency
6. Configure frontend API client to attach JWT to Authorization: Bearer header
7. Handle 401 redirects on frontend
8. Test for common attacks (invalid token, expired, mismatched user_id)
9. Escalate if any security gap found

Decision Authority:
- ACCEPT: Full stateless JWT flow with user_id matching and filtering
- REJECT: Missing middleware, no ownership check, cookie instead of header
- ESCALATE: Complex cases like refresh tokens (not needed here)

Reporting Format:
=== AUTH INTEGRATION REPORT ===
Component: [frontend | backend | both]
Verdict: [ACCEPT | REJECT | ESCALATE]
Generated Code Files: [list]
Reasoning: [detailed criteria analysis]
Actions Required: [if ESCALATE or REJECT]

## Response snapshot

Created `.claude/agents/auth-integrator.md` defining the high-autonomy subagent with persona, pre-flight checks, 9-step operating procedure, decision matrix, reporting format, and safeguards aligned with Phase II Better Auth + JWT requirements.

## Outcome

- ✅ Impact: Added reusable auth-integrator subagent guarding Better Auth + JWT integration across frontend/backend.
- 🧪 Tests: Not run (definition-only change).
- 📁 Files: Plan updated; new subagent file authored.
- 🔁 Next prompts: None.
- 🧠 Reflection: Centralizing auth scrutiny ensures consistent data isolation and accelerates future security audits.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
