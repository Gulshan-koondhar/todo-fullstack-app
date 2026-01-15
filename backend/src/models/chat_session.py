from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4


class ChatSessionBase(SQLModel):
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    messages: Optional[List[Dict[str, Any]]] = Field(default=None)  # List of message objects


class ChatSession(ChatSessionBase, table=True):
    """
    Chat session model representing a conversation between a user and the AI agent,
    containing the history of interactions.
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ChatSessionCreate(SQLModel):
    """
    Model for creating a new chat session.
    """
    user_id: UUID
    messages: Optional[List[Dict[str, Any]]] = []


class ChatSessionUpdate(SQLModel):
    """
    Model for updating an existing chat session.
    """
    messages: Optional[List[Dict[str, Any]]] = None


class ChatSessionPublic(ChatSessionBase):
    """
    Public model for chat session with ID and timestamps.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime