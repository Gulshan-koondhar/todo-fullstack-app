from typing import Dict, Any, List
import os
from dotenv import load_dotenv
from ..mcp_tools.create_todo import create_todo
from ..mcp_tools.validation import validate_create_todo_params

load_dotenv()

class TodoAIAgent:
    """
    AI agent for handling natural language todo operations.
    This agent uses MCP tools to execute todo operations based on natural language input.
    """

    def __init__(self):
        self.tools = {
            "create_todo": self._execute_create_todo,
        }

        # Add more tools as they are implemented
        self._initialize_tools()

    def _initialize_tools(self):
        """
        Initialize all available MCP tools for the agent.
        """
        # Import and register additional tools as they become available
        try:
            from ..mcp_tools.get_todos import get_todos
            from ..mcp_tools.validation import validate_get_todos_params

            def wrapped_get_todos(user_token, params):
                # Validate parameters
                validation_result = validate_get_todos_params(params)

                if not validation_result["valid"]:
                    return {
                        "success": False,
                        "error": f"Invalid parameters: {'; '.join(validation_result['errors'])}"
                    }

                # Execute the tool with validated parameters
                return get_todos(user_token, validation_result["params"])

            self.tools["get_todos"] = wrapped_get_todos
        except ImportError:
            pass  # Tool not yet implemented

        try:
            from ..mcp_tools.update_todo import update_todo
            from ..mcp_tools.validation import validate_update_todo_params

            def wrapped_update_todo(user_token, params):
                # Validate parameters
                validation_result = validate_update_todo_params(params)

                if not validation_result["valid"]:
                    return {
                        "success": False,
                        "error": f"Invalid parameters: {'; '.join(validation_result['errors'])}"
                    }

                # Execute the tool with validated parameters
                return update_todo(user_token, validation_result["params"])

            self.tools["update_todo"] = wrapped_update_todo
        except ImportError:
            pass  # Tool not yet implemented

        try:
            from ..mcp_tools.delete_todo import delete_todo
            from ..mcp_tools.validation import validate_delete_todo_params

            def wrapped_delete_todo(user_token, params):
                # Validate parameters
                validation_result = validate_delete_todo_params(params)

                if not validation_result["valid"]:
                    return {
                        "success": False,
                        "error": f"Invalid parameters: {'; '.join(validation_result['errors'])}"
                    }

                # Execute the tool with validated parameters
                return delete_todo(user_token, validation_result["params"])

            self.tools["delete_todo"] = wrapped_delete_todo
        except ImportError:
            pass  # Tool not yet implemented

        try:
            from ..mcp_tools.toggle_todo_completion import toggle_todo_completion
            from ..mcp_tools.validation import validate_toggle_completion_params

            def wrapped_toggle_todo_completion(user_token, params):
                # Validate parameters
                validation_result = validate_toggle_completion_params(params)

                if not validation_result["valid"]:
                    return {
                        "success": False,
                        "error": f"Invalid parameters: {'; '.join(validation_result['errors'])}"
                    }

                # Execute the tool with validated parameters
                return toggle_todo_completion(user_token, validation_result["params"])

            self.tools["toggle_todo_completion"] = wrapped_toggle_todo_completion
        except ImportError:
            pass  # Tool not yet implemented

    def _execute_create_todo(self, user_token: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the create_todo tool with validation.
        """
        # Validate parameters
        validation_result = validate_create_todo_params(params)

        if not validation_result["valid"]:
            return {
                "success": False,
                "error": f"Invalid parameters: {'; '.join(validation_result['errors'])}"
            }

        # Execute the tool
        return create_todo(user_token, validation_result["params"])

    def process_request(self, user_token: str, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request by executing the specified tool.

        Args:
            user_token: JWT token for user authentication
            tool_name: Name of the MCP tool to execute
            params: Parameters for the tool

        Returns:
            Dict containing the result of the tool execution
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not available"
            }

        try:
            # Execute the tool
            result = self.tools[tool_name](user_token, params)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing tool '{tool_name}': {str(e)}"
            }

    def get_available_tools(self) -> List[str]:
        """
        Get a list of available tools.

        Returns:
            List of available tool names
        """
        return list(self.tools.keys())


# Create a singleton instance of the agent
todo_agent = TodoAIAgent()


def execute_mcp_tool(user_token: str, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute an MCP tool through the AI agent.

    Args:
        user_token: JWT token for user authentication
        tool_name: Name of the MCP tool to execute
        params: Parameters for the tool

    Returns:
        Dict containing the result of the tool execution
    """
    return todo_agent.process_request(user_token, tool_name, params)