from datetime import datetime
from typing import Optional
from uuid import uuid4
from sqlmodel import SQLModel, Field, Relationship


class Task(SQLModel, table=True):
    """Task model for todo items owned by users."""

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
    )
    title: str = Field(
        max_length=200,
        index=True,
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
    )
    completed: bool = Field(default=False, index=True)
    user_id: str = Field(
        foreign_key="user.id",
        index=True,
        ondelete="CASCADE",
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")

    def to_dict(self) -> dict:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_response(self) -> dict:
        """Convert task to API response."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
