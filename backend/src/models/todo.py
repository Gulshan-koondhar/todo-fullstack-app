from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    in_progress: bool = Field(default=False)


class Todo(TodoBase, table=True):
    """
    Todo item model representing a user's task that can be managed through natural language commands.
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TodoCreate(TodoBase):
    """
    Model for creating a new todo item.
    """
    pass


class TodoUpdate(SQLModel):
    """
    Model for updating an existing todo item.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)
    in_progress: Optional[bool] = Field(default=None)


class TodoPublic(TodoBase):
    """
    Public model for todo item with ID and timestamps.
    """
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime