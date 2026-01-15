from typing import Dict, Any, Optional
from uuid import UUID
import json
from pydantic import BaseModel, Field
from ..services.todo_service import todo_service
from ..models.todo import TodoCreate
from ..database.database import get_db_session
from ..auth.validation import validate_jwt_token


class CreateTodoParams(BaseModel):
    """
    Parameters for the create_todo MCP tool.
    """
    title: str = Field(..., description="The title of the todo item (1-255 characters)", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Optional description of the todo item (0-1000 characters)", max_length=1000)


def create_todo(user_token: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new todo item for the authenticated user.

    Args:
        user_token: JWT token for user authentication
        params: Parameters for creating the todo (title, description)

    Returns:
        Dict containing success status, todo data, and potential error
    """
    try:
        # Validate the JWT token to get user information
        token_data = validate_jwt_token(user_token)
        user_id = token_data.user_id

        # Validate parameters using Pydantic model
        validated_params = CreateTodoParams(**params)

        # Create the todo using the service
        with get_db_session() as db_session:
            todo_create = TodoCreate(
                title=validated_params.title,
                description=validated_params.description
            )

            # Create the todo for the authenticated user
            new_todo = todo_service.create_todo(
                db=db_session,
                obj_in=todo_create,
                user_id=user_id
            )

            # Return success response with todo data
            return {
                "success": True,
                "todo": {
                    "id": str(new_todo.id),
                    "title": new_todo.title,
                    "description": new_todo.description,
                    "completed": new_todo.completed,
                    "created_at": new_todo.created_at.isoformat(),
                    "updated_at": new_todo.updated_at.isoformat()
                }
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
    Example of how the create_todo function would be used.
    This is for demonstration purposes only.
    """
    # This would normally be called by the MCP framework with a valid token
    example_params = {
        "title": "Buy groceries",
        "description": "Milk, bread, eggs, and fruit"
    }

    # This token would come from the authenticated user session
    example_token = "example_jwt_token"

    result = create_todo(example_token, example_params)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    example_usage()