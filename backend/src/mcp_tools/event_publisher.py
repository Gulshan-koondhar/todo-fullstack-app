"""Module for publishing task events to Kafka via Dapr."""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4
from pydantic import BaseModel, Field

import httpx
from fastapi import HTTPException


class TaskEventPayload(BaseModel):
    """Base payload for task events."""
    pass


class CreateTaskPayload(TaskEventPayload):
    """Payload for CREATE_TASK events."""
    title: str
    description: Optional[str] = None
    created_at: str


class UpdateTaskPayload(TaskEventPayload):
    """Payload for UPDATE_TASK events."""
    title: Optional[str] = None
    description: Optional[str] = None
    updated_at: str


class CompleteTaskPayload(TaskEventPayload):
    """Payload for COMPLETE_TASK events."""
    completed_at: str
    completed_by: str


class DeleteTaskPayload(TaskEventPayload):
    """Payload for DELETE_TASK events."""
    deleted_at: str


class TaskEvent(BaseModel):
    """Task event structure for publishing to Kafka via Dapr."""
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    task_id: str
    user_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    payload: Dict[str, Any]
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    version: str = "1.0"


class DaprEventPublisher:
    """Service for publishing events to Kafka via Dapr pub/sub."""

    def __init__(self, dapr_http_port: int = 3500, dapr_grpc_port: int = 50001):
        self.dapr_http_port = dapr_http_port
        self.dapr_grpc_port = dapr_grpc_port
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def publish_event(self, event: TaskEvent, pubsub_name: str = "kafka-pubsub"):
        """
        Publish a task event to Kafka via Dapr pub/sub.

        Args:
            event: TaskEvent to publish
            pubsub_name: Name of the Dapr pub/sub component

        Returns:
            bool: True if event was published successfully
        """
        try:
            # Construct the Dapr pub/sub endpoint URL
            url = f"http://localhost:{self.dapr_http_port}/v1.0/publish/{pubsub_name}/task-events"

            # Prepare the request data
            # Dapr expects the message in the 'data' field
            request_data = {
                "data": event.dict(),
                "datacontenttype": "application/json",
                "topic": "task-events"
            }

            # Send the event to Dapr pub/sub
            response = await self.http_client.post(
                url,
                json=request_data,
                headers={
                    "Content-Type": "application/json"
                }
            )

            if response.status_code in [200, 204]:
                print(f"Event published successfully: {event.event_type} for task {event.task_id}")
                return True
            else:
                print(f"Failed to publish event: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error publishing event: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to publish task event: {str(e)}"
            )

    async def publish_create_task_event(self, task_id: str, user_id: str, title: str, description: Optional[str] = None):
        """Publish a CREATE_TASK event."""
        payload = CreateTaskPayload(
            title=title,
            description=description,
            created_at=datetime.utcnow().isoformat()
        )

        event = TaskEvent(
            event_type="CREATE_TASK",
            task_id=task_id,
            user_id=user_id,
            payload=payload.dict()
        )

        return await self.publish_event(event)

    async def publish_update_task_event(self, task_id: str, user_id: str, title: Optional[str] = None,
                                      description: Optional[str] = None):
        """Publish an UPDATE_TASK event."""
        payload = UpdateTaskPayload(
            title=title,
            description=description,
            updated_at=datetime.utcnow().isoformat()
        )

        event = TaskEvent(
            event_type="UPDATE_TASK",
            task_id=task_id,
            user_id=user_id,
            payload=payload.dict()
        )

        return await self.publish_event(event)

    async def publish_complete_task_event(self, task_id: str, user_id: str, completed_by: str):
        """Publish a COMPLETE_TASK event."""
        payload = CompleteTaskPayload(
            completed_at=datetime.utcnow().isoformat(),
            completed_by=completed_by
        )

        event = TaskEvent(
            event_type="COMPLETE_TASK",
            task_id=task_id,
            user_id=user_id,
            payload=payload.dict()
        )

        return await self.publish_event(event)

    async def publish_delete_task_event(self, task_id: str, user_id: str):
        """Publish a DELETE_TASK event."""
        payload = DeleteTaskPayload(
            deleted_at=datetime.utcnow().isoformat()
        )

        event = TaskEvent(
            event_type="DELETE_TASK",
            task_id=task_id,
            user_id=user_id,
            payload=payload.dict()
        )

        return await self.publish_event(event)

    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()


# Global instance for use in endpoints
dapr_publisher = DaprEventPublisher()