# API Specification: Secure Multi-User Todo Application

**Feature**: 001-multi-user-todo
**Created**: 2026-01-03
**Purpose**: Define REST API endpoints, request/response schemas, and security requirements

## Overview

RESTful API with JWT authentication. All protected endpoints require `Authorization: Bearer <jwt_token>` header. Endpoints follow the pattern `/api/users/{user_id}/tasks` for explicit scoping and ownership verification.

**Base URL**: `http://localhost:8000/api/v1` (development), `https://<backend-domain>/api/v1` (production)

**Authentication**:
- Method: Stateless JWT tokens (issued by Better Auth on frontend)
- Header: `Authorization: Bearer <jwt_token>`
- Token Validation: Backend middleware verifies JWT signature and extracts `user_id`
- Unauthenticated Response: 401 Unauthorized (no token, invalid token, expired token)

**Security Enforcement**:
- All task queries filtered by `user_id` extracted from JWT
- Ownership verified before task UPDATE/DELETE operations
- Cross-user access returns 404 Not Found (not 403 to prevent enumeration)

**Response Format**:
- Success: 200 OK (or 201 Created for POST)
- Error: 4xx/5xx with JSON body: `{"error": "error message"}`

---

## Task Endpoints

### 1. List User's Tasks

**Endpoint**: `GET /api/v1/users/{user_id}/tasks`

**Authentication**: Required (JWT)

**Description**: Retrieve all tasks belonging to the authenticated user. Tasks are sorted by creation date (newest first).

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID | User ID (must match authenticated user_id from JWT) |

**Query Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `completed` | boolean | null | Optional filter by completion status (`true` for completed only, `false` for active only) |

**Response Codes**:

| Code | Description |
|------|-------------|
| 200 | Success - returns array of tasks |
| 401 | Unauthorized - missing or invalid JWT |
| 403 | Forbidden - `user_id` in path doesn't match authenticated user |
| 500 | Internal server error |

**Response Body (200 OK)**:

```json
{
  "tasks": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440111",
      "title": "Complete project documentation",
      "description": "Write comprehensive README and API docs",
      "completed": false,
      "user_id": "550e8400-e29b-41d4-a716-4466554400000",
      "created_at": "2026-01-03T11:00:00Z",
      "updated_at": "2026-01-03T11:00:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440112",
      "title": "Review pull requests",
      "description": null,
      "completed": true,
      "user_id": "550e8400-e29b-41d4-a716-4466554400000",
      "created_at": "2026-01-03T10:30:00Z",
      "updated_at": "2026-01-03T10:35:00Z"
    }
  ],
  "count": 2
}
```

**Response Body (401 Unauthorized)**:

```json
{
  "error": "Authentication required"
}
```

**Response Body (403 Forbidden)**:

```json
{
  "error": "Access denied: user_id mismatch"
}
```

---

### 2. Create Task

**Endpoint**: `POST /api/v1/users/{user_id}/tasks`

**Authentication**: Required (JWT)

**Description**: Create a new task for the authenticated user. Task is automatically associated with the user.

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID | User ID (must match authenticated user_id from JWT) |

**Request Body**:

```json
{
  "title": "Task title (required)",
  "description": "Task description (optional)"
}
```

**Request Validation**:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | Yes | 1-200 characters, not empty or whitespace-only |
| `description` | string | No | 0-1000 characters |

**Response Codes**:

| Code | Description |
|------|-------------|
| 201 | Created - returns created task |
| 400 | Bad Request - invalid request body |
| 401 | Unauthorized - missing or invalid JWT |
| 403 | Forbidden - `user_id` in path doesn't match authenticated user |
| 500 | Internal server error |

**Response Body (201 Created)**:

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440113",
  "title": "Implement authentication flow",
  "description": "Add JWT middleware to FastAPI",
  "completed": false,
  "user_id": "550e8400-e29b-41d4-a716-4466554400000",
  "created_at": "2026-01-03T12:00:00Z",
  "updated_at": "2026-01-03T12:00:00Z"
}
```

**Response Body (400 Bad Request)**:

```json
{
  "error": "Invalid request body",
  "details": {
    "title": "Title is required and must be 1-200 characters"
  }
}
```

---

### 3. Get Task by ID

**Endpoint**: `GET /api/v1/users/{user_id}/tasks/{task_id}`

**Authentication**: Required (JWT)

**Description**: Retrieve a specific task by ID. User must own the task.

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID | User ID (must match authenticated user_id from JWT) |
| `task_id` | UUID | Task ID to retrieve |

**Response Codes**:

| Code | Description |
|------|-------------|
| 200 | Success - returns task |
| 401 | Unauthorized - missing or invalid JWT |
| 403 | Forbidden - `user_id` in path doesn't match authenticated user |
| 404 | Not Found - task doesn't exist or user doesn't own it |
| 500 | Internal server error |

**Response Body (200 OK)**:

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440113",
  "title": "Implement authentication flow",
  "description": "Add JWT middleware to FastAPI",
  "completed": false,
  "user_id": "550e8400-e29b-41d4-a716-4466554400000",
  "created_at": "2026-01-03T12:00:00Z",
  "updated_at": "2026-01-03T12:00:00Z"
}
```

**Response Body (404 Not Found)**:

```json
{
  "error": "Task not found"
}
```

**Security Note**: Returns 404 whether task doesn't exist OR user doesn't own it (prevents enumeration).

---

### 4. Update Task

**Endpoint**: `PUT /api/v1/users/{user_id}/tasks/{task_id}`

**Authentication**: Required (JWT)

**Description**: Update an existing task. User must own the task. Partial updates allowed (only provided fields are updated).

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID | User ID (must match authenticated user_id from JWT) |
| `task_id` | UUID | Task ID to update |

**Request Body**:

```json
{
  "title": "Updated task title (optional)",
  "description": "Updated description (optional)",
  "completed": true
}
```

**Request Validation**:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | No | 1-200 characters if provided |
| `description` | string | No | 0-1000 characters if provided |
| `completed` | boolean | No | true or false if provided |

**Response Codes**:

| Code | Description |
|------|-------------|
| 200 | Success - returns updated task |
| 400 | Bad Request - invalid request body |
| 401 | Unauthorized - missing or invalid JWT |
| 403 | Forbidden - `user_id` in path doesn't match authenticated user |
| 404 | Not Found - task doesn't exist or user doesn't own it |
| 500 | Internal server error |

**Response Body (200 OK)**:

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440113",
  "title": "Implement JWT authentication flow",
  "description": "Add JWT verification middleware to all protected routes",
  "completed": true,
  "user_id": "550e8400-e29b-41d4-a716-4466554400000",
  "created_at": "2026-01-03T12:00:00Z",
  "updated_at": "2026-01-03T12:15:00Z"
}
```

---

### 5. Delete Task

**Endpoint**: `DELETE /api/v1/users/{user_id}/tasks/{task_id}`

**Authentication**: Required (JWT)

**Description**: Delete a task permanently. User must own the task. Cannot be undone.

**Path Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | UUID | User ID (must match authenticated user_id from JWT) |
| `task_id` | UUID | Task ID to delete |

**Response Codes**:

| Code | Description |
|------|-------------|
| 204 | No Content - task deleted successfully |
| 401 | Unauthorized - missing or invalid JWT |
| 403 | Forbidden - `user_id` in path doesn't match authenticated user |
| 404 | Not Found - task doesn't exist or user doesn't own it |
| 500 | Internal server error |

**Response Body (204 No Content)**:
Empty response body (no content).

**Response Body (404 Not Found)**:

```json
{
  "error": "Task not found"
}
```

---

## Health Check Endpoint

### Health Check

**Endpoint**: `GET /api/v1/health`

**Authentication**: Not required

**Description**: Check if backend API is running and healthy.

**Response Codes**:

| Code | Description |
|------|-------------|
| 200 | Success - API is healthy |

**Response Body (200 OK)**:

```json
{
  "status": "healthy",
  "timestamp": "2026-01-03T12:00:00Z"
}
```

---

## Authentication Endpoints

**Note**: User signup and signin are handled by Better Auth on the frontend. The backend only verifies JWTs issued by Better Auth.

If backend endpoints are needed for user management (optional for Phase II):

### Create User Account

**Endpoint**: `POST /api/v1/users`

**Authentication**: Not required

**Description**: Create a new user account. This is typically handled by Better Auth, but can be used for API-only testing.

**Request Body**:

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Request Validation**:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email format, unique |
| `password` | string | Yes | Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special |

**Response Codes**:

| Code | Description |
|------|-------------|
| 201 | Created - returns user (without password hash) |
| 400 | Bad Request - invalid email/password |
| 409 | Conflict - email already exists |
| 500 | Internal server error |

**Response Body (201 Created)**:

```json
{
  "id": "550e8400-e29b-41d4-a716-4466554400000",
  "email": "user@example.com",
  "created_at": "2026-01-03T10:00:00Z"
}
```

---

## Error Response Format

All error responses follow this consistent format:

```json
{
  "error": "Human-readable error message",
  "details": {
    "field_name": "Specific validation error for this field (optional)"
  }
}
```

**Common Error Codes**:

| Code | Meaning |
|------|---------|
| 400 | Bad Request - invalid request body or parameters |
| 401 | Unauthorized - missing, invalid, or expired JWT |
| 403 | Forbidden - user doesn't have permission |
| 404 | Not Found - resource doesn't exist or not owned |
| 409 | Conflict - email already exists (user creation) |
| 422 | Unprocessable Entity - validation failed |
| 500 | Internal Server Error - unexpected server error |

---

## Security Headers

All responses include these security headers:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

---

## JWT Token Structure

JWT tokens issued by Better Auth contain the following claims:

```json
{
  "sub": "550e8400-e29b-41d4-a716-4466554400000",
  "email": "user@example.com",
  "iat": 17042856000,
  "exp": 17042896000
}
```

**Claims**:
- `sub`: User ID (subject)
- `email`: User's email address
- `iat`: Issued at timestamp (Unix epoch)
- `exp`: Expiration timestamp (Unix epoch)

**Backend JWT Verification**:
1. Extract `Authorization: Bearer <token>` header
2. Verify JWT signature using `BETTER_AUTH_SECRET` environment variable
3. Check token not expired (`exp` > current time)
4. Extract `user_id` from `sub` claim
5. Inject `user_id` into request state for route handlers

---

## API Usage Examples

### Example 1: List Tasks with cURL

```bash
curl -X GET \
  "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-4466554400000/tasks" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Example 2: Create Task with cURL

```bash
curl -X POST \
  "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-4466554400000/tasks" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete API documentation",
    "description": "Write OpenAPI spec for task endpoints"
  }'
```

### Example 3: Update Task with cURL

```bash
curl -X PUT \
  "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-4466554400000/tasks/660e8400-e29b-41d4-a716-446655440113" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

### Example 4: Delete Task with cURL

```bash
curl -X DELETE \
  "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-4466554400000/tasks/660e8400-e29b-41d4-a716-446655440113" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Example 5: Test 401 Unauthorized (No Token)

```bash
curl -X GET \
  "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-4466554400000/tasks"

# Response: 401 Unauthorized
# Body: {"error": "Authentication required"}
```

---

## Rate Limiting (Future Enhancement)

For Phase II, no rate limiting is implemented. For production deployment, consider adding rate limiting to prevent abuse:

- Anonymous requests: 10 requests/minute
- Authenticated requests: 100 requests/minute
- Burst allowance: 5 requests above limit

---

## CORS Configuration

Backend must configure CORS to allow requests from frontend:

```
Allow-Origin: https://<frontend-domain>.vercel.app
Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Allow-Headers: Authorization, Content-Type
Allow-Credentials: true
```

For local development:
```
Allow-Origin: http://localhost:3000
```

---

## Summary

- **5 Task Endpoints**: List, Create, Get, Update, Delete (all scoped by `user_id`)
- **JWT Authentication**: All task endpoints require `Authorization: Bearer <jwt>` header
- **Data Isolation**: All queries filter by `user_id`, ownership verified for UPDATE/DELETE
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Strict-Transport-Security
- **Error Format**: Consistent JSON error responses with human-readable messages
- **Health Check**: Public endpoint for uptime monitoring
