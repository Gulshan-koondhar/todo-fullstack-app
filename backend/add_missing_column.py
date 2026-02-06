#!/usr/bin/env python3
"""
Script to add missing 'in_progress' column to the task table.
This addresses the database schema mismatch issue.
"""

import os
import sys
from sqlmodel import create_engine, text

# Add the app directory to the path so we can import the settings
sys.path.append('.')

from app.core.config import settings

def add_in_progress_column():
    """Add the missing in_progress column to the task table."""
    # Create engine using the database URL from settings
    db_url = settings.DATABASE_URL

    print(f"Connecting to database: {db_url}")

    # Create engine
    engine = create_engine(db_url)

    # Check if the column already exists
    with engine.connect() as conn:
        # Query to check if the column exists (works for PostgreSQL)
        if 'postgresql://' in db_url or 'postgresql+psycopg2://' in db_url:
            check_query = text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='task' AND column_name='in_progress';
            """)

            result = conn.execute(check_query)
            existing_columns = [row[0] for row in result.fetchall()]

            if 'in_progress' in existing_columns:
                print("Column 'in_progress' already exists in the task table.")
                return

            # Add the missing column
            alter_query = text("ALTER TABLE task ADD COLUMN in_progress BOOLEAN DEFAULT FALSE;")
            conn.execute(alter_query)
            conn.commit()
            print("Column 'in_progress' added successfully to the task table.")

        elif 'sqlite://' in db_url:
            # For SQLite, we need to handle it differently since ALTER TABLE has limitations
            # First check if column exists
            check_query = text("""
                SELECT name
                FROM pragma_table_info('task')
                WHERE name='in_progress';
            """)

            result = conn.execute(check_query)
            existing_columns = [row[0] for row in result.fetchall()]

            if 'in_progress' in existing_columns:
                print("Column 'in_progress' already exists in the task table.")
                return

            # For SQLite, we need to recreate the table with the new column
            print("SQLite detected. Recreating table with in_progress column...")

            # Get the current table structure
            result = conn.execute(text("SELECT sql FROM sqlite_master WHERE type='table' AND name='task';"))
            current_sql = result.fetchone()[0]

            if 'in_progress' not in current_sql:
                # Modify the SQL to include the new column
                # Find the closing parenthesis and add the new column before it
                pos = current_sql.rfind(')')
                new_column_def = ", in_progress BOOLEAN DEFAULT FALSE"
                new_sql = current_sql[:pos] + new_column_def + current_sql[pos:]

                # Create a new table with the updated structure
                temp_table_sql = new_sql.replace('task', 'task_temp')
                conn.execute(text(temp_table_sql))

                # Copy data from old table to new table
                # We need to explicitly list columns to avoid issues with the new column
                conn.execute(text("""
                    INSERT INTO task_temp (id, title, description, completed, user_id, created_at, updated_at)
                    SELECT id, title, description, completed, user_id, created_at, updated_at FROM task;
                """))

                # Drop the old table
                conn.execute(text("DROP TABLE task;"))

                # Rename the new table
                conn.execute(text("ALTER TABLE task_temp RENAME TO task;"))

                conn.commit()
                print("Column 'in_progress' added successfully to the task table (SQLite).")
            else:
                print("Column 'in_progress' already exists in the task table.")

        else:
            print(f"Unsupported database type: {db_url}")
            return

if __name__ == "__main__":
    add_in_progress_column()