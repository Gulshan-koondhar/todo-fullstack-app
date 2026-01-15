# Quickstart Guide: AI-Powered Todo Chatbot

## Overview
This guide provides a quick overview of how to set up and run the AI-Powered Todo Chatbot system.

## Prerequisites
- Node.js 18+ for the Next.js frontend
- Python 3.11+ for the FastAPI backend
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- OpenAI API key for the AI agent functionality
- Better Auth configuration for authentication

## Setup Steps

### 1. Environment Configuration
```bash
# Copy environment variables
cp .env.example .env.local  # for frontend
cp backend/.env.example backend/.env  # for backend
```

### 2. Install Dependencies
```bash
# Frontend
cd frontend
npm install

# Backend
cd backend
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Run migrations using the existing Phase II schema
cd backend
python -m src.database.migrate
```

### 4. Start Services
```bash
# Terminal 1: Start backend
cd backend
python -m src.main

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## Architecture Components

### AI Agent Layer
- OpenAI Agents SDK for natural language processing
- MCP (Model Context Protocol) tools for executing todo operations
- Intent classification for mapping user input to appropriate tools

### MCP Tools
- `create_todo`: Create new todo items from natural language
- `get_todos`: Retrieve user's todo list
- `update_todo`: Update existing todo items
- `delete_todo`: Remove todo items
- `toggle_todo_completion`: Mark todos as completed/incomplete

### Backend Services
- FastAPI REST API (reusing Phase II endpoints)
- JWT authentication with Better Auth
- User data isolation with user_id filtering
- Database operations with SQLModel

### Frontend Components
- Next.js chat interface
- Real-time messaging with the AI agent
- Todo list display and management
- User authentication and session management

## Usage
1. Navigate to the application in your browser
2. Authenticate using your credentials
3. Interact with the chatbot using natural language:
   - "Add buy groceries to my todo list"
   - "Show me my todos"
   - "Mark buy milk as complete"
   - "Delete the meeting with John"

## Testing
```bash
# Run backend tests
cd backend
pytest

# Run frontend tests
cd frontend
npm run test

# Run contract tests
npm run test:contract
```