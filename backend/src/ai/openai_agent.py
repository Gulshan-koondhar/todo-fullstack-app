from typing import Dict, Any, List, Optional
import os
import json
from openai import OpenAI
from pydantic import BaseModel, Field
from ..services.todo_service import todo_service
from ..database.database import get_db_session
from ..models.todo import TodoCreate, TodoUpdate


class OpenAIAgent:
    """
    AI agent for handling natural language todo operations using OpenAI API.
    This agent uses OpenRouter's free models to execute todo operations based on natural language input.
    """

    def __init__(self):
        # Use OpenRouter API endpoint
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY", "sk-openrouter-placeholder")
        )

        # Define the model to use (free model from OpenRouter)
        self.model = os.getenv("AI_MODEL", "openai/gpt-3.5-turbo")

        # Define available tools for the agent
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_todo",
                    "description": "Create a new todo item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Title of the todo"},
                            "description": {"type": "string", "description": "Description of the todo (optional)"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_todo",
                    "description": "Update an existing todo item. You can identify the todo by either its ID or title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {"type": "string", "description": "ID of the todo to update (alternative to title)"},
                            "title": {"type": "string", "description": "Title of the existing todo to update (alternative to todo_id)"},
                            "new_title": {"type": "string", "description": "New title of the todo (optional)"},
                            "description": {"type": "string", "description": "New description of the todo (optional)"},
                            "completed": {"type": "boolean", "description": "New completion status (optional)"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_todo",
                    "description": "Delete a todo item. You can identify the todo by either its ID or title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {"type": "string", "description": "ID of the todo to delete (alternative to title)"},
                            "title": {"type": "string", "description": "Title of the existing todo to delete (alternative to todo_id)"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_todos",
                    "description": "Get all todo items for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "toggle_todo_completion",
                    "description": "Toggle the completion status of a todo item. You can identify the todo by either its ID or title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {"type": "string", "description": "ID of the todo to toggle (alternative to title)"},
                            "title": {"type": "string", "description": "Title of the existing todo to toggle completion status (alternative to todo_id)"}
                        }
                    }
                }
            }
        ]

    def _validate_todo_id(self, todo_id: str) -> bool:
        """Validate that the todo_id is a proper UUID string."""
        import uuid
        try:
            uuid.UUID(todo_id)
            return True
        except ValueError:
            return False

    def _create_todo(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new todo item."""
        try:
            # Validate parameters
            title = params.get("title")
            description = params.get("description")

            if not title or not title.strip():
                return {"success": False, "error": "Title is required and cannot be empty"}

            # Create the todo
            todo_create = TodoCreate(
                title=title.strip(),
                description=description.strip() if description else None
            )

            with get_db_session() as db_session:
                new_todo = todo_service.create_todo(db_session, obj_in=todo_create, user_id=user_id)

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
            return {"success": False, "error": str(e)}

    def _update_todo(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing todo item."""
        try:
            # Validate parameters
            todo_id = params.get("todo_id")
            if not todo_id or not self._validate_todo_id(todo_id):
                return {"success": False, "error": "Valid todo_id is required"}

            # Prepare update data
            update_data = {}
            # Use 'new_title' if provided, otherwise use 'title' (for backward compatibility)
            if "new_title" in params and params["new_title"] is not None:
                update_data["title"] = params["new_title"].strip()
            elif "title" in params and params["title"] is not None:
                update_data["title"] = params["title"].strip()
            if "description" in params and params["description"] is not None:
                update_data["description"] = params["description"].strip()
            if "completed" in params and params["completed"] is not None:
                update_data["completed"] = params["completed"]

            if not update_data:
                return {"success": False, "error": "At least one field to update is required"}

            # Create update object
            todo_update = TodoUpdate(**update_data)

            with get_db_session() as db_session:
                # Get existing todo to check ownership
                existing_todo = todo_service.get(db_session, id=todo_id)
                if not existing_todo:
                    return {"success": False, "error": f"Todo with ID {todo_id} not found"}

                if str(existing_todo.user_id) != str(user_id):
                    return {"success": False, "error": "Access denied: You don't own this todo"}

                # Update the todo using the base service update method
                updated_todo = todo_service.update(
                    db=db_session,
                    db_obj=existing_todo,
                    obj_in=todo_update
                )

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
            return {"success": False, "error": str(e)}

    def _delete_todo(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a todo item."""
        try:
            # Validate parameters
            todo_id = params.get("todo_id")
            if not todo_id or not self._validate_todo_id(todo_id):
                return {"success": False, "error": "Valid todo_id is required"}

            with get_db_session() as db_session:
                # Get existing todo to check ownership
                existing_todo = todo_service.get(db_session, id=todo_id)
                if not existing_todo:
                    return {"success": False, "error": f"Todo with ID {todo_id} not found"}

                if str(existing_todo.user_id) != str(user_id):
                    return {"success": False, "error": "Access denied: You don't own this todo"}

                # Delete the todo
                deleted_todo = todo_service.remove(db_session, id=todo_id)

                return {
                    "success": True,
                    "message": f"Todo '{deleted_todo.title}' has been deleted successfully"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _get_todos(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get all todo items for the user."""
        try:
            with get_db_session() as db_session:
                todos = todo_service.get_todos_by_user(db_session, user_id=user_id)

                return {
                    "success": True,
                    "todos": [
                        {
                            "id": str(todo.id),
                            "title": todo.title,
                            "description": todo.description,
                            "completed": todo.completed,
                            "created_at": todo.created_at.isoformat(),
                            "updated_at": todo.updated_at.isoformat()
                        }
                        for todo in todos
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _toggle_todo_completion(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Toggle the completion status of a todo item."""
        try:
            # Validate parameters
            todo_id = params.get("todo_id")
            if not todo_id or not self._validate_todo_id(todo_id):
                return {"success": False, "error": "Valid todo_id is required"}

            with get_db_session() as db_session:
                # Get existing todo to check ownership
                existing_todo = todo_service.get(db_session, id=todo_id)
                if not existing_todo:
                    return {"success": False, "error": f"Todo with ID {todo_id} not found"}

                if str(existing_todo.user_id) != str(user_id):
                    return {"success": False, "error": "Access denied: You don't own this todo"}

                # Toggle completion status using the service method
                toggled_todo = todo_service.toggle_completion(db_session, todo_id=todo_id, user_id=user_id)

                if not toggled_todo:
                    return {"success": False, "error": f"Failed to toggle completion for todo with ID {todo_id}"}

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
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _find_todo_by_title(self, user_id: str, title: str) -> Optional[Dict[str, Any]]:
        """Find a todo by title for the user."""
        with get_db_session() as db_session:
            todos = todo_service.get_todos_by_user(db_session, user_id=user_id)
            # Find case-insensitive partial match
            for todo in todos:
                if title.lower() in todo.title.lower():
                    return {
                        "id": str(todo.id),
                        "title": todo.title,
                        "completed": todo.completed
                    }
        return None

    def _execute_tool(self, tool_name: str, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the specified tool with the given parameters."""
        # Handle tools that need to find a todo by title first
        if tool_name in ["update_todo", "delete_todo", "toggle_todo_completion"]:
            # Check if the user provided a title instead of an ID
            if "title" in params and "todo_id" not in params:
                # Find the todo by title
                found_todo = self._find_todo_by_title(user_id, params["title"])
                if found_todo:
                    # Use the found todo's ID and merge other params
                    updated_params = {"todo_id": found_todo["id"]}
                    updated_params.update({k: v for k, v in params.items() if k != "title"})
                    params = updated_params
                else:
                    return {"success": False, "error": f"Todo with title '{params['title']}' not found"}

        tool_functions = {
            "create_todo": self._create_todo,
            "update_todo": self._update_todo,
            "delete_todo": self._delete_todo,
            "get_todos": self._get_todos,
            "toggle_todo_completion": self._toggle_todo_completion
        }

        if tool_name not in tool_functions:
            return {"success": False, "error": f"Tool '{tool_name}' not available"}

        try:
            return tool_functions[tool_name](user_id, params)
        except Exception as e:
            return {"success": False, "error": f"Error executing tool '{tool_name}': {str(e)}"}

    def process_natural_language_request(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """
        Process a natural language request using the OpenAI agent.

        Args:
            user_input: Natural language request from the user
            user_id: User ID for authentication

        Returns:
            Dict containing the result of the operation
        """
        try:
            # Create the message for the AI
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful todo assistant. You can create, update, delete, and manage todo items.
                    Analyze the user's request and determine which function to call and with what parameters.
                    When a user refers to a task by its title (e.g., "Complete the task 'Buy groceries'"),
                    use the title parameter in update_todo, delete_todo, or toggle_todo_completion functions.
                    Only use the available functions to fulfill the user's request."""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]

            # Call the OpenAI API with function calling
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            # Check if the response contains tool calls
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Execute each tool call
                results = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    result = self._execute_tool(function_name, user_id, function_args)
                    results.append({
                        "tool_call": function_name,
                        "result": result
                    })

                return {
                    "success": True,
                    "results": results,
                    "message": f"Executed {len(results)} operations successfully"
                }
            else:
                # If no tool calls were made, return the AI's response
                return {
                    "success": True,
                    "message": response_message.content or "Operation completed",
                    "needs_clarification": True
                }

        except Exception as e:
            return {"success": False, "error": f"Error processing request: {str(e)}"}


# Create a singleton instance of the agent
openai_agent = OpenAIAgent()


def process_openai_request(user_input: str, user_id: str) -> Dict[str, Any]:
    """
    Process a natural language request through the OpenAI agent.

    Args:
        user_input: Natural language request from the user
        user_id: User ID for authentication

    Returns:
        Dict containing the result of the operation
    """
    return openai_agent.process_natural_language_request(user_input, user_id)