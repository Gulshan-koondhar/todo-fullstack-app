#!/usr/bin/env python3
"""
Debug script to test the API response and see the exact field names
"""

import requests
import json

# Test the API response format
def test_api_response():
    # Since we don't have a valid auth token, let's look at the swagger docs or test structure
    print("Testing API response structure...")

    # We can't make a real request without a valid token, but let's examine our model
    from app.models.task import Task
    from pydantic import BaseModel
    from typing import Optional
    from datetime import datetime

    # Let's create a test response using the same structure as our TaskResponse model
    from app.api.v1.endpoints.tasks import TaskResponse

    # Simulate a task object
    sample_task_data = {
        "id": "test-123",
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
        "in_progress": True,  # This is how it's stored in the database
        "user_id": "user-123",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    # Create a response object using our model
    try:
        task_response = TaskResponse(**sample_task_data)
        print("TaskResponse model created successfully")

        # Convert to dict to see how it serializes
        serialized = task_response.model_dump()
        print(f"Serialized response: {json.dumps(serialized, indent=2, default=str)}")

        # Check with by_alias to see if aliases are working
        aliased = task_response.model_dump(by_alias=True)
        print(f"Serialized with aliases: {json.dumps(aliased, indent=2, default=str)}")

    except Exception as e:
        print(f"Error creating TaskResponse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_response()