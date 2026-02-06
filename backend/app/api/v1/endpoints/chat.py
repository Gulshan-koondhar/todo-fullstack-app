from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional
from app.core.deps import get_current_user_id
import sys
import os
# Add the backend directory to Python path to import src modules
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, backend_dir)

from src.ai.openai_agent import process_openai_request


router = APIRouter()


class ChatRequest(BaseModel):
    """Request schema for chat operations."""
    message: str


class ChatResponse(BaseModel):
    """Response schema for chat operations."""
    success: bool
    message: Optional[str] = None
    results: Optional[list] = None
    error: Optional[str] = None
    needs_clarification: Optional[bool] = False


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    token_user_id: str = Depends(get_current_user_id)
):
    """
    Chat with the AI agent to perform todo operations using natural language.

    The AI agent can understand requests like:
    - "Create a task to buy groceries"
    - "Update my task 'buy groceries' to 'buy milk and bread'"
    - "Complete the task 'buy groceries'"
    - "Delete the task 'buy groceries'"
    - "Show me my tasks"
    """
    try:
        # Process the natural language request
        # We need to create a proper JWT token to pass to the agent
        # Since get_current_user_id only returns the user_id, we need to reconstruct the token
        # For now, we'll pass the user_id directly as it's used for validation internally
        result = process_openai_request(request.message, token_user_id)

        return ChatResponse(
            success=result.get("success", False),
            message=result.get("message"),
            results=result.get("results"),
            error=result.get("error"),
            needs_clarification=result.get("needs_clarification", False)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )