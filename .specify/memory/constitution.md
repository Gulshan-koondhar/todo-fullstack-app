<!--
  Sync Impact Report
  =================
  Version: 1.0.0 → 1.1.0
  Change: Updated constitution to emphasize AI-native design, MCP protocol, and stateless AI with persistent memory
  Modified Principles: I. AI-Native Design, V. Reusable Intelligence Implementation, VI. Agentic Dev Stack Workflow
  Added Sections: MCP Protocol Compliance, Stateless AI Architecture
  Removed Sections: None
  Templates Updated:
    ✅ plan-template.md - Updated to reflect MCP requirements
    ✅ spec-template.md - Updated to reflect AI-native design requirements
    ✅ tasks-template.md - Updated to reflect stateless AI architecture requirements
    ✅ phr-template.prompt.md - No changes needed
  Follow-up TODOs: None
-->

# Phase III – AI-Powered Todo Chatbot (Spec-Driven Development) Constitution

## Core Principles

### I. AI-Native Design (Agent-First, Tool-Driven, No Hardcoded Flows)
All functionality MUST be implemented through AI agents using the official MCP SDK. Natural language input MUST be translated into structured tool calls. AI agents MUST NOT directly manipulate databases or bypass existing FastAPI APIs. All Todo operations MUST be executed via MCP tools backed by FastAPI APIs. AI agent MUST NOT directly manipulate the database. Natural language input MUST be translated into structured tool calls. Agent decisions MUST be explainable and traceable.

**Rationale**: Ensures deterministic, traceable AI operations while maintaining separation of concerns between AI reasoning and data storage.

### II. Spec-Driven Development
All code MUST be generated exclusively by Claude Code through spec refinement. Every feature MUST have its own dedicated Markdown spec file before implementation. Zero manual coding is permitted outside the spec-driven workflow - all implementation MUST be traceable to spec-driven iterations.

**Rationale**: Ensures architectural integrity, prevents ad-hoc decisions, and maintains complete traceability from requirements to implementation.

### III. User Data Isolation and Security
Complete user data isolation and security through JWT authentication. Authentication MUST use Better Auth with stateless JWT tokens. All requests without valid JWT MUST return 401 Unauthorized. Database operations MUST always filter by authenticated user_id. Task ownership MUST be enforced on every CRUD operation. Every user action MUST be authenticated and user-scoped.

**Rationale**: Guarantees security boundaries between users, prevents data leakage, and enforces strict access controls mandated by multi-user requirements.

### IV. Reuse of Phase II Architecture
Reuse of Phase II architecture, APIs, and database without redesign. Backend: Existing FastAPI APIs from Phase II (no breaking changes). Database: Neon PostgreSQL (reuse Phase II schema). All changes MUST maintain backward compatibility with existing Phase II features.

**Rationale**: Ensures continuity with previous work, minimizes risk of introducing breaking changes, and maximizes reuse of proven architecture.

### V. Deterministic Tool Execution via MCP
Deterministic tool execution via MCP (no hallucinated actions). Protocol: Official MCP SDK only. AI agent MUST consistently select correct MCP tools. No hallucinated responses or unauthorized actions.

**Rationale**: Ensures reliable, predictable AI operations while preventing unauthorized or unsafe actions.

### VI. Stateless AI with Persistent External Memory
Stateless AI with persistent external memory. Chat sessions: Stateless (no in-memory conversation state). Chat history MUST be stored and retrievable per user. Clear separation between reasoning, tools, and data storage.

**Rationale**: Ensures scalability, reliability, and persistence of user data while maintaining stateless AI operations.

### VII. Agentic Dev Stack Workflow
The Agentic Dev Stack workflow MUST be followed: spec → plan → tasks → implement. Every feature MUST progress through these stages sequentially. Implementation cannot begin without completing tasks.md. No manual coding outside spec-driven workflow.

**Rationale**: Ensures rigorous planning, validation, and execution, preventing scope creep and ensuring quality delivery.

## Technology Stack & Constraints

### Locked Technology Stack
- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (stateless JWT tokens)
- **AI Layer**: OpenAI Agents SDK
- **Protocol**: Official MCP SDK only

### MCP Protocol Compliance
- All AI operations MUST use official MCP SDK
- AI agent MUST NOT directly manipulate databases
- Every user action MUST be authenticated and user-scoped
- Natural language input MUST be translated into structured tool calls
- Agent decisions MUST be explainable and traceable
- Chat history MUST be stored and retrievable per user

### API Contract Requirements
- API endpoints MUST exactly match the specified REST contract
- user_id MUST be included in API paths where required
- All database queries MUST filter by authenticated user_id
- No deviations from specified REST endpoints

### Authentication Flow
- Stateless JWT tokens issued by Better Auth
- BETTER_AUTH_SECRET shared between frontend and backend
- Missing or invalid JWT MUST return 401 Unauthorized
- User identity extracted from JWT for all operations

### Data Isolation Constraints
- Every database operation MUST include user_id filter
- Users can only view, create, update, and delete their own tasks
- No cross-user data access permitted
- No hardcoded data or test data that bypasses authentication

### Code Generation Constraints
- Zero manual code edits permitted
- All implementation must be generated by Claude Code
- All changes must be traceable to spec-driven iterations
- No ad-hoc modifications outside the spec-driven workflow

### Stateless AI Architecture
- Chat sessions: Stateless (no in-memory conversation state)
- External persistent memory for conversation history
- Clear separation between reasoning, tools, and data storage
- No hardcoded flows or predetermined conversation paths

## Agentic Dev Stack Workflow

### Workflow Stages
1. **Spec Creation**: User provides feature description → Claude generates spec.md with user stories, requirements, and success criteria
2. **Planning**: Claude generates plan.md with architecture, data models, API contracts, and implementation strategy
3. **Task Generation**: Claude generates tasks.md with testable, ordered tasks grouped by user story
4. **Implementation**: Claude executes tasks.md sequentially, implementing all code

### Documentation Requirements
- Every feature gets its own spec.md before implementation
- Public GitHub repository MUST contain:
  - Constitution (this file)
  - Full specs history in `specs/` directory
  - All generated code
  - CLAUDE.md files for agent guidance
- CLAUDE.md MUST follow the SpecKit Plus structure

### Success Criteria Tracking
- Users can manage todos entirely via natural language
- AI agent consistently selects correct MCP tools
- No hallucinated responses or unauthorized actions
- All Phase II features remain fully functional
- System is scalable and Kubernetes-ready
- Working multi-user web application with full CRUD for tasks
- Users can only view, create, update, and delete their own tasks
- Responsive frontend interface deployed on Vercel
- Backend API secured with JWT verification and user filtering
- Evidence of reusable intelligence usage (skills/subagents) for bonus consideration
- Zero manual code edits — all implementation traceable to spec-driven iterations
- Successful demonstration in <90-second video showing signup, login, task management, and isolation between users

## Governance

### Constitution Authority
This constitution supersedes all other practices and guidelines in the project. All development decisions MUST be evaluated against these principles. Any ambiguity MUST be resolved by prioritizing security, data isolation, and spec-driven workflow.

### Amendment Process
1. Propose amendment with clear justification and impact analysis
2. Document the change rationale, affected artifacts, and migration strategy
3. Verify that changes do not violate core security and isolation principles
4. Update constitution version following semantic versioning:
   - MAJOR: Backward-incompatible principle removals or redefinitions
   - MINOR: New principle added or material expansion of guidance
   - PATCH: Clarifications, wording fixes, non-semantic refinements
5. Propagate changes to dependent templates (plan, spec, tasks)
6. Maintain full amendment history in governance section

### Compliance Verification
- All PRs MUST verify compliance with constitution principles
- Complexity or deviations from principles MUST be explicitly justified
- Constitution Check in plan.md MUST be completed before implementation
- Any bypass of spec-driven workflow MUST be documented and approved

### Runtime Development Guidance
Use CLAUDE.md in the repository root for agent-specific runtime guidance. Constitution provides the principles; CLAUDE.md provides operational context.

**Version**: 1.1.0 | **Ratified**: 2026-01-03 | **Last Amended**: 2026-01-12
