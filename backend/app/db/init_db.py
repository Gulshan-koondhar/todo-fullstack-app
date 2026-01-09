"""Database initialization module."""
from sqlalchemy import text
from sqlmodel import SQLModel
from app.db.session import engine, SessionLocal
from app.models.user import User
from app.models.task import Task


def init_db():
    """Create all database tables if they don't exist."""
    SQLModel.metadata.create_all(bind=engine)


def verify_tables():
    """Verify that tables were created successfully."""
    with SessionLocal() as session:
        result = session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result.fetchall()]
        return tables


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database tables created.")
    tables = verify_tables()
    print(f"Tables in database: {tables}")
