# API Contracts: UI Polish & Visual Feedback Enhancements

**Feature**: UI Polish & Visual Feedback Enhancements for Todo Tasks Page
**Date**: 2026-01-17

## Overview

This feature is primarily a UI enhancement with no new API endpoints. It relies on existing task management APIs.

## Existing API Contracts Used

### Task Operations
- `GET /api/tasks` - Retrieve user's tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task (including completion status)
- `DELETE /api/tasks/{id}` - Delete task

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

### Task Card Props Interface
```typescript
interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: string, completed: boolean) => void;
  onEdit: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
}
```

### Toast Props Interface
```typescript
interface ToastProps {
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
}
```

### AddTaskModal Props Interface
```typescript
interface AddTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (taskData: { title: string; description?: string }) => void;
}
```

## UI Event Contracts

### Events Emitted by Components
- `taskCompleted(taskId: string)` - When a task is marked complete
- `taskCreated(task: Task)` - When a new task is created
- `taskUpdated(task: Task)` - When a task is modified
- `taskDeleted(taskId: string)` - When a task is deleted
- `toastRequested(message: string, type: string)` - When a toast notification is needed

## UI State Transitions

### Task Card States
- `pending` → `completed` (via checkbox interaction)
- `completed` → `pending` (via checkbox interaction)
- `idle` → `hovered` (via mouseover)
- `idle` → `focused` (via keyboard navigation)

### Modal States
- `closed` → `open` (via + FAB click)
- `open` → `closed` (via cancel, submit, or ESC key)