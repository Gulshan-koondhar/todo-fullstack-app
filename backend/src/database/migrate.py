from sqlmodel import SQLModel
from .database import engine
from ..models.todo import Todo
from ..models.chat_session import ChatSession
import os
from dotenv import load_dotenv

load_dotenv()

def create_db_and_tables():
    """
    Create database tables based on the models.
    This uses the existing Phase II schema as a foundation and adds new tables as needed.
    """
    print("Creating database tables...")

    # Create all tables defined in the models
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


def drop_db_tables():
    """
    Drop all database tables (use with caution!).
    """
    print("Dropping database tables...")
    SQLModel.metadata.drop_all(engine)
    print("Database tables dropped successfully!")


def recreate_db_tables():
    """
    Recreate database tables by dropping and creating them again.
    """
    drop_db_tables()
    create_db_and_tables()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        action = sys.argv[1].lower()

        if action == "drop":
            drop_db_tables()
        elif action == "recreate":
            recreate_db_tables()
        elif action == "create":
            create_db_and_tables()
        else:
            print(f"Unknown action: {action}")
            print("Usage: python migrate.py [create|drop|recreate]")
    else:
        # Default action is to create tables
        create_db_and_tables()