from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.core.config import settings
import logging
from typing import Optional

# Import all models to register them with SQLModel metadata
from app.models.user import User
from app.models.task import Task


# Engine will be created lazily to handle malformed URLs gracefully
engine: Optional[object] = None
SessionLocal: Optional[object] = None
_database_available = False


def get_engine():
    """Create and return database engine, handling errors gracefully."""
    global engine, SessionLocal, _database_available

    if engine is not None:
        return engine

    try:
        # Validate that the DATABASE_URL looks like a proper connection string
        db_url = settings.DATABASE_URL
        if not db_url:
            # Use SQLite as fallback for Hugging Face Spaces deployment
            db_url = "sqlite:///./todo.db"

        if not db_url.startswith(('postgresql://', 'postgresql+psycopg2://', 'sqlite://', 'mysql://', 'oracle://')):
            raise ValueError(f"Invalid database URL format: {db_url}. Must start with postgresql://, sqlite://, mysql://, or oracle://")

        # Only apply sslmode for PostgreSQL databases, not for SQLite
        connect_args = {"sslmode": "require"} if "localhost" not in db_url and not db_url.startswith("sqlite://") else {}
        engine = create_engine(
            db_url,
            echo=False,
            connect_args=connect_args,
        )
        logging.info("Database engine created successfully")
        _database_available = True

        # Create session factory only after engine is created
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    except Exception as e:
        logging.error(f"Failed to create database engine: {e}")
        # Print more specific error to help with debugging
        print(f"Database engine creation failed: {e}")
        print("Please verify your DATABASE_URL environment variable is correctly formatted.")
        print("Example format: postgresql://username:password@hostname:port/database_name")
        print("Continuing without database functionality...")

        # Create a mock engine that will fail gracefully when used
        fallback_engine = create_engine(
            "sqlite:///:memory:",
            echo=False,
            connect_args={"check_same_thread": False},
        )
        engine = fallback_engine
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        _database_available = False

    return engine


def get_session_local():
    """Get the session local, creating it if needed."""
    get_engine()  # Ensure engine and session local are created
    return SessionLocal


def get_db():
    """Dependency to get database session."""
    session_local = get_session_local()

    if not is_database_available():
        # Log a warning but still provide a session (will fail on actual DB operations)
        logging.warning("Attempting to get database session but database is not available")

    db = session_local()
    try:
        yield db
    finally:
        db.close()


def is_database_available():
    """Check if the database is available."""
    global _database_available
    # Try to get engine which will update the availability status
    get_engine()
    return _database_available


def init_db():
    """Initialize database tables."""
    try:
        # Attempt to connect to the database and create tables
        # Don't check DATABASE_AVAILABLE here to avoid the chicken-and-egg problem
        engine_for_init = get_engine()
        SQLModel.metadata.create_all(bind=engine_for_init)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
        print("This might be because the database URL is not configured yet.")
        print("Make sure to set the DATABASE_URL environment variable with a valid PostgreSQL connection string.")
        # Continue without raising the exception to allow the app to start
        # The app can still function for endpoints that don't require database access immediately
