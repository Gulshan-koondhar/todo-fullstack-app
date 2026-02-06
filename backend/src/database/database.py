from sqlmodel import create_engine, Session
from typing import Generator
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment, defaulting to a local development database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/todo_db")

# Create the engine with appropriate settings
engine = create_engine(
    DATABASE_URL,
    # Additional engine configuration can be added here if needed
    echo=False  # Set to True for SQL query logging during development
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for use with dependency injection in FastAPI.
    """
    with Session(engine) as session:
        yield session


@contextmanager
def get_db_session():
    """
    Context manager for database sessions, useful for non-FastAPI code.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()