---
id: 1
title: Hackathon constitution
stage: constitution
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: unknown
command: /sp.constitution
labels: ["constitution", "governance", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - Constitution template validation
 - Dependency verification (plan-template.md, spec-template.md, tasks-template.md)
 - PHR template alignment
---

## Prompt

Project: Hackathon II - Evolution of Todo Phase II: Full-Stack Web Application
Core principles:
- Strict Spec-Driven Development with zero manual coding
- Complete user data isolation and security through JWT authentication
- Clean, modular, and maintainable full-stack architecture
- Reusability and extensibility to support future phases (chatbot, Kubernetes, event-driven)
- Bonus-eligible implementation of reusable intelligence (skills and subagents)

Key standards:
- All code must be generated exclusively by Claude Code through spec refinement
- Every feature must have its own dedicated Markdown spec file before implementation
- Agentic Dev Stack workflow must be followed: spec → plan → tasks → implement
- Authentication via Better Auth with stateless JWT tokens
- API endpoints must exactly match the specified REST contract with user_id in path
- Database operations must always filter by authenticated user_id
- Monorepo structure must follow the hackathon-specified layout with organized specs

Constraints:
- Technology stack locked: Next.js 16+ (App Router), FastAPI, SQLModel, Neon Serverless PostgreSQL, Better Auth
- No deviations from the defined API endpoints or authentication flow
- Shared BETTER_AUTH_SECRET environment variable across frontend and backend
- All requests without valid JWT must return 401 Unauthorized
- Task ownership enforced on every CRUD operation

Success criteria:
- Working multi-user web application with full CRUD for tasks
- Users can only view, create, update, and delete their own tasks
- Responsive frontend interface deployed on Vercel
- Backend API secured with JWT verification and user filtering
- Public GitHub repository containing constitution, full specs history, generated code, and CLAUDE.md files
- Successful demonstration in <90-second video showing signup, login, task management, and isolation between users
- Evidence of reusable intelligence usage (skills/subagents) for bonus consideration
- Zero manual code edits — all implementation traceable to spec-driven iterations

## Response snapshot

Successfully created the Hackathon II constitution (v1.0.0) with six core principles:

1. **Spec-Driven Development** - Zero manual coding, all code generated through spec refinement
2. **User Data Isolation and Security** - JWT authentication with Better Auth, strict data isolation
3. **Clean, Modular Architecture** - Support for future phases (chatbot, Kubernetes, event-driven)
4. **Reusable Intelligence Implementation** - Skills and subagents for bonus eligibility
5. **Agentic Dev Stack Workflow** - Enforced spec → plan → tasks → implement sequence
6. **Technology Stack Compliance** - Locked stack: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth

The constitution includes comprehensive sections on technology stack constraints, API contract requirements, authentication flow, data isolation, and governance. Templates (plan-template.md, spec-template.md, tasks-template.md) were verified to align with the constitution.

Version: 1.0.0 | Ratified: 2026-01-03 | Last Amended: 2026-01-03

## Outcome

- ✅ Impact: Established foundational governance document for Hackathon II development
- 🧪 Tests: Template validation completed; all templates aligned with constitution principles
- 📁 Files: Created .specify/memory/constitution.md (v1.0.0)
- 🔁 Next prompts: /sp.specify to create first feature specification
- 🧠 Reflection: Constitution successfully encodes all user requirements into enforceable principles with clear governance model

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (constitution creation, no automated tests)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test constitution by creating first feature spec and verifying compliance
