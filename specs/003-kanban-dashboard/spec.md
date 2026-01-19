# Feature Specification: Kanban-Style Dashboard UI Evolution for Todo Tasks Page (Doist-Inspired)

**Feature Branch**: `003-kanban-dashboard`
**Created**: 2026-01-17
**Status**: Draft
**Input**: User description: "Kanban-Style Dashboard UI Evolution for Todo Tasks Page (Doist-Inspired)

Target audience: Hackathon judges and Panaversity core team evaluating advanced visual presentation, intuitive task flow, and professional dashboard aesthetics in a spec-driven full-stack AI Todo application
Focus: Transform the /tasks page into a modern Kanban-board dashboard inspired by Doist/Todoist: columns for task stages (Backlog, Doing, Completed), card-based tasks with checkboxes + metadata, progress insights on the right, top project header, while integrating existing AI chatbot and maintaining simple English natural language support

Success criteria:
- Main area divided into 3 horizontal columns: Backlog (pending), Doing (active), Completed (done)
- Each task displayed as a clean card with:
  - Checkbox (□ / ✓) for completion
  - Title (with strikethrough + gray text when completed)
  - Optional metadata (e.g., due date placeholder, edit/delete icons)
  - Subtle hover effects, shadows, green accents for completed
- Right sidebar panel showing insights: progress bar (e.g., % complete), completed count, simple stats (this week / total)
- Top header with project name ("My Tasks" or "Todo Dashboard"), share/insights toggle, ellipsis menu
- Empty state per column or global: friendly message + "+ Add task" button
- Add task flow: + button opens modal/inline in relevant column
- Existing floating chat FAB or right panel for AI Todo Assistant (with welcome + example commands)
- Drag-and-drop reordering or real-time sync (Kanban simulation only via status)
- Full responsive (mobile stacks columns vertically), complete dark/light mode support, accessibility (ARIA, keyboard focus)

Constraints:
- Tech stack: Next.js (App Router), Tailwind CSS v3+, React (hooks/state for columns/filtering), existing components (TaskCard, Toast, AIChatPanel)
- All changes generated exclusively via Claude Code from refined specs; no manual coding
- Simulate Kanban via status-based grouping (pending → active → completed); NO real drag-and-drop or backend column persistence required (use simple filtering/grouping)
- Keep Basic Level scope: no real assignees, labels, priorities, recurring tasks, or multi-user features
- Integrate existing Phase III AI chatbot as right panel or floating bubble

Not building:
- Drag-and-drop reordering or real-time sync (Kanban simulation only via status)
- Advanced insights (detailed charts, burndown, team metrics) — keep simple progress bar + counts
- New backend models/endpoints for columns/assignees
- Third-party"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Kanban Board Layout & Column Structure (Priority: P1)

When a user visits the tasks page, they need to see their tasks organized in a clear Kanban-style board with three distinct columns: Backlog (pending tasks), Doing (active tasks), and Completed (finished tasks). This layout provides visual organization and clear status progression for task management.

**Why this priority**: This is the core transformation of the feature - changing from a simple list to a structured Kanban board dramatically improves task visualization and workflow management.

**Independent Test**: Can be fully tested by viewing the tasks page and verifying the three-column layout appears correctly with tasks properly distributed by status. Delivers clear value by organizing tasks into logical workflow stages.

**Acceptance Scenarios**:

1. **Given** user navigates to the tasks page, **When** page loads, **Then** three horizontal columns appear: "Backlog", "Doing", and "Completed"
2. **Given** user has tasks with different statuses, **When** page loads, **Then** tasks appear in the correct column based on their status (pending → Backlog, active → Doing, completed → Completed)

---

### User Story 2 - Enhanced Task Card Display (Priority: P1)

When a user views tasks in the Kanban columns, they need to see each task as a clean, interactive card with visual indicators for completion status, hover effects, and easy access to task actions like editing and deleting.

**Why this priority**: This enhances the user experience by providing rich visual feedback and making task interactions more intuitive and satisfying.

**Independent Test**: Can be fully tested by examining task cards in each column and verifying proper styling, hover effects, and visual indicators. Delivers value by improving the aesthetic and interactive experience.

**Acceptance Scenarios**:

1. **Given** user views a task card, **When** task is completed, **Then** card shows strikethrough text, gray text color, and green accent background
2. **Given** user hovers over a task card, **When** mouse enters card area, **Then** card lifts slightly with shadow and scale effect
3. **Given** user views any task card, **When** card is displayed, **Then** card shows checkbox, title, and action icons (edit/delete)

---

### User Story 3 - Right Sidebar Insights Panel (Priority: P2)

When a user works with their tasks, they need quick access to progress insights and statistics in a dedicated sidebar to understand their productivity and task completion rates.

**Why this priority**: Provides valuable context and motivation by showing progress metrics, helping users understand their task management effectiveness.

**Independent Test**: Can be fully tested by viewing the right sidebar and verifying progress bar, completed count, and other statistics display correctly. Delivers value by providing meaningful task analytics.

**Acceptance Scenarios**:

1. **Given** user is on the tasks page, **When** page loads, **Then** right sidebar shows progress bar with completion percentage
2. **Given** user has completed tasks, **When** viewing sidebar, **Then** completed task count and weekly statistics are displayed

---

### User Story 4 - Top Project Header & Navigation (Priority: P2)

When a user navigates the tasks page, they need a clear header with project name, share options, and menu controls to maintain orientation and access additional functionality.

**Why this priority**: Provides consistent navigation and context for the Kanban workspace, maintaining familiar interface patterns.

**Independent Test**: Can be fully tested by viewing the top header and verifying project name, menu items, and share options appear correctly. Delivers value by maintaining clear page structure.

**Acceptance Scenarios**:

1. **Given** user is on tasks page, **When** page loads, **Then** top header displays "My Tasks" or "Todo Dashboard" project name
2. **Given** user looks at header, **When** viewing controls, **Then** share/insights toggle and ellipsis menu are available

---

### User Story 5 - Column-Specific Empty States & Add Task Flow (Priority: P2)

When a user has no tasks in a particular column or wants to add tasks, they need clear empty state messages and intuitive add task functionality that works within the column context.

**Why this priority**: Improves the user experience when columns are empty and provides clear pathways for adding new tasks in the appropriate workflow stage.

**Independent Test**: Can be fully tested by viewing empty columns and verifying friendly messages with add task buttons. Delivers value by providing clear guidance for task creation.

**Acceptance Scenarios**:

1. **Given** a column has no tasks, **When** user views the column, **Then** friendly empty state message with "+ Add task" button appears
2. **Given** user clicks add task button in a column, **When** button is clicked, **Then** modal or inline form opens for adding a task in that context

---

### User Story 6 - AI Chatbot Integration (Priority: P2)

When a user needs help managing their tasks, they need to access the existing AI chatbot functionality seamlessly integrated with the new Kanban interface while maintaining simple English natural language support.

**Why this priority**: Preserves existing AI functionality while adapting it to the new Kanban context, maintaining the intelligent task assistance users expect.

**Independent Test**: Can be fully tested by interacting with the AI chatbot and verifying it works properly alongside the new Kanban interface. Delivers value by maintaining intelligent task management support.

**Acceptance Scenarios**:

1. **Given** user is on the Kanban tasks page, **When** AI chat bubble is clicked, **Then** chat panel opens with welcome message and example commands
2. **Given** user enters a natural language task command, **When** command is processed, **Then** appropriate action is taken on the Kanban board

---

### Edge Cases

- What happens when a user has many tasks in one column? Columns should scroll vertically without affecting other columns.
- How does the interface handle very long task titles? Text should wrap appropriately and not break the card layout.
- What happens during network interruptions? The Kanban board should maintain visual state and sync changes when connection resumes.
- How does the interface behave on small mobile screens? Columns should stack vertically with clear navigation between sections.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST divide main area into 3 horizontal columns: Backlog (pending), Doing (active), Completed (done)
- **FR-002**: System MUST display each task as a clean card with checkbox (□ / ✓) for completion status
- **FR-003**: System MUST apply strikethrough and gray text to completed task titles with optional green accent
- **FR-004**: System MUST implement subtle hover effects (shadow, scale) on task cards for visual feedback
- **FR-005**: System MUST show right sidebar panel with progress insights (progress bar, completed count, weekly stats)
- **FR-006**: System MUST display top header with project name ("My Tasks" or "Todo Dashboard") and menu controls
- **FR-007**: System MUST show column-specific empty states with "+ Add task" buttons when columns are empty
- **FR-008**: System MUST integrate existing AI chatbot as floating bubble or right panel with welcome message
- **FR-009**: System MUST maintain full responsiveness (columns stack vertically on mobile)
- **FR-010**: System MUST support complete dark/light mode functionality
- **FR-011**: System MUST maintain accessibility standards (ARIA labels, keyboard focus management)
- **FR-012**: System MUST simulate Kanban via status-based grouping without requiring backend column persistence
- **FR-013**: System MUST preserve existing AI chatbot functionality and simple English natural language support
- **FR-014**: System MUST provide intuitive add task functionality that works within column context
- **FR-015**: System MUST maintain task status synchronization across the Kanban board

### Key Entities

- **KanbanBoard**: Represents the main dashboard layout with three columns (Backlog, Doing, Completed) for organizing tasks by status
- **TaskCard**: Individual task representation with checkbox, title, metadata, and interactive elements (edit/delete)
- **Column**: Container for tasks of a specific status (pending/active/completed) with empty state handling
- **InsightsPanel**: Right sidebar component showing progress metrics, completion rates, and statistical data
- **ProjectHeader**: Top navigation area with project name, sharing options, and menu controls
- **AITaskAssistant**: Integrated AI functionality that can interpret natural language commands within the Kanban context

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Three-column Kanban layout appears consistently on tasks page with proper labeling (Backlog, Doing, Completed)
- **SC-002**: Task cards display with appropriate visual styling (checkbox, strikethrough for completed, hover effects) in 100% of cases
- **SC-003**: Right sidebar insights panel shows progress bar and statistics within 200ms of page load
- **SC-004**: Top project header displays consistently with proper navigation controls across all screen sizes
- **SC-005**: Empty states appear correctly in each column when no tasks are present with prominent "+ Add task" buttons
- **SC-006**: Interface is fully responsive and usable on mobile devices (columns stack vertically)
- **SC-007**: Dark/light mode toggle works correctly for all new UI elements without visual defects
- **SC-008**: All new UI elements meet accessibility standards (ARIA labels, keyboard navigation, focus management)
- **SC-009**: Existing AI chatbot functionality remains fully operational alongside new Kanban interface
- **SC-010**: 95% of users can successfully navigate and interact with the new Kanban board without confusion
- **SC-011**: Task status changes are reflected immediately across the Kanban board (completed tasks move to Completed column)
- **SC-012**: Add task functionality works seamlessly within each column context with appropriate status assignment
