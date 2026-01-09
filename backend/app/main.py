from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.session import init_db, is_database_available
from app.api.v1.router import api_router
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    try:
        init_db()
        if is_database_available():
            logging.info("Database initialized successfully during startup")
        else:
            logging.warning("Database not available - app will start with limited functionality")
    except Exception as e:
        logging.error(f"Database initialization failed during startup: {e}")
        logging.info("The application will continue to start, but database functionality may be limited")
    yield
    # Shutdown: cleanup if needed


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Secure multi-user todo API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS.split(",") if settings.BACKEND_CORS_ORIGINS else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint for Hugging Face Spaces."""
    return {"message": "Todo Backend API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    status = "healthy"
    if not is_database_available():
        status = "degraded - database unavailable"

    return {"status": status}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True,
    )
