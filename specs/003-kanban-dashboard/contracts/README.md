# API Contracts: Kanban-Style Dashboard UI Evolution

**Feature**: Kanban-Style Dashboard UI Evolution for Todo Tasks Page (Doist-Inspired)
**Date**: 2026-01-17

## Overview

This feature is primarily a UI enhancement with no new API endpoints. It relies on existing task management APIs and organizes tasks into Kanban-style columns using client-side filtering.

## Existing API Contracts Used

### Task Operations
- `GET /api/tasks` - Retrieve user's tasks (unchanged)
- `POST /api/tasks` - Create new task (unchanged)
- `PUT /api/tasks/{id}` - Update task (including completion status) (unchanged)
- `DELETE /api/tasks/{id}` - Delete task (unchanged)

### Expected Request/Response Formats

#### Task Object
```json
{
  "id": "string",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "user_id": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Create Task Request
```json
{
  "title": "string (required)",
  "description": "string (optional)"
}
```

#### Update Task Request
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

## UI State Contracts

### Kanban Board Props Interface
```typescript
interface KanbanBoardProps {
  tasks: Task[];
  onTaskUpdate: (taskId: string, updates: Partial<Task>) => void;
  onTaskCreate: (taskData: CreateTaskRequest) => void;
  onTaskDelete: (taskId: string) => void;
}
```

### Kanban Column Props Interface
```typescript
interface KanbanColumnProps {
  title: string;
  status: 'backlog' | 'doing' | 'completed';
  tasks: Task[];
  onTaskMove?: (taskId: string, newStatus: string) => void;
  onTaskCreate: (taskData: CreateTaskRequest) => void;
}
```

### Insights Panel Props Interface
```typescript
interface InsightsPanelProps {
  tasks: Task[];
  completedCount: number;
  totalCount: number;
  completionPercentage: number;
}
```

### Project Header Props Interface
```typescript
interface ProjectHeaderProps {
  projectName: string;
  onMenuToggle?: () => void;
  onShareToggle?: () => void;
}
```

## UI Event Contracts

### Events Emitted by Components
- `taskCreated(task: Task)` - When a new task is created
- `taskUpdated(task: Task)` - When a task is modified
- `taskDeleted(taskId: string)` - When a task is deleted
- `taskMoved(taskId: string, newColumn: string)` - When task is moved between columns
- `columnAddTask(column: string)` - When add task is requested for specific column

## UI State Transitions

### Task Card States
- `pending` → `completed` (via checkbox interaction)
- `completed` → `pending` (via checkbox interaction)
- `idle` → `hovered` (via mouseover)
- `idle` → `focused` (via keyboard navigation)

### Column States
- `empty` → `populated` (when tasks added)
- `normal` → `drag-over` (simulated drag-and-drop state)

### Board States
- `loading` → `loaded` (when tasks are fetched)
- `desktop` → `mobile` (responsive layout change)