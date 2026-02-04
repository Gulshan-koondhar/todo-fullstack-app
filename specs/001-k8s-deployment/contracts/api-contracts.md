# API Contracts: Phase IV – Local Kubernetes Deployment

**Date**: 2026-01-20
**Feature**: Phase IV – Local Kubernetes Deployment
**Branch**: 001-k8s-deployment

## Overview

This document defines the API contracts for the AI Todo Chatbot application in the Kubernetes deployment context. The API contracts remain unchanged from Phase III, but this document highlights how they are exposed and managed in the Kubernetes environment.

## Authentication API

### POST /api/auth/register
**Description**: Register a new user account
- **Request Body**: `{email: string, password: string, name: string}`
- **Response**: `{user: User, token: string}`
- **Headers**: `Content-Type: application/json`
- **Kubernetes Service**: `todo-backend-service:8000`

### POST /api/auth/login
**Description**: Authenticate user and return JWT token
- **Request Body**: `{email: string, password: string}`
- **Response**: `{user: User, token: string}`
- **Headers**: `Content-Type: application/json`
- **Kubernetes Service**: `todo-backend-service:8000`

### GET /api/auth/me
**Description**: Get authenticated user profile
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{user: User}`
- **Kubernetes Service**: `todo-backend-service:8000`

## Task Management APIs

### GET /api/tasks
**Description**: Get all tasks for the authenticated user
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{tasks: Task[]}`
- **Kubernetes Service**: `todo-backend-service:8000`

### POST /api/tasks
**Description**: Create a new task for the authenticated user
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{title: string, description?: string, status?: string}`
- **Response**: `{task: Task}`
- **Kubernetes Service**: `todo-backend-service:8000`

### PUT /api/tasks/{taskId}
**Description**: Update an existing task
- **Headers**: `Authorization: Bearer <token>`
- **Path Params**: `taskId: string`
- **Request Body**: `{title?: string, description?: string, status?: string}`
- **Response**: `{task: Task}`
- **Kubernetes Service**: `todo-backend-service:8000`

### DELETE /api/tasks/{taskId}
**Description**: Delete a task
- **Headers**: `Authorization: Bearer <token>`
- **Path Params**: `taskId: string`
- **Response**: `{success: boolean}`
- **Kubernetes Service**: `todo-backend-service:8000`

## AI Chatbot APIs

### POST /api/chat
**Description**: Send a message to the AI chatbot
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{message: string, conversationId?: string}`
- **Response**: `{response: string, conversationId: string}`
- **Kubernetes Service**: `todo-backend-service:8000`

### GET /api/chat/conversations
**Description**: Get all conversations for the authenticated user
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{conversations: Conversation[]}`
- **Kubernetes Service**: `todo-backend-service:8000`

### GET /api/chat/conversations/{conversationId}
**Description**: Get messages for a specific conversation
- **Headers**: `Authorization: Bearer <token>`
- **Path Params**: `conversationId: string`
- **Response**: `{messages: Message[], conversation: Conversation}`
- **Kubernetes Service**: `todo-backend-service:8000`

## MCP Server APIs

### GET /api/mcp/tools
**Description**: Get available MCP tools
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{tools: Tool[]}`
- **Kubernetes Service**: `todo-backend-service:8000`

### POST /api/mcp/execute
**Description**: Execute an MCP tool
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**: `{toolId: string, params: object}`
- **Response**: `{result: object}`
- **Kubernetes Service**: `todo-backend-service:8000`

## Kubernetes Service Contracts

### Frontend Service
- **Name**: `todo-frontend-service`
- **Type**: `NodePort` or `ClusterIP`
- **Ports**:
  - `80:3000/TCP` (HTTP)
- **Selector**: `app=todo-frontend`
- **Environment**: Exposes Next.js application to external access

### Backend Service
- **Name**: `todo-backend-service`
- **Type**: `ClusterIP`
- **Ports**:
  - `8000:8000/TCP` (HTTP API)
- **Selector**: `app=todo-backend`
- **Environment**: Internal service for API access within cluster

### MCP Server Service
- **Name**: `todo-mcp-service` (if separate)
- **Type**: `ClusterIP`
- **Ports**:
  - `8001:8001/TCP` (MCP endpoints)
- **Selector**: `app=todo-mcp`
- **Environment**: Internal service for MCP server access

## Health Check Endpoints

### GET /health
**Description**: Health check endpoint for Kubernetes liveness/readiness probes
- **Response**: `{status: "healthy", timestamp: string}`
- **Kubernetes Service**: `todo-backend-service:8000`

### GET /ready
**Description**: Readiness probe endpoint
- **Response**: `{ready: boolean, checks: object}`
- **Kubernetes Service**: `todo-backend-service:8000`

## Error Handling Contract

### Standard Error Response
```json
{
  "error": {
    "message": "Human-readable error message",
    "code": "ERROR_CODE",
    "details": {}
  }
}
```

### Common HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

## Security Contract

### JWT Token Validation
- All protected endpoints require valid JWT token in Authorization header
- Tokens expire after 24 hours
- Refresh tokens mechanism implemented (if applicable)

### Rate Limiting
- API endpoints subject to rate limiting (configuration TBD)
- Standard rate limit headers included in responses

### CORS Policy
- Configured to allow frontend domain access
- Restricted to secure origins only