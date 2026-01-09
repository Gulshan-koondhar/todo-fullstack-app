---
title: Todo Backend API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# Todo Backend API

This is the backend API for the secure multi-user todo application, designed for deployment on Hugging Face Spaces.

## Features

- Secure JWT-based authentication
- Multi-user isolation (users can only access their own tasks)
- RESTful API with full CRUD operations for tasks
- PostgreSQL database support

## Deployment on Hugging Face Spaces

This application is ready for deployment on Hugging Face Spaces with the following configuration:

### Environment Variables

You'll need to set the following environment variables in your Hugging Face Space settings:

- `DATABASE_URL`: PostgreSQL database connection string
- `BETTER_AUTH_SECRET`: JWT secret key (at least 32 characters)
- `BACKEND_CORS_ORIGINS`: Comma-separated list of allowed origins (including your HF Space URL)

### Runtime

The application will automatically run on the port specified by the `PORT` environment variable (standard for Hugging Face Spaces).

## API Endpoints

- `/docs`: Interactive API documentation (Swagger UI)
- `/api/v1/users/`: User authentication endpoints
- `/api/v1/users/{user_id}/tasks/`: Task management endpoints

## Requirements

- Python 3.11+
- PostgreSQL database