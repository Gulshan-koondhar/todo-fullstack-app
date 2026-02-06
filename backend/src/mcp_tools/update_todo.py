from typing import Dict, Any, Optional
from uuid import UUID
import json
from pydantic import BaseModel, Field
from ..services.todo_service import todo_service
from ..models.todo import TodoUpdate
from ..database.database import get_db_session
from ..auth.validation import validate_jwt_token, validate_todo_ownership


class UpdateTodoParams(BaseModel):
    """
    Parameters for the update_todo MCP tool.
    """
    todo_id: str = Field(..., description="The ID of the todo item to update")
    title: Optional[str] = Field(None, description="New title for the todo item (1-255 characters)", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="New description for the todo item (0-1000 characters)", max_length=1000)
    completed: Optional[bool] = Field(None, description="New completion status for the todo item")


def update_todo(user_token: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates an existing todo item for the authenticated user.

    Args:
        user_token: JWT token for user authentication
        params: Parameters for updating the todo (todo_id, title, description, completed)

    Returns:
        Dict containing success status, todo data, and potential error
    """
    try:
        # Validate the JWT token to get user information
        token_data = validate_jwt_token(user_token)
        user_id = token_data.user_id

        # Validate parameters using Pydantic model
        validated_params = UpdateTodoParams(**params)

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

            # Prepare the update object
            update_data = {}
            if validated_params.title is not None:
                update_data["title"] = validated_params.title
            if validated_params.description is not None:
                update_data["description"] = validated_params.description
            if validated_params.completed is not None:
                update_data["completed"] = validated_params.completed

            if not update_data:
                return {
                    "success": False,
                    "error": "No fields to update provided"
                }

            # Create the update object
            todo_update = TodoUpdate(**update_data)

            # Update the todo
            updated_todo = todo_service.update(
                db=db_session,
                db_obj=existing_todo,
                obj_in=todo_update
            )

            # Return success response with updated todo data
            return {
                "success": True,
                "todo": {
                    "id": str(updated_todo.id),
                    "title": updated_todo.title,
                    "description": updated_todo.description,
                    "completed": updated_todo.completed,
                    "created_at": updated_todo.created_at.isoformat(),
                    "updated_at": updated_todo.updated_at.isoformat()
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
    Example of how the update_todo function would be used.
    This is for demonstration purposes only.
    """
    # This would normally be called by the MCP framework with a valid token
    example_params = {
        "todo_id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Updated grocery list",
        "completed": False
    }

    # This token would come from the authenticated user session
    example_token = "example_jwt_token"

    result = update_todo(example_token, example_params)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    example_usage()