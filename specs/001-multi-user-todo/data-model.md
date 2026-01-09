# Data Model: Secure Multi-User Todo Application

**Feature**: 001-multi-user-todo
**Created**: 2026-01-03
**Purpose**: Define entity schemas, relationships, and validation rules for User and Task entities

## Entity: User

Represents a person with an account who can manage their own tasks. Users are the owners of all tasks they create.

### Attributes

| Field Name | Type | Constraints | Description | Index |
|------------|------|-------------|-------------|--------|
| `id` | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the user | PK |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (used for login) | UNIQUE INDEX |
| `password_hash` | VARCHAR(255) | NOT NULL | Securely hashed password (bcrypt/argon2) | - |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp | - |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP, ON UPDATE | Last update timestamp | - |

### Validation Rules

- **Email**: Must be a valid email format (regex pattern). Case-insensitive unique check.
- **Password**: Minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 number, 1 special character.
- **Password Hash**: Never store plain text. Use bcrypt or argon2 with cost factor ≥ 10.

### Relationships

- **One-to-Many with Task**: A User can have zero or more Tasks. When a User is deleted, their Tasks are cascade deleted (or soft-delete with `deleted_at` flag).

### Example

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X.wKvPq4Y7J5WqW",
  "created_at": "2026-01-03T10:30:00Z",
  "updated_at": "2026-01-03T10:30:00Z"
}
```

---

## Entity: Task

Represents an individual todo item owned by a specific User. Tasks can only be accessed and modified by their owning user.

### Attributes

| Field Name | Type | Constraints | Description | Index |
|------------|------|-------------|-------------|--------|
| `id` | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the task | PK |
| `title` | VARCHAR(200) | NOT NULL | Task title (required) | - |
| `description` | VARCHAR(1000) | NULLABLE | Task description (optional) | - |
| `completed` | BOOLEAN | DEFAULT FALSE | Task completion status | - |
| `user_id` | UUID | FOREIGN KEY → users.id, NOT NULL | User who owns this task | INDEX `idx_user_id` |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Task creation timestamp | INDEX `idx_created_at` |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP, ON UPDATE | Last update timestamp | - |

### Validation Rules

- **Title**: Required, 1-200 characters. Cannot be empty or whitespace-only. Trim leading/trailing whitespace.
- **Description**: Optional, 0-1000 characters. Trim leading/trailing whitespace.
- **Completed**: Boolean (true/false). Default is false (active).
- **User ID**: Must reference a valid User record. Foreign key constraint enforced.

### Relationships

- **Many-to-One with User**: A Task belongs to exactly one User. A User can have zero or more Tasks.

### Indexes

- **Primary Key**: `id` (UUID) for fast lookups and joins
- **Foreign Key Index**: `user_id` for efficient user task queries (WHERE user_id = X)
- **Timestamp Index**: `created_at` for sorting tasks by creation date (ORDER BY created_at DESC)

### Security Constraints

- **Data Isolation**: All queries MUST include `WHERE user_id = <authenticated_user_id>`
- **Ownership Verification**: Before UPDATE/DELETE, verify `task.user_id == authenticated_user_id`
- **Enumeration Protection**: Return 404 if task not found (don't reveal whether task exists or user owns it)

### State Transitions

```
┌─────────────┐
│  Created    │
│ (active)    │
└──────┬──────┘
       │
       │ mark as complete
       │
┌──────▼──────┐
│ Completed   │ ◄── mark as incomplete
│             │
└─────────────┘
```

- **Active → Completed**: User marks task as complete (completion toggled, visual feedback)
- **Completed → Active**: User marks task as incomplete (uncheck completion)
- **Completed**: Task displays strikethrough and color change in UI
- **Deleted**: Task permanently removed from database (cannot be recovered)

### Example

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440111",
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "completed": false,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-01-03T11:00:00Z",
  "updated_at": "2026-01-03T11:00:00Z"
}
```

---

## Database Schema (SQL)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster email lookups during authentication
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for user task queries (CRITICAL FOR DATA ISOLATION)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for sorting tasks by creation date
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Composite index for user tasks sorted by creation date (optimizes common query)
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

---

## Entity Relationship Diagram

```
┌─────────────────────────────┐
│          USERS             │
├─────────────────────────────┤
│  id (PK)                 │
│  email (UNIQUE)            │
│  password_hash             │
│  created_at                │
│  updated_at                │
└──────────────┬──────────────┘
               │ 1
               │
               │ N
┌──────────────▼──────────────┐
│          TASKS             │
├─────────────────────────────┤
│  id (PK)                 │
│  title                    │
│  description               │
│  completed                │
│  user_id (FK) ──────────┘
│  created_at                │
│  updated_at                │
└─────────────────────────────┘
```

**Relationship**: One User can have zero or more Tasks. A Task belongs to exactly one User.

---

## Query Patterns (Security Enforcement)

All database operations MUST filter by authenticated user_id:

### Create Task
```sql
INSERT INTO tasks (id, title, description, completed, user_id, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?);
```
- **Security**: `user_id` is extracted from JWT and injected into INSERT

### Read User's Tasks
```sql
SELECT * FROM tasks
WHERE user_id = ?
ORDER BY created_at DESC;
```
- **Security**: `user_id` filter enforces data isolation
- **Optimization**: Uses `idx_tasks_user_created` composite index

### Read Single Task
```sql
SELECT * FROM tasks
WHERE id = ? AND user_id = ?;
```
- **Security**: Double check: task.id AND user_id
- **Result**: 404 Not Found if task doesn't exist or user doesn't own it

### Update Task
```sql
UPDATE tasks
SET title = ?, description = ?, completed = ?, updated_at = ?
WHERE id = ? AND user_id = ?;
```
- **Security**: Only update if user owns the task
- **Return**: 404 Not Found if task not found or not owned

### Delete Task
```sql
DELETE FROM tasks
WHERE id = ? AND user_id = ?;
```
- **Security**: Only delete if user owns the task
- **Return**: 404 Not Found if task not found or not owned

### Count User's Tasks
```sql
SELECT COUNT(*) FROM tasks
WHERE user_id = ?;
```
- **Security**: Filter by user_id

---

## Data Access Patterns

### Frontend → Backend Flow

1. **User Action**: User clicks "Add Task" in UI
2. **Frontend**: Opens modal, user enters title/description
3. **Frontend**: Validates form (Zod schema)
4. **Frontend**: API client POSTs to `/api/tasks` with JWT in `Authorization: Bearer <token>` header
5. **Backend**: JWT verification middleware extracts `user_id` from token
6. **Backend**: Task endpoint validates, creates task with injected `user_id`
7. **Backend**: Returns created task JSON
8. **Frontend**: Optimistically adds task to list + shows toast notification
9. **Database**: Task stored with `user_id` foreign key enforcing ownership

### Security Enforcement Layers

1. **JWT Middleware**: Verifies token signature and extracts user_id (returns 401 if invalid/missing)
2. **Route Parameters**: Endpoint paths include `/users/{user_id}` for explicit scoping
3. **Business Logic**: Check `task.user_id == authenticated_user_id` before UPDATE/DELETE
4. **Database Queries**: All queries include `WHERE user_id = <extracted_user_id>`
5. **Response Handling**: Return 404 Not Found for non-owned tasks (don't reveal existence)

---

## Edge Cases and Constraints

### Task Ownership
- **Cross-User Access**: User A cannot access User B's tasks (404/403)
- **Task Transfer**: Tasks cannot be transferred between users (not in scope)
- **Orphaned Tasks**: Not possible due to FK constraint with ON DELETE CASCADE

### Data Integrity
- **Empty Tasks**: Title cannot be empty or whitespace-only
- **Long Titles**: Truncate to 200 characters if user exceeds limit
- **Concurrent Edits**: Last write wins (no conflict resolution for Phase II)
- **Soft Delete**: Not implemented - permanent deletion only

### Performance Considerations
- **100+ Tasks**: Indexes ensure <2s load time for users with 100 tasks
- **Pagination**: Not implemented for Phase II (load all user tasks)
- **Full Text Search**: Not implemented (requires additional indexes)

### Future Extensibility

The data model supports future enhancements without schema migration for many features:
- **Task Priorities**: Add `priority` column (ENUM: low, medium, high)
- **Tags/Labels**: Add separate `tags` table with `task_tags` junction table
- **Due Dates**: Add `due_date` column (TIMESTAMP or DATE)
- **Recurring Tasks**: Add `recurrence_rule` column (JSONB for flexibility)
- **Task Notes**: Add separate `task_notes` table with one-to-many relationship
- **Subtasks**: Add `parent_task_id` FK to tasks table for hierarchical tasks

---

## Summary

- **2 Entities**: User (account) and Task (todo item)
- **One Relationship**: User (1) → (N) Task (ownership enforced via foreign key)
- **Security**: All queries MUST filter by `user_id` for 100% data isolation
- **Validation**: Email format, password strength, title length (200 chars), description length (1000 chars)
- **Indexes**: Optimized for user task queries and sorting
- **State Transitions**: Simple active/completed toggle
- **Extensibility**: Schema supports future features without breaking changes
