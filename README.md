# Todo Application

A secure, multi-user todo web application built with Next.js 16+ and FastAPI.

## Features

- **User Authentication**: Secure signup/signin with JWT tokens
- **Task Management**: Create, view, update, delete, and complete tasks
- **Data Isolation**: Complete user data isolation - users can only see their own tasks
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode**: Automatic theme switching based on system preference
- **Real-time Feedback**: Toast notifications for all actions

## Tech Stack

### Frontend
- Next.js 16+ with App Router
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Better Auth for authentication
- Zod for validation

### Backend
- FastAPI with Python 3.11+
- SQLModel for ORM
- PostgreSQL (Neon) for database
- JWT authentication

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL database (Neon free tier recommended)

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your configuration
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database URL and JWT secret
python -m uvicorn app.main:app --reload
```

## Project Structure

```
├── frontend/                 # Next.js frontend
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities and configurations
│   └── hooks/               # Custom React hooks
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── db/             # Database utilities
│   │   └── models/         # SQLModel entities
│   └── requirements.txt    # Python dependencies
└── specs/                   # Feature specifications
```

## API Documentation

See `specs/001-multi-user-todo/contracts/api-spec.md` for detailed API documentation.

## License

MIT
