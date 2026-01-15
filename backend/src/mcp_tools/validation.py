from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError, validator
import re


class MCPToolValidator:
    """
    Validator class for MCP tool parameters.
    Provides common validation functions for different types of tools.
    """

    @staticmethod
    def validate_todo_title(title: str) -> bool:
        """
        Validate todo title length and content.

        Args:
            title: The title to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not title or not isinstance(title, str):
            return False
        if len(title.strip()) < 1 or len(title.strip()) > 255:
            return False
        return True

    @staticmethod
    def validate_todo_description(description: Optional[str]) -> bool:
        """
        Validate todo description length and content.

        Args:
            description: The description to validate (can be None)

        Returns:
            bool: True if valid, False otherwise
        """
        if description is None:
            return True
        if not isinstance(description, str):
            return False
        if len(description) > 1000:
            return False
        return True

    @staticmethod
    def validate_todo_id(todo_id: str) -> bool:
        """
        Validate todo ID format (UUID).

        Args:
            todo_id: The todo ID to validate

        Returns:
            bool: True if valid, False otherwise
        """
        import uuid
        try:
            uuid.UUID(todo_id)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        """
        Validate user ID format (UUID).

        Args:
            user_id: The user ID to validate

        Returns:
            bool: True if valid, False otherwise
        """
        import uuid
        try:
            uuid.UUID(user_id)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_completion_status(completed: Optional[bool]) -> bool:
        """
        Validate completion status.

        Args:
            completed: The completion status to validate (can be None)

        Returns:
            bool: True if valid, False otherwise
        """
        if completed is None:
            return True
        return isinstance(completed, bool)


def validate_create_todo_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters for create_todo tool.

    Args:
        params: Parameters to validate

    Returns:
        Dict with validation result and cleaned parameters or error
    """
    errors = []

    # Check required fields
    if 'title' not in params:
        errors.append("Missing required field: 'title'")
    else:
        title = params['title']
        if not MCPToolValidator.validate_todo_title(title):
            errors.append(f"Invalid title: must be 1-255 characters, got {len(title) if isinstance(title, str) else 'non-string'}")

    # Validate optional description
    if 'description' in params:
        description = params['description']
        if not MCPToolValidator.validate_todo_description(description):
            errors.append(f"Invalid description: must be string with max 1000 characters, got {len(description) if isinstance(description, str) else 'non-string'}")

    if errors:
        return {
            "valid": False,
            "errors": errors,
            "params": None
        }

    # Clean and return parameters
    cleaned_params = {
        "title": params['title'].strip() if isinstance(params['title'], str) else params['title'],
        "description": params.get('description', '').strip() if params.get('description') else None
    }

    return {
        "valid": True,
        "errors": [],
        "params": cleaned_params
    }


def validate_get_todos_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters for get_todos tool.

    Args:
        params: Parameters to validate

    Returns:
        Dict with validation result and cleaned parameters or error
    """
    errors = []

    # Validate optional completed parameter
    if 'completed' in params:
        completed = params['completed']
        if not MCPToolValidator.validate_completion_status(completed):
            errors.append("Invalid 'completed' parameter: must be boolean")

    if errors:
        return {
            "valid": False,
            "errors": errors,
            "params": None
        }

    # Clean and return parameters
    cleaned_params = {
        "completed": params.get('completed')
    }

    return {
        "valid": True,
        "errors": [],
        "params": cleaned_params
    }


def validate_update_todo_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters for update_todo tool.

    Args:
        params: Parameters to validate

    Returns:
        Dict with validation result and cleaned parameters or error
    """
    errors = []

    # Check required fields
    if 'todo_id' not in params:
        errors.append("Missing required field: 'todo_id'")
    else:
        todo_id = params['todo_id']
        if not MCPToolValidator.validate_todo_id(todo_id):
            errors.append(f"Invalid todo_id: must be a valid UUID")

    # Validate optional fields
    if 'title' in params:
        title = params['title']
        if not MCPToolValidator.validate_todo_title(title):
            errors.append(f"Invalid title: must be 1-255 characters, got {len(title) if isinstance(title, str) else 'non-string'}")

    if 'description' in params:
        description = params['description']
        if not MCPToolValidator.validate_todo_description(description):
            errors.append(f"Invalid description: must be string with max 1000 characters")

    if 'completed' in params:
        completed = params['completed']
        if not MCPToolValidator.validate_completion_status(completed):
            errors.append("Invalid 'completed' parameter: must be boolean")

    if errors:
        return {
            "valid": False,
            "errors": errors,
            "params": None
        }

    # Clean and return parameters
    cleaned_params = {
        "todo_id": params['todo_id'],
        "title": params.get('title', '').strip() if params.get('title') else None,
        "description": params.get('description', '').strip() if params.get('description') else None,
        "completed": params.get('completed')
    }

    return {
        "valid": True,
        "errors": [],
        "params": cleaned_params
    }


def validate_delete_todo_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters for delete_todo tool.

    Args:
        params: Parameters to validate

    Returns:
        Dict with validation result and cleaned parameters or error
    """
    errors = []

    # Check required fields
    if 'todo_id' not in params:
        errors.append("Missing required field: 'todo_id'")
    else:
        todo_id = params['todo_id']
        if not MCPToolValidator.validate_todo_id(todo_id):
            errors.append(f"Invalid todo_id: must be a valid UUID")

    if errors:
        return {
            "valid": False,
            "errors": errors,
            "params": None
        }

    # Clean and return parameters
    cleaned_params = {
        "todo_id": params['todo_id']
    }

    return {
        "valid": True,
        "errors": [],
        "params": cleaned_params
    }


def validate_toggle_completion_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters for toggle_todo_completion tool.

    Args:
        params: Parameters to validate

    Returns:
        Dict with validation result and cleaned parameters or error
    """
    errors = []

    # Check required fields
    if 'todo_id' not in params:
        errors.append("Missing required field: 'todo_id'")
    else:
        todo_id = params['todo_id']
        if not MCPToolValidator.validate_todo_id(todo_id):
            errors.append(f"Invalid todo_id: must be a valid UUID")

    if errors:
        return {
            "valid": False,
            "errors": errors,
            "params": None
        }

    # Clean and return parameters
    cleaned_params = {
        "todo_id": params['todo_id']
    }

    return {
        "valid": True,
        "errors": [],
        "params": cleaned_params
    }