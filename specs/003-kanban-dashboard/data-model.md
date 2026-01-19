# Data Model: Kanban-Style Dashboard UI Evolution

**Feature**: Kanban-Style Dashboard UI Evolution for Todo Tasks Page (Doist-Inspired)
**Date**: 2026-01-17
**Modeler**: Claude Code

## Overview

This data model describes the UI-focused entities for the Kanban dashboard feature. Since this is primarily a visual enhancement feature without new backend functionality, the model focuses on the visual state representations and UI component properties.

## Key Entities

### 1. Kanban Board
**Description**: Represents the main dashboard layout with three columns for organizing tasks by status

**Properties**:
- `id`: Unique identifier for the board
- `columns`: Array of KanbanColumn objects representing the three sections
  - `Backlog`: Column for pending tasks
  - `Doing`: Column for active tasks
  - `Completed`: Column for finished tasks
- `layoutState`: Object containing UI-specific properties
  - `isResponsive`: Boolean for mobile/desktop layout adjustments
  - `columnWidth`: String for current column width calculation
  - `dragOverColumn`: String for drag-and-drop simulation state

**Validation Rules**:
- `columns` must have exactly 3 items
- Each column must have a unique identifier
- `id` must be unique within user's context

**State Transitions**:
- `desktop` → `mobile` (responsive layout adjustment)
- `loading` → `loaded` (board content populated)

### 2. Kanban Column
**Description**: Represents a single column in the Kanban board with specific task status

**Properties**:
- `id`: Unique identifier for the column (e.g., "backlog", "doing", "completed")
- `title`: String representing the column header (e.g., "Backlog", "Doing", "Completed")
- `statusFilter`: String indicating the task status this column displays
- `tasks`: Array of Task objects that belong to this column
- `isEmpty`: Boolean indicating if the column has no tasks
- `visualState`: Object containing UI-specific properties
  - `isDraggingOver`: Boolean for drag-and-drop simulation
  - `isHovered`: Boolean for hover state styling
  - `transitionState`: String for current transition phase

**Validation Rules**:
- `id` must be one of: "backlog", "doing", "completed"
- `statusFilter` must correspond to valid task status values
- `tasks` must be an array of valid Task objects

**State Transitions**:
- `empty` → `populated` (tasks added to column)
- `normal` → `drag-over` (simulated drag-and-drop interaction)

### 3. Kanban Task Card
**Description**: Enhanced task card component with Kanban-specific visual styling and interactions

**Properties**:
- `id`: Unique identifier for the task (inherited from base Task)
- `title`: String representing the task title (inherited from base Task)
- `description`: Optional string with task details (inherited from base Task)
- `completed`: Boolean indicating completion status (inherited from base Task)
- `createdAt`: Timestamp for task creation (inherited from base Task)
- `updatedAt`: Timestamp for last update (inherited from base Task)
- `visualState`: Object containing UI-specific properties
  - `isHovered`: Boolean for hover state styling
  - `isFocused`: Boolean for focus state styling
  - `transitionState`: String for current transition phase
  - `completionStyle`: Object with completion visual properties
    - `hasStrikethrough`: Boolean for line-through effect
    - `textColor`: String for text color in completion state
    - `accentColor`: String for optional accent color
  - `dragState`: Object for drag-and-drop simulation
    - `isDragging`: Boolean for current drag state
    - `dragOrigin`: String for original column location

**Validation Rules**:
- `title` must not be empty
- `completed` must be boolean
- `id` must be unique within user's tasks

**State Transitions**:
- `pending` → `completed` (when user marks task complete)
- `completed` → `pending` (when user unmarks task)
- `normal` → `dragging` (simulated drag state)

### 4. Insights Panel
**Description**: Sidebar component showing progress insights and statistics

**Properties**:
- `id`: Unique identifier for the insights panel
- `totalTasks`: Number representing the total count of tasks
- `completedTasks`: Number representing the completed task count
- `activeTasks`: Number representing the active task count
- `completionPercentage`: Number representing the percentage of completed tasks
- `weeklyStats`: Object containing weekly statistics
  - `tasksCompletedThisWeek`: Number of tasks completed in the current week
  - `tasksCreatedThisWeek`: Number of tasks created in the current week
- `isVisible`: Boolean controlling panel visibility
- `visualState`: Object containing UI-specific properties
  - `isExpanded`: Boolean for expanded/collapsed state
  - `transitionState`: String for current transition phase

**Validation Rules**:
- `totalTasks` must be >= 0
- `completedTasks` must be >= 0 and <= totalTasks
- `completionPercentage` must be between 0 and 100

**State Transitions**:
- `hidden` → `visible` (panel shown)
- `collapsed` → `expanded` (panel expanded)

### 5. Project Header
**Description**: Top navigation area with project name and menu controls

**Properties**:
- `id`: Unique identifier for the header
- `projectName`: String for the project title ("My Tasks" or "Todo Dashboard")
- `menuItems`: Array of objects representing available menu options
- `shareOptions`: Object containing sharing functionality options
- `insightsToggle`: Boolean for insights panel visibility toggle
- `visualState`: Object containing UI-specific properties
  - `isScrolled`: Boolean for scrolled state styling

**Validation Rules**:
- `projectName` must not be empty
- `menuItems` must be an array of valid menu item objects

**State Transitions**:
- `normal` → `scrolled` (header styling changes on scroll)

### 6. Add Task Modal
**Description**: Modal component for creating new tasks with column context

**Properties**:
- `isVisible`: Boolean controlling modal visibility
- `targetColumn`: String indicating which column the task should be added to
- `titleValue`: String for current title input value
- `descriptionValue`: String for current description input value
- `validationErrors`: Object containing field-specific validation errors
  - `title`: String error message if title validation fails
- `isSubmitting`: Boolean indicating if form is being submitted
- `submitButtonDisabled`: Boolean controlling submit button state

**Validation Rules**:
- `titleValue` must not be empty or whitespace-only
- `titleValue` must be ≤255 characters
- `descriptionValue` can be empty (optional)
- `targetColumn` must be one of: "backlog", "doing", "completed"

**State Transitions**:
- `hidden` → `visible` (when add task button clicked)
- `visible` → `hidden` (on cancel or successful submission)

## UI Component Properties

### 7. Empty State Per Column
**Description**: Properties controlling the empty state display for each column

**Properties**:
- `columnId`: String identifying which column this empty state belongs to
- `isVisible`: Boolean indicating if empty state should be shown
- `message`: String for the empty state message
- `ctaText`: String for the call-to-action button text
- `icon`: String representing the visual icon
- `isInteractive`: Boolean indicating if CTA button is clickable

**Validation Rules**:
- `ctaText` must not be empty
- `isVisible` is true only when column has no tasks
- `columnId` must match a valid column ID

**State Transitions**:
- `visible` → `hidden` (when first task is added to column)
- `hidden` → `visible` (when last task is moved from column)

### 8. Theme Configuration
**Description**: Properties controlling light/dark mode styling

**Properties**:
- `mode`: Enum ('light' | 'dark')
- `cardBgLight`: String for card background in light mode
- `cardBgDark`: String for card background in dark mode
- `textColorLight`: String for text in light mode
- `textColorDark`: String for text in dark mode
- `accentColor`: String for accent color (used in both modes)
- `columnBgLight`: String for column background in light mode
- `columnBgDark`: String for column background in dark mode

## Relationships

```
Kanban Board ←→ Kanban Column (contains multiple columns)
Kanban Column ←→ Kanban Task Card (contains multiple tasks)
Kanban Board ←→ Insights Panel (related information display)
Project Header ←→ Kanban Board (top-level navigation)
Add Task Modal ←→ Kanban Column (creates tasks for specific columns)
Empty State ←→ Kanban Column (displays when column is empty)
Kanban Board ←→ Theme Configuration (uses theme for styling)
```

## UI State Flow

1. **Initial State**: Kanban Board loads with three columns, tasks distributed by status
2. **Task Interaction**: Kanban Task Card state changes on completion
3. **Add Task**: Add Task Modal appears when column add button clicked
4. **Feedback**: Toast Notification appears for user actions
5. **Insights**: Insights Panel updates with current statistics
6. **Theme**: Theme Configuration applied throughout UI

## Accessibility Attributes

Each UI element includes appropriate ARIA attributes:
- `role` attributes for component identification (region, grid, row, gridcell)
- `aria-label` for unlabeled elements
- `aria-describedby` for additional context
- `tabindex` for keyboard navigation
- `aria-live` for dynamic content updates
- `aria-grabbed` and `aria-dropeffect` for drag-and-drop simulation
- `aria-expanded` for collapsible elements