from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.chat_session import ChatSession, ChatSessionCreate, ChatSessionUpdate, ChatSessionPublic
from .base_service import BaseService


class ChatSessionService(BaseService[ChatSession, ChatSessionCreate, ChatSessionUpdate]):
    """
    Service class for handling chat session-related operations.
    """
    def __init__(self):
        super().__init__(ChatSession)

    def get_sessions_by_user(self, db: Session, user_id: UUID) -> List[ChatSession]:
        """
        Get all chat sessions for a specific user.
        """
        statement = select(ChatSession).where(ChatSession.user_id == user_id)
        return db.exec(statement).all()

    def create_session(self, db: Session, obj_in: ChatSessionCreate) -> ChatSession:
        """
        Create a new chat session.
        """
        session = ChatSession(
            user_id=obj_in.user_id,
            messages=obj_in.messages or []
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def add_message_to_session(self, db: Session, session_id: UUID, user_id: UUID, role: str, content: str) -> Optional[ChatSession]:
        """
        Add a message to a specific chat session for a user.
        """
        session = db.exec(select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        )).first()

        if session:
            if not session.messages:
                session.messages = []

            # Add the new message to the session
            session.messages.append({
                "role": role,
                "content": content,
                "timestamp": str(session.updated_at)  # Use current timestamp
            })

            db.add(session)
            db.commit()
            db.refresh(session)

        return session

    def to_public(self, session: ChatSession) -> ChatSessionPublic:
        """
        Convert a ChatSession model to a ChatSessionPublic model for safe serialization.
        """
        return ChatSessionPublic(
            id=session.id,
            user_id=session.user_id,
            messages=session.messages,
            created_at=session.created_at,
            updated_at=session.updated_at
        )


# Create a singleton instance for use throughout the application
chat_session_service = ChatSessionService()