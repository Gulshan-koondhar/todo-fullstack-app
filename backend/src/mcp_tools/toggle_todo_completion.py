from typing import Dict, Any
from uuid import UUID
import json
from pydantic import BaseModel, Field
from ..services.todo_service import todo_service
from ..database.database import get_db_session
from ..auth.validation import validate_jwt_token, validate_todo_ownership


class ToggleTodoCompletionParams(BaseModel):
    """
    Parameters for the toggle_todo_completion MCP tool.
    """
    todo_id: str = Field(..., description="The ID of the todo item to toggle")


def toggle_todo_completion(user_token: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Toggles the completion status of an existing todo item for the authenticated user.

    Args:
        user_token: JWT token for user authentication
        params: Parameters for toggling the todo completion status (todo_id)

    Returns:
        Dict containing success status, todo data, and potential error
    """
    try:
        # Validate the JWT token to get user information
        token_data = validate_jwt_token(user_token)
        user_id = token_data.user_id

        # Validate parameters using Pydantic model
        validated_params = ToggleTodoCompletionParams(**params)

        # Convert todo_id string to UUID
        from uuid import UUID
        try:
            todo_uuid = UUID(validated_params.todo_id)
        except ValueError:
            return {
                "success": False,
                "error": f"Invalid todo_id format: {validated_params.todo_id}"
            }

        # Toggle the completion status
        with get_db_session() as db_session:
            # Get the todo to check ownership
            existing_todo = todo_service.get(db_session, todo_uuid)

            if not existing_todo:
                return {
                    "success": False,
                    "error": f"Todo with ID {validated_params.todo_id} not found"
                }

            # Validate that the user owns this todo
            validate_todo_ownership(existing_todo.user_id, token_data)

            # Toggle the completion status
            toggled_todo = todo_service.toggle_completion(
                db=db_session,
                todo_id=todo_uuid,
                user_id=user_id
            )

            if toggled_todo:
                # Return success response with updated todo data
                return {
                    "success": True,
                    "todo": {
                        "id": str(toggled_todo.id),
                        "title": toggled_todo.title,
                        "description": toggled_todo.description,
                        "completed": toggled_todo.completed,
                        "created_at": toggled_todo.created_at.isoformat(),
                        "updated_at": toggled_todo.updated_at.isoformat()
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to toggle completion status for todo with ID {validated_params.todo_id}"
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
    Example of how the toggle_todo_completion function would be used.
    This is for demonstration purposes only.
    """
    # This would normally be called by the MCP framework with a valid token
    example_params = {
        "todo_id": "123e4567-e89b-12d3-a456-426614174000"
    }

    # This token would come from the authenticated user session
    example_token = "example_jwt_token"

    result = toggle_todo_completion(example_token, example_params)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    example_usage()