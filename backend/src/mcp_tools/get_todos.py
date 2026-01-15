from typing import Dict, Any, Optional
from uuid import UUID
import json
from pydantic import BaseModel, Field
from ..services.todo_service import todo_service
from ..database.database import get_db_session
from ..auth.validation import validate_jwt_token


class GetTodosParams(BaseModel):
    """
    Parameters for the get_todos MCP tool.
    """
    completed: Optional[bool] = Field(None, description="Optional filter to get only completed (true) or incomplete (false) todos")


def get_todos(user_token: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieves all todos for the authenticated user, optionally filtered by completion status.

    Args:
        user_token: JWT token for user authentication
        params: Parameters for getting todos (optional completed filter)

    Returns:
        Dict containing success status, todos data, and potential error
    """
    try:
        # Validate the JWT token to get user information
        token_data = validate_jwt_token(user_token)
        user_id = token_data.user_id

        # Validate parameters using Pydantic model
        validated_params = GetTodosParams(**params)

        # Get todos using the service
        with get_db_session() as db_session:
            todos = todo_service.get_todos_by_user(
                db=db_session,
                user_id=user_id,
                completed=validated_params.completed
            )

            # Convert todos to public format
            todos_data = []
            for todo in todos:
                todos_data.append({
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                })

            # Return success response with todos data
            return {
                "success": True,
                "todos": todos_data
            }

    except Exception as e:
        # Return error response
        return {
            "success": False,
            "error": str(e)
        }


# Example usage function for testing
def example_usage():
    """
    Example of how the get_todos function would be used.
    This is for demonstration purposes only.
    """
    # This would normally be called by the MCP framework with a valid token
    example_params = {
        "completed": None  # Get all todos regardless of completion status
    }

    # This token would come from the authenticated user session
    example_token = "example_jwt_token"

    result = get_todos(example_token, example_params)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    example_usage()