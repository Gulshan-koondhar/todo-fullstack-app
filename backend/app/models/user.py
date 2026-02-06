from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from sqlmodel import SQLModel, Field, Relationship
import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash using bcrypt."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


class User(SQLModel, table=True):
    """User model for authentication and ownership."""

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
    )
    password_hash: str = Field(
        max_length=255,
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Verify a password against the hash."""
        return verify_password(password, self.password_hash)

    def to_dict(self, include_password: bool = False) -> dict:
        """Convert user to dictionary."""
        data = {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if include_password:
            data["password_hash"] = self.password_hash
        return data

    def to_response(self) -> dict:
        """Convert user to API response (without password)."""
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
