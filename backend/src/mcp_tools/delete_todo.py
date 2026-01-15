from typing import Dict, Any
from uuid import UUID
import json
from pydantic import BaseModel, Field
from ..services.todo_service import todo_service
from ..database.database import get_db_session
from ..auth.validation import validate_jwt_token, validate_todo_ownership


class DeleteTodoParams(BaseModel):
    """
    Parameters for the delete_todo MCP tool.
    """
    todo_id: str = Field(..., description="The ID of the todo item to delete")


def delete_todo(user_token: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deletes an existing todo item for the authenticated user.

    Args:
        user_token: JWT token for user authentication
        params: Parameters for deleting the todo (todo_id)

    Returns:
        Dict containing success status, message, and potential error
    """
    try:
        # Validate the JWT token to get user information
        token_data = validate_jwt_token(user_token)
        user_id = token_data.user_id

        # Validate parameters using Pydantic model
        validated_params = DeleteTodoParams(**params)

        # Convert todo_id string to UUID
        from uuid import UUID
        try:
            todo_uuid = UUID(validated_params.todo_id)
        except ValueError:
            return {
                "success": False,
                "error": f"Invalid todo_id format: {validated_params.todo_id}"
            }

        # Get the todo to check ownership
        with get_db_session() as db_session:
            existing_todo = todo_service.get(db_session, todo_uuid)

            if not existing_todo:
                return {
                    "success": False,
                    "error": f"Todo with ID {validated_params.todo_id} not found"
                }

            # Validate that the user owns this todo
            validate_todo_ownership(existing_todo.user_id, token_data)

            # Remove the todo
            deleted_todo = todo_service.remove(db=db_session, id=todo_uuid)

            if deleted_todo:
                # Return success response with confirmation message
                return {
                    "success": True,
                    "message": f"Todo '{deleted_todo.title}' has been deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to delete todo with ID {validated_params.todo_id}"
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
    Example of how the delete_todo function would be used.
    This is for demonstration purposes only.
    """
    # This would normally be called by the MCP framework with a valid token
    example_params = {
        "todo_id": "123e4567-e89b-12d3-a456-426614174000"
    }

    # This token would come from the authenticated user session
    example_token = "example_jwt_token"

    result = delete_todo(example_token, example_params)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    example_usage()