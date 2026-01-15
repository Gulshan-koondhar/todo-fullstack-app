from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..database.database import get_session
from ..middleware.auth import get_current_user, TokenData


router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "service": "AI Todo Chatbot Backend"}


@router.get("/user")
def get_user_info(current_user: TokenData = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.
    """
    return {
        "user_id": str(current_user.user_id),
        "message": "User authenticated successfully"
    }


@router.get("/api-info")
def api_info():
    """
    Get information about the API and available endpoints.
    """
    return {
        "name": "AI Todo Chatbot API",
        "version": "1.0.0",
        "description": "API for the AI-Powered Todo Chatbot that allows users to manage todos using natural language",
        "features": [
            "Natural language todo creation, retrieval, update, and deletion",
            "MCP tool integration for AI agent communication",
            "JWT-based authentication and user data isolation",
            "Chat history persistence"
        ]
    }