# Implementation Plan: Kanban-Style Dashboard UI Evolution for Todo Tasks Page (Doist-Inspired)

**Branch**: `003-kanban-dashboard` | **Date**: 2026-01-17 | **Spec**: [specs/003-kanban-dashboard/spec.md](specs/003-kanban-dashboard/spec.md)
**Input**: Feature specification from `/specs/003-kanban-dashboard/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the current simple task list page into a professional Kanban-board dashboard interface with visual columns (Backlog / Doing / Completed), enhanced task cards, right-side progress insights panel, and seamless integration of the existing AI Todo Assistant. The implementation maintains full compatibility with existing Phase II & III functionality while adhering to spec-driven development principles.

## Technical Context

**Language/Version**: TypeScript 5.3, React 18.2, Next.js 14.0, Tailwind CSS 3.3
**Primary Dependencies**: Next.js (App Router), Tailwind CSS, React (hooks/state), existing TaskCard, Toast, AIChatPanel components
**Storage**: N/A (UI only changes)
**Testing**: Jest, React Testing Library (existing test suite)
**Target Platform**: Web browser (Chrome, Firefox, Safari, Edge) with responsive design
**Project Type**: Web application (frontend only changes)
**Performance Goals**: <200ms UI response time, 60fps animations, no performance degradation
**Constraints**: Must preserve existing structure (floating chat FAB, right-side AI chat panel, toast system), no new backend logic
**Scale/Scope**: Single-page application UI enhancements affecting only the /tasks page components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **AI-Native Design**: N/A (UI-only changes, no AI functionality modification)
- **Spec-Driven Development**: PASS - Following spec from `/specs/003-kanban-dashboard/spec.md`
- **User Data Isolation**: N/A (UI-only changes, no data access modifications)
- **Reuse of Phase II Architecture**: PASS - Maintaining existing backend APIs and database structure
- **Deterministic Tool Execution via MCP**: N/A (UI-only changes)
- **Stateless AI with Persistent External Memory**: N/A (UI-only changes, no AI memory modifications)
- **Agentic Dev Stack Workflow**: PASS - Following spec → plan → tasks → implement sequence

## Project Structure

### Documentation (this feature)

```text
specs/003-kanban-dashboard/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── KanbanBoard.tsx          # Main Kanban board layout with columns
│   │   ├── KanbanColumn.tsx         # Individual column component (Backlog/Doing/Completed)
│   │   ├── KanbanTaskCard.tsx       # Enhanced task card with Kanban-specific styling
│   │   ├── InsightsPanel.tsx        # Right sidebar with progress insights
│   │   ├── ProjectHeader.tsx        # Top header with project name and menu
│   │   ├── EmptyState.tsx           # Column-specific empty state
│   │   └── AddTaskModal.tsx         # Modal for adding tasks per column
│   ├── pages/
│   │   └── tasks/
│   │       └── page.tsx             # Main tasks page (Kanban dashboard)
│   ├── services/
│   │   └── tasks.ts                 # Existing task service (unchanged)
│   ├── styles/
│   │   └── globals.css              # Global styles with dark mode support
│   └── utils/
│       └── constants.ts             # UI constants (colors, transitions)
└── tests/
    ├── components/
    │   ├── KanbanBoard.test.tsx
    │   ├── KanbanColumn.test.tsx
    │   ├── KanbanTaskCard.test.tsx
    │   ├── InsightsPanel.test.tsx
    │   └── ProjectHeader.test.tsx
    └── pages/
        └── tasks/
            └── page.test.tsx
```

**Structure Decision**: Web application structure selected with frontend modifications only. Kanban dashboard components will be implemented with new Kanban-specific components while preserving existing functionality. All changes maintain existing architecture and component structure while adding Kanban board functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None identified | N/A | N/A |
