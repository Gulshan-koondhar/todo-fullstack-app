from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from ..middleware.auth import verify_token, TokenData


def validate_user_access(user_id: UUID, token_data: TokenData) -> bool:
    """
    Validate that the user in the token matches the requested user_id.

    Args:
        user_id: The user_id being accessed
        token_data: The token data from JWT validation

    Returns:
        bool: True if user has access, raises HTTPException if not
    """
    if str(user_id) != str(token_data.user_id):
        raise HTTPException(
            status_code=403,
            detail="Access denied: Insufficient permissions to access this resource"
        )
    return True


def validate_todo_ownership(todo_user_id: UUID, token_data: TokenData) -> bool:
    """
    Validate that the user in the token owns the todo being accessed.

    Args:
        todo_user_id: The user_id associated with the todo
        token_data: The token data from JWT validation

    Returns:
        bool: True if user owns the todo, raises HTTPException if not
    """
    if str(todo_user_id) != str(token_data.user_id):
        raise HTTPException(
            status_code=403,
            detail="Access denied: You do not own this todo item"
        )
    return True


def validate_chat_session_ownership(session_user_id: UUID, token_data: TokenData) -> bool:
    """
    Validate that the user in the token owns the chat session being accessed.

    Args:
        session_user_id: The user_id associated with the chat session
        token_data: The token data from JWT validation

    Returns:
        bool: True if user owns the chat session, raises HTTPException if not
    """
    if str(session_user_id) != str(token_data.user_id):
        raise HTTPException(
            status_code=403,
            detail="Access denied: You do not own this chat session"
        )
    return True


def validate_jwt_token(token: str) -> TokenData:
    """
    Validate a JWT token and return the token data.

    Args:
        token: The JWT token string

    Returns:
        TokenData: Contains user_id and expiration

    Raises:
        HTTPException: If token is invalid
    """
    return verify_token(token)