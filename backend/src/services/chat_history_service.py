from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.chat_session import ChatSession, ChatSessionCreate, ChatSessionUpdate
from .base_service import BaseService
from ..auth.validation import validate_chat_session_ownership


class ChatHistoryService(BaseService[ChatSession, ChatSessionCreate, ChatSessionUpdate]):
    """
    Service class for handling chat history-related operations.
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
                "timestamp": session.updated_at.isoformat()  # Use current timestamp
            })

            db.add(session)
            db.commit()
            db.refresh(session)

        return session

    def get_messages_for_session(self, db: Session, session_id: UUID, user_id: UUID) -> Optional[List[dict]]:
        """
        Get all messages for a specific chat session, ensuring user owns the session.
        """
        session = db.exec(select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        )).first()

        if session:
            return session.messages

        return None

    def get_recent_sessions(self, db: Session, user_id: UUID, limit: int = 10) -> List[ChatSession]:
        """
        Get the most recent chat sessions for a user.
        """
        statement = select(ChatSession).where(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.updated_at.desc()).limit(limit)

        return db.exec(statement).all()

    def get_full_history_for_user(self, db: Session, user_id: UUID) -> List[ChatSession]:
        """
        Get all chat history for a specific user.
        """
        statement = select(ChatSession).where(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.created_at)

        return db.exec(statement).all()

    def clear_session_messages(self, db: Session, session_id: UUID, user_id: UUID) -> bool:
        """
        Clear all messages in a specific chat session, ensuring user owns the session.
        """
        session = db.exec(select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        )).first()

        if session:
            session.messages = []
            db.add(session)
            db.commit()
            db.refresh(session)
            return True

        return False

    def delete_session(self, db: Session, session_id: UUID, user_id: UUID) -> bool:
        """
        Delete a specific chat session, ensuring user owns the session.
        """
        session = db.exec(select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        )).first()

        if session:
            db.delete(session)
            db.commit()
            return True

        return False


# Create a singleton instance for use throughout the application
chat_history_service = ChatHistoryService()