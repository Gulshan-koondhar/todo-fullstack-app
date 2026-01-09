# Data Contracts: Request/Response Schemas

**Feature**: 001-multi-user-todo
**Created**: 2026-01-03
**Purpose**: Define TypeScript and Python schemas for API requests and responses

## Overview

Type-safe schemas ensure consistency between frontend (TypeScript) and backend (Python/Pydantic). These contracts prevent data validation issues and provide clear API documentation.

**Frontend**: TypeScript + Zod schemas for runtime validation
**Backend**: Pydantic models for request/response validation

---

## Task Schema

### TypeScript Types (Frontend)

```typescript
// Base task fields
interface BaseTask {
  id: string; // UUID
  title: string; // 1-200 characters
  description: string | null; // 0-1000 characters, optional
  completed: boolean;
  user_id: string; // UUID (owner's ID)
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

// Full task (with all fields)
interface Task extends BaseTask {}

// Task creation request (subset of fields)
interface CreateTaskRequest {
  title: string; // 1-200 characters, required
  description?: string; // 0-1000 characters, optional
}

// Task update request (subset of fields, all optional)
interface UpdateTaskRequest {
  title?: string; // 1-200 characters, optional
  description?: string; // 0-1000 characters, optional
  completed?: boolean; // optional
}

// Task list response
interface TasksListResponse {
  tasks: Task[];
  count: number;
}

// Single task response
interface TaskResponse {
  task: Task;
}
```

### Zod Schemas (Frontend Runtime Validation)

```typescript
import { z } from 'zod';

// Base task schema
export const BaseTaskSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1).max(200),
  description: z.string().max(1000).nullable(),
  completed: z.boolean(),
  user_id: z.string().uuid(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

// Task type (inferred from schema)
export type Task = z.infer<typeof BaseTaskSchema>;

// Create task request schema
export const CreateTaskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .trim()
    .refine(val => val.trim().length > 0, 'Title cannot be empty'),
  description: z.string()
    .max(1000, 'Description must be less than 1000 characters')
    .optional()
    .nullable(),
});

export type CreateTaskRequest = z.infer<typeof CreateTaskSchema>;

// Update task request schema
export const UpdateTaskSchema = z.object({
  title: z.string()
    .min(1, 'Title must be at least 1 character')
    .max(200, 'Title must be less than 200 characters')
    .trim()
    .refine(val => val.trim().length > 0, 'Title cannot be empty')
    .optional(),
  description: z.string()
    .max(1000, 'Description must be less than 1000 characters')
    .optional()
    .nullable(),
  completed: z.boolean().optional(),
});

export type UpdateTaskRequest = z.infer<typeof UpdateTaskSchema>;

// Tasks list response schema
export const TasksListResponseSchema = z.object({
  tasks: z.array(BaseTaskSchema),
  count: z.number().int().nonnegative(),
});

export type TasksListResponse = z.infer<typeof TasksListResponseSchema>;

// Task response schema
export const TaskResponseSchema = z.object({
  task: BaseTaskSchema,
});

export type TaskResponse = z.infer<typeof TaskResponseSchema>;
```

### Pydantic Models (Backend)

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class BaseTaskModel(BaseModel):
    """Base task model with common fields."""

    id: UUID
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440111",
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API docs",
                "completed": False,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2026-01-03T11:00:00Z",
                "updated_at": "2026-01-03T11:00:00Z",
            }
        }
    }


class CreateTaskRequest(BaseModel):
    """Request schema for creating a task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator('title')
    @classmethod
    def title_not_whitespace(cls, v: str) -> str:
        """Validate title is not just whitespace."""
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API docs",
            }
        }
    }


class UpdateTaskRequest(BaseModel):
    """Request schema for updating a task (partial updates allowed)."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def title_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not just whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip() if v else v

    model_config = {
        "json_schema_extra": {
            "example": {
                "completed": True,
            }
        }
    }


class TasksListResponse(BaseModel):
    """Response schema for listing user's tasks."""

    tasks: list[BaseTaskModel]
    count: int = Field(..., ge=0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "tasks": [
                    {
                        "id": "660e8400-e29b-41d4-a716-446655440111",
                        "title": "Complete project documentation",
                        "description": "Write comprehensive README and API docs",
                        "completed": False,
                        "user_id": "550e8400-e29b-41d4-a716-446655440000",
                        "created_at": "2026-01-03T11:00:00Z",
                        "updated_at": "2026-01-03T11:00:00Z",
                    }
                ],
                "count": 1,
            }
        }
    }


class TaskResponse(BaseModel):
    """Response schema for single task operations."""

    task: BaseTaskModel

    model_config = {
        "json_schema_extra": {
            "example": {
                "task": {
                    "id": "660e8400-e29b-41d4-a716-446655440111",
                    "title": "Complete project documentation",
                    "description": "Write comprehensive README and API docs",
                    "completed": False,
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "created_at": "2026-01-03T11:00:00Z",
                    "updated_at": "2026-01-03T11:00:00Z",
                }
            }
        }
    }
```

---

## User Schema

### TypeScript Types (Frontend)

```typescript
// Base user fields
interface BaseUser {
  id: string; // UUID
  email: string; // Valid email format
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

// Full user (without password hash - never exposed to frontend)
interface User extends BaseUser {}

// User creation request (for signup via Better Auth)
interface CreateUserRequest {
  email: string; // Valid email format
  password: string; // Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special
}

// User response (without password hash)
interface UserResponse {
  user: User;
}
```

### Zod Schemas (Frontend Runtime Validation)

```typescript
import { z } from 'zod';

// Base user schema
export const BaseUserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export type User = z.infer<typeof BaseUserSchema>;

// Create user request schema
export const CreateUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least 1 uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least 1 lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least 1 number')
    .regex(/[^A-Za-z0-9]/, 'Password must contain at least 1 special character'),
});

export type CreateUserRequest = z.infer<typeof CreateUserSchema>;

// User response schema
export const UserResponseSchema = z.object({
  user: BaseUserSchema,
});

export type UserResponse = z.infer<typeof UserResponseSchema>;
```

### Pydantic Models (Backend)

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class BaseUserModel(BaseModel):
    """Base user model (password hash never exposed)."""

    id: UUID
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-01-03T10:00:00Z",
                "updated_at": "2026-01-03T10:00:00Z",
            }
        }
    }


class CreateUserRequest(BaseModel):
    """Request schema for creating a user account."""

    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least 1 uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least 1 lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least 1 number')
        if not any(not c.isalnum() for c in v):
            raise ValueError('Password must contain at least 1 special character')
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!",
            }
        }
    }


class UserResponse(BaseModel):
    """Response schema for user operations (password hash not included)."""

    user: BaseUserModel

    model_config = {
        "json_schema_extra": {
            "example": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "created_at": "2026-01-03T10:00:00Z",
                    "updated_at": "2026-01-03T10:00:00Z",
                }
            }
        }
    }
```

---

## Error Response Schema

### TypeScript Types (Frontend)

```typescript
// Error response
interface ErrorResponse {
  error: string;
  details?: {
    [key: string]: string;
  };
}
```

### Zod Schema (Frontend Runtime Validation)

```typescript
import { z } from 'zod';

export const ErrorResponseSchema = z.object({
  error: z.string(),
  details: z.record(z.string()).optional(),
});

export type ErrorResponse = z.infer<typeof ErrorResponseSchema>;
```

### Pydantic Model (Backend)

```python
from pydantic import BaseModel
from typing import Optional, Dict


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    error: str
    details: Optional[Dict[str, str]] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "Invalid request body",
                "details": {
                    "title": "Title is required and must be 1-200 characters"
                }
            }
        }
    }


# Common error responses
UNAUTHORIZED_RESPONSE = ErrorResponse(error="Authentication required")
FORBIDDEN_RESPONSE = ErrorResponse(error="Access denied: user_id mismatch")
NOT_FOUND_RESPONSE = ErrorResponse(error="Task not found")
BAD_REQUEST_RESPONSE = ErrorResponse(error="Invalid request body")
CONFLICT_RESPONSE = ErrorResponse(error="Email already exists")
INTERNAL_ERROR_RESPONSE = ErrorResponse(error="Internal server error")
```

---

## Query Parameter Schemas

### TypeScript Types (Frontend)

```typescript
// List tasks query parameters
interface ListTasksParams {
  completed?: boolean; // Optional filter by completion status
}
```

### Zod Schema (Frontend Runtime Validation)

```typescript
import { z } from 'zod';

export const ListTasksParamsSchema = z.object({
  completed: z.coerce.boolean().optional(),
});

export type ListTasksParams = z.infer<typeof ListTasksParamsSchema>;
```

---

## Summary

- **Task Schemas**: BaseTask, CreateTaskRequest, UpdateTaskRequest, TasksListResponse
- **User Schemas**: BaseUser, CreateUserRequest (password validation), UserResponse
- **Error Schema**: Consistent error response format
- **Type Safety**: TypeScript types + Zod validation (frontend), Pydantic models (backend)
- **Validation**: Email format, password strength, title/description length, UUID format, datetime format
- **Consistency**: Frontend and backend use identical validation rules
