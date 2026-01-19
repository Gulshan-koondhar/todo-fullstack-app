# Implementation Tasks: Kanban-Style Dashboard UI Evolution for Todo Tasks Page (Doist-Inspired)

**Feature**: Kanban-Style Dashboard UI Evolution for Todo Tasks Page (Doist-Inspired)
**Date**: 2026-01-17
**Status**: Ready for Implementation

## Phase 1: Setup & Environment

- [ ] T001 Verify project prerequisites (Node.js 18+, Next.js 14+, Tailwind CSS 3.3+)
- [ ] T002 Install any missing dependencies with `npm install`
- [ ] T003 Verify existing TaskCard, EmptyState, Toast, and AIChatPanel components are accessible

## Phase 2: Foundational Components

- [ ] T004 [P] Create frontend/components/KanbanBoard.tsx component file
- [ ] T005 [P] Create frontend/components/KanbanColumn.tsx component file
- [ ] T006 [P] Create frontend/components/KanbanTaskCard.tsx component file
- [ ] T007 [P] Create frontend/components/InsightsPanel.tsx component file
- [ ] T008 [P] Create frontend/components/ProjectHeader.tsx component file
- [ ] T009 [P] Create frontend/components/EmptyState.tsx component file
- [ ] T010 [P] Create frontend/components/AddTaskModal.tsx component file
- [ ] T011 [P] Create frontend/utils/constants.ts for UI constants (colors, transitions)
- [ ] T012 [P] Update frontend/styles/globals.css with dark mode configurations

## Phase 3: [US1] Kanban Board Layout & Column Structure

**Goal**: Implement the main Kanban board layout with three horizontal columns for Backlog, Doing, and Completed tasks

**Independent Test**: View the tasks page and verify that three horizontal columns appear with proper labeling (Backlog, Doing, Completed) and tasks are distributed by status

**Tasks**:

- [ ] T013 [US1] Create KanbanBoard.tsx with CSS Grid layout for three columns
- [ ] T014 [US1] Implement responsive behavior: stack columns vertically on mobile screens (<768px)
- [ ] T015 [US1] Add proper gap spacing between columns (gap-4) with minimum column widths
- [ ] T016 [US1] Create KanbanColumn.tsx components for Backlog, Doing, and Completed columns
- [ ] T017 [US1] Implement column headers with proper labeling ("Backlog", "Doing", "Completed")
- [ ] T018 [US1] Add drop zone functionality for simulated drag-and-drop
- [ ] T019 [US1] Test column layout on different screen sizes
- [ ] T020 [US1] Ensure columns work properly in dark mode with dark: variants

## Phase 4: [US2] Enhanced Task Card Display

**Goal**: Enhance task cards with visual indicators for completion status, hover effects, and easy access to task actions

**Independent Test**: Examine task cards in each column and verify proper styling, hover effects, and visual indicators - strikethrough for completed tasks, gray text, green accent, hover lift/scale effects

**Tasks**:

- [ ] T021 [US2] Update KanbanTaskCard.tsx to apply strikethrough effect when task.completed is true
- [ ] T022 [US2] Update KanbanTaskCard.tsx to apply gray text styling when task.completed is true
- [ ] T023 [US2] Update KanbanTaskCard.tsx to apply green accent background when task.completed is true
- [ ] T024 [US2] Add subtle shadow and hover effects to KanbanTaskCard (hover:shadow-lg hover:scale-[1.02])
- [ ] T025 [US2] Add smooth transitions to KanbanTaskCard (transition-all duration-300)
- [ ] T026 [US2] Implement visual state transitions when checkbox is toggled
- [ ] T027 [US2] Add checkbox (□ / ✓) with proper completion handling
- [ ] T028 [US2] Add edit & delete icons/buttons to KanbanTaskCard
- [ ] T029 [US2] Test hover effects work on different screen sizes
- [ ] T030 [US2] Ensure hover effects work properly in dark mode with dark: variants
- [ ] T031 [US2] Add accessibility attributes for keyboard navigation

## Phase 5: [US3] Right Sidebar Insights Panel

**Goal**: Create a right sidebar panel showing progress insights and statistics

**Independent Test**: View the right sidebar and verify progress bar, completed count, and other statistics display correctly

**Tasks**:

- [ ] T032 [US3] Create InsightsPanel.tsx component with progress bar implementation
- [ ] T033 [US3] Calculate and display completion percentage (completedTasks / totalTasks \* 100)
- [ ] T034 [US3] Display completed task count and total task count
- [ ] T035 [US3] Add simple "This week" stats placeholder
- [ ] T036 [US3] Implement toggleable or persistent behavior on desktop
- [ ] T037 [US3] Use Tailwind for clean styling (green progress, neutral text)
- [ ] T038 [US3] Connect InsightsPanel to task data for real-time updates
- [ ] T039 [US3] Ensure proper positioning with new layout
- [ ] T040 [US3] Test insights panel in both light and dark modes
- [ ] T041 [US3] Add smooth entry/exit animations to InsightsPanel component

## Phase 6: [US4] Top Project Header & Navigation

**Goal**: Create a clear header with project name, share options, and menu controls

**Independent Test**: View the top header and verify project name, menu items, and share options appear correctly

**Tasks**:

- [ ] T042 [US4] Create ProjectHeader.tsx component with project name display
- [ ] T043 [US4] Implement "My Tasks" or "Todo Dashboard" project name display
- [ ] T044 [US4] Add ellipsis menu placeholder with dropdown functionality
- [ ] T045 [US4] Add share/insights toggle functionality
- [ ] T046 [US4] Implement proper positioning and styling
- [ ] T047 [US4] Ensure header works properly in responsive layouts
- [ ] T048 [US4] Add accessibility attributes for navigation
- [ ] T049 [US4] Test header in both light and dark modes

## Phase 7: [US5] Column-Specific Empty States & Add Task Flow

**Goal**: Implement empty states per column with intuitive add task functionality

**Independent Test**: View empty columns and verify friendly messages with "+ Add task" buttons appear correctly

**Tasks**:

- [ ] T050 [US5] Update EmptyState.tsx to support column-specific messages
- [ ] T051 [US5] Create per-column messages: "No tasks in [status] yet"
- [ ] T052 [US5] Add prominent "+ Add task" button to each column's empty state
- [ ] T053 [US5] Maintain clipboard icon with appropriate sizing
- [ ] T054 [US5] Add subtle animation to draw attention to add button
- [ ] T055 [US5] Update AddTaskModal.tsx to support column context
- [ ] T056 [US5] Pass column context to modal to set initial status appropriately
- [ ] T057 [US5] Add "+ Add task" button to each column footer
- [ ] T058 [US5] Handle modal opening from column-specific add buttons
- [ ] T059 [US5] Test empty states work in both light and dark modes

## Phase 8: [US6] AI Chat Integration Continuity

**Goal**: Preserve existing AI chat functionality with seamless integration

**Independent Test**: Interact with the AI chatbot and verify it works properly alongside the new Kanban interface

**Tasks**:

- [ ] T060 [US6] Verify existing floating chat bubble FAB remains functional
- [ ] T061 [US6] Ensure new Kanban layout doesn't interfere with chat overlay
- [ ] T062 [US6] Maintain same AI assistant functionality and welcome message
- [ ] T063 [US6] Test proper z-index stacking with new components
- [ ] T064 [US6] Ensure AI chat FAB remains visible and accessible
- [ ] T065 [US6] Verify AI chat functionality works in both light and dark modes
- [ ] T066 [US6] Test that AI commands work properly with Kanban board

## Phase 9: Cross-Cutting Concerns

- [ ] T067 Add dark mode variants (dark:) to all new UI elements in KanbanBoard
- [ ] T068 Add dark mode variants (dark:) to all new UI elements in KanbanColumn
- [ ] T069 Add dark mode variants (dark:) to all new UI elements in KanbanTaskCard
- [ ] T070 Add dark mode variants (dark:) to all new UI elements in InsightsPanel
- [ ] T071 Add dark mode variants (dark:) to all new UI elements in ProjectHeader
- [ ] T072 Add dark mode variants (dark:) to all new UI elements in EmptyState
- [ ] T073 Add dark mode variants (dark:) to all new UI elements in AddTaskModal
- [ ] T074 Add proper ARIA labels to all interactive elements (checkbox, edit/delete, FABs)
- [ ] T075 Test responsive behavior on mobile devices (touch targets ≥44px)
- [ ] T076 Verify no horizontal scroll on narrow screens
- [ ] T077 Ensure AI chat panel still overlays correctly with new UI changes
- [ ] T078 Verify toast works with both UI actions and AI commands
- [ ] T079 Test all UI elements in both light and dark mode for visual defects
- [ ] T080 Validate all accessibility features are functional (keyboard nav, screen readers)
- [ ] T081 Update existing tests to account for new UI changes
- [ ] T082 Run full application test to ensure no regressions in existing functionality

## Dependencies

**User Story Dependency Graph**:

- US1 (Kanban Board Layout) - Independent, can be developed first
- US2 (Task Card Enhancement) - Depends on US1 (needs columns to display cards)
- US3 (Insights Panel) - Independent, can be developed in parallel with US1/US2
- US4 (Project Header) - Independent, can be developed in parallel with others
- US5 (Empty States & Add Task) - Depends on US1/US2 (needs working board and cards)
- US6 (AI Chat Integration) - Independent, can be developed in parallel with others

## Parallel Execution Examples

**Parallel Opportunities**:

- US1 and US3 can be developed in parallel (different components: KanbanBoard and InsightsPanel)
- US2 and US4 can be developed in parallel (different components: KanbanTaskCard and ProjectHeader)
- US5 and US6 can be developed in parallel (different components: EmptyState/AddTaskModal and AIChatPanel)

## Implementation Strategy

**MVP Scope**: Focus on US1 (Kanban Board Layout) and US2 (Task Card Enhancement) for initial deliverable

**Incremental Delivery**:

1. Phase 1-2: Setup foundational components
2. Phase 3-4: Core Kanban functionality (layout and task cards)
3. Phase 5-6: Enhanced features (insights and header)
4. Phase 7-8: Add task flow and AI integration
5. Phase 9: Polish and integration
