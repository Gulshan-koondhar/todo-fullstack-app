# Quickstart Guide: Secure Multi-User Todo Application

**Feature**: 001-multi-user-todo
**Created**: 2026-01-03
**Purpose**: Get the development environment up and running quickly

## Prerequisites

### Required Software

- **Node.js**: 18.x or higher (for Next.js frontend)
- **Python**: 3.11 or higher (for FastAPI backend)
- **PostgreSQL Client**: `psql` or pgAdmin (optional, for database inspection)
- **Git**: For version control
- **Code Editor**: VS Code (recommended) with extensions:
  - Prettier - Code formatter
  - ESLint - JavaScript/TypeScript linter
  - Python - Python language support
  - Tailwind CSS IntelliSense - CSS framework support

### Accounts

- **Neon Database Account**: Free tier (https://neon.tech)
- **Vercel Account** (for frontend deployment): Free tier (https://vercel.com)
- **Better Auth Setup**: See https://better-auth.com/docs for initial configuration

---

## Environment Setup (10 minutes)

### 1. Clone Repository

```bash
git clone <repository-url>
cd hackathon_phase_II
git checkout 001-multi-user-todo
```

### 2. Set Up Backend (FastAPI)

#### Navigate to backend directory

```bash
cd backend
```

#### Create Python virtual environment

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**:
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Create `.env` file

Create a `.env` file in the `backend/` directory:

```bash
# Database (Neon Serverless PostgreSQL)
DATABASE_URL=postgresql://<username>:<password>@<host>/<database>?sslmode=require

# JWT Secret (shared with frontend)
BETTER_AUTH_SECRET=your-super-secret-jwt-signing-key-change-this-in-production

# Backend Settings
BACKEND_CORS_ORIGINS=http://localhost:3000
BACKEND_HOST=localhost
BACKEND_PORT=8000
```

**Get DATABASE_URL from Neon**:
1. Sign up at https://neon.tech
2. Create a new project
3. Copy the connection string (PostgreSQL)
4. Replace `<username>`, `<password>`, `<host>`, `<database>` with your Neon credentials

**Generate BETTER_AUTH_SECRET**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Initialize Database

```bash
# Initialize database schema
python -m app.db.init_db

# Verify tables created
python -c "from app.db.session import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"
```

Expected output:
```python
['users', 'tasks']
```

### 4. Start Backend Server

```bash
# Run FastAPI development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify backend is running:
```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-03T12:00:00Z"
}
```

### 5. Set Up Frontend (Next.js)

#### Navigate to frontend directory (new terminal)

```bash
cd frontend
```

#### Install dependencies

```bash
npm install
```

#### Create `.env.local` file

Create a `.env.local` file in the `frontend/` directory:

```bash
# API URL (backend)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# JWT Secret (shared with backend)
BETTER_AUTH_SECRET=your-super-secret-jwt-signing-key-change-this-in-production

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
BETTER_AUTH_SECRET=your-super-secret-jwt-signing-key-change-this-in-production

# Environment
NODE_ENV=development
```

**Important**: `BETTER_AUTH_SECRET` MUST be identical in backend `.env` and frontend `.env.local`

### 6. Initialize Better Auth

Follow the Better Auth setup guide: https://better-auth.com/docs/quickstart

```bash
# Install Better Auth
npm install better-auth

# Initialize Better Auth configuration
npx better-auth init
```

Configure Better Auth in `frontend/lib/auth.ts` (created by init command):

```typescript
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";

// For Phase II, use simple email/password authentication
export const auth = betterAuth({
  providers: {
    emailAndPassword: true,
  },
  secret: process.env.BETTER_AUTH_SECRET,
});
```

### 7. Start Frontend Development Server

```bash
npm run dev
```

Frontend will be available at: http://localhost:3000

---

## Development Workflow

### Running Both Services

**Backend (Terminal 1)**:
```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows PowerShell
source venv/bin/activate  # Linux/macOS
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Terminal 2)**:
```bash
cd frontend
npm run dev
```

### Database Migrations (if needed)

```bash
# In backend directory
alembic revision --autogenerate -m "Add tasks table"
alembic upgrade head
```

### API Testing with Postman

1. Import API specification from `specs/001-multi-user-todo/contracts/api-spec.md`
2. Set environment variable: `BASE_URL=http://localhost:8000/api/v1`
3. Use JWT token from Better Auth in `Authorization` header

**Example Request**:
- Method: POST
- URL: `{{BASE_URL}}/users/{user_id}/tasks`
- Headers:
  - `Authorization: Bearer <your-jwt-token>`
  - `Content-Type: application/json`
- Body:
```json
{
  "title": "Test task",
  "description": "Testing API"
}
```

---

## Common Issues

### Issue: Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Activate virtual environment and install dependencies:
```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Issue: Database connection failed

**Error**: `connection to server at "localhost:5432" failed`

**Solution**: Ensure `DATABASE_URL` in `.env` is correct:
- Check Neon connection string format
- Verify SSL mode is enabled (`sslmode=require`)
- Confirm database exists

### Issue: Frontend can't connect to backend

**Error**: `Network request failed` or CORS errors

**Solution**:
1. Check backend is running on port 8000
2. Verify `NEXT_PUBLIC_API_URL` in frontend `.env.local`
3. Check `BACKEND_CORS_ORIGINS` in backend `.env` includes frontend URL
4. Try accessing http://localhost:8000/api/v1/health in browser

### Issue: JWT verification fails

**Error**: `401 Unauthorized` on API requests

**Solution**:
1. Verify `BETTER_AUTH_SECRET` is identical in both backend `.env` and frontend `.env.local`
2. Check JWT is sent in `Authorization: Bearer <token>` header
3. Ensure JWT is not expired

### Issue: Better Auth not working

**Error**: Auth pages return 404 or errors

**Solution**:
1. Verify Better Auth is initialized correctly in `frontend/lib/auth.ts`
2. Check `NEXT_PUBLIC_BETTER_AUTH_URL` is correct
3. Review Better Auth documentation: https://better-auth.com/docs

---

## Development Tips

### Hot Reload

- **Backend**: Changes to Python files auto-reload (Uvicorn `--reload` flag)
- **Frontend**: Changes to Next.js files auto-reload (Vite dev server)

### Database Inspection

Use Neon Console or `psql` to inspect data:

```bash
# Connect to Neon database
psql <DATABASE_URL>

# List tables
\dt

# Query users
SELECT * FROM users;

# Query tasks
SELECT * FROM tasks;
```

### Debugging

**Backend**:
```bash
# Set debug logging
export LOG_LEVEL=DEBUG  # Linux/macOS
set LOG_LEVEL=DEBUG  # Windows PowerShell

# Run with verbose output
python -m uvicorn app.main:app --reload --log-level debug
```

**Frontend**:
```bash
# Run with debug logging
DEBUG=* npm run dev
```

### Type Checking

**Frontend**:
```bash
npm run type-check
```

**Backend**:
```bash
# Pydantic validates request/response automatically
# Type hints enable IDE autocomplete
```

---

## Testing the Application

### 1. Create User Account

1. Navigate to http://localhost:3000/signup
2. Enter email: `test@example.com`
3. Enter password: `TestPass123!`
4. Click "Sign Up"
5. Redirected to task list page

### 2. Create Tasks

1. Click "Add Task" button
2. Enter title: "My first task"
3. (Optional) Enter description: "Testing task creation"
4. Click "Save"
5. Task appears in list with toast notification

### 3. Test Task CRUD

- **Complete Task**: Click checkbox → task shows strikethrough
- **Edit Task**: Click edit button → update title/description → save
- **Delete Task**: Click delete button → confirm → task removed

### 4. Test User Isolation (Security)

1. Sign out of current user
2. Create new account: `test2@example.com` / `TestPass456!`
3. Verify new user sees 0 tasks (not previous user's tasks)
4. Create task as new user
5. Sign out, sign in as first user
6. Verify first user sees only their own tasks

### 5. Test Responsiveness

1. Open browser DevTools
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test mobile viewport (375x667)
4. Verify FAB (Floating Action Button) appears at bottom
5. Resize to desktop viewport
6. Verify fixed "Add Task" button appears

---

## Deployment

### Frontend to Vercel

1. Push code to GitHub repository
2. Import project in Vercel dashboard
3. Configure environment variables:
   - `NEXT_PUBLIC_API_URL` = your backend API URL
   - `BETTER_AUTH_SECRET` = production secret
   - `NEXT_PUBLIC_BETTER_AUTH_URL` = Vercel domain
4. Deploy (automatic on push)

### Backend to Cloud Provider

**Option 1: Render.com** (Free tier available)
1. Create new Web Service
2. Connect GitHub repository
3. Configure build: `pip install -r requirements.txt`
4. Configure start: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Add environment variables
6. Deploy

**Option 2: Railway.app** (Free tier available)
1. Create new project
2. Connect GitHub repository
3. Configure build and start commands
4. Add environment variables
5. Deploy

### Update Environment for Production

**Frontend (Vercel)**:
```bash
# In Vercel dashboard
NEXT_PUBLIC_API_URL=https://<your-backend-domain>/api/v1
BETTER_AUTH_SECRET=<production-secret>
NEXT_PUBLIC_BETTER_AUTH_URL=https://<your-vercel-domain>/api/auth
```

**Backend**:
```bash
# In .env file
DATABASE_URL=<neon-production-connection-string>
BETTER_AUTH_SECRET=<production-secret>
BACKEND_CORS_ORIGINS=https://<your-vercel-domain>
```

---

## Next Steps

1. **Review Implementation Plan**: `specs/001-multi-user-todo/plan.md`
2. **Check Data Model**: `specs/001-multi-user-todo/data-model.md`
3. **Review API Contracts**: `specs/001-multi-user-todo/contracts/api-spec.md`
4. **Generate Tasks**: Run `/sp.tasks` to create implementation roadmap
5. **Start Implementation**: Follow tasks in `specs/001-multi-user-todo/tasks.md`

---

## Support and Documentation

- **Feature Specification**: `specs/001-multi-user-todo/spec.md`
- **Implementation Plan**: `specs/001-multi-user-todo/plan.md`
- **Data Model**: `specs/001-multi-user-todo/data-model.md`
- **API Specification**: `specs/001-multi-user-todo/contracts/api-spec.md`
- **Data Contracts**: `specs/001-multi-user-todo/contracts/data-contracts.md`
- **Project Constitution**: `.specify/memory/constitution.md`
- **Better Auth Docs**: https://better-auth.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLModel Docs**: https://sqlmodel.tiangolo.com
- **Neon Docs**: https://neon.tech/docs
- **Tailwind CSS Docs**: https://tailwindcss.com/docs
- **shadcn/ui Docs**: https://ui.shadcn.com

---

## Summary

- **Setup Time**: 10-15 minutes
- **Technologies**: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth
- **Development**: Hot reload for both frontend and backend
- **Testing**: Manual testing with browser and Postman
- **Deployment**: Vercel (frontend) + Render/Railway (backend)
- **Support**: Comprehensive documentation available in `specs/` directory

You're now ready to start development! 🚀
