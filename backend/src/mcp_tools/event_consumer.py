"""Module for consuming task events from Kafka via Dapr."""

import asyncio
import json
from typing import Dict, Any, Callable, Optional
import httpx
from fastapi import HTTPException
from pydantic import BaseModel


class EventConsumer:
    """Service for consuming events from Kafka via Dapr pub/sub."""

    def __init__(self, dapr_http_port: int = 3500, dapr_grpc_port: int = 50001):
        self.dapr_http_port = dapr_http_port
        self.dapr_grpc_port = dapr_grpc_port
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.subscribers: Dict[str, Callable] = {}

    def subscribe_to_topic(self, topic_name: str, handler: Callable[[Dict[str, Any]], None]):
        """
        Subscribe to a topic with a handler function.

        Args:
            topic_name: Name of the topic to subscribe to
            handler: Function to handle incoming messages
        """
        self.subscribers[topic_name] = handler

    async def consume_event(self, topic: str, data: Dict[str, Any]):
        """
        Consume an event from a topic.

        Args:
            topic: Topic name
            data: Event data
        """
        if topic in self.subscribers:
            try:
                # Call the handler function with the event data
                await self.subscribers[topic](data)
            except Exception as e:
                print(f"Error processing event for topic '{topic}': {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to process event: {str(e)}"
                )
        else:
            print(f"No handler registered for topic: {topic}")

    async def create_subscription_endpoint(self, app):
        """
        Create a subscription endpoint for Dapr to call when events arrive.

        Args:
            app: FastAPI application instance
        """
        from fastapi import Request
        import logging

        @app.post("/dapr/subscribe")
        async def handle_dapr_subscription(request: Request):
            """Handle incoming events from Dapr pub/sub."""
            try:
                payload = await request.json()

                # Extract topic and data from Dapr event
                topic = payload.get('topic', '')
                data = payload.get('data', {})

                print(f"Received event from topic: {topic}")
                print(f"Event data: {data}")

                # Process the event based on topic
                await self.consume_event(topic, data)

                return {"success": True}

            except Exception as e:
                print(f"Error handling Dapr subscription: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to handle event subscription: {str(e)}"
                )

    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()


# Global instance for use in the application
event_consumer = EventConsumer()


# Example event handlers
async def handle_task_created_event(event_data: Dict[str, Any]):
    """Handle task created events."""
    print(f"Task created event received: {event_data}")
    # Add your business logic here for when a task is created


async def handle_task_updated_event(event_data: Dict[str, Any]):
    """Handle task updated events."""
    print(f"Task updated event received: {event_data}")
    # Add your business logic here for when a task is updated


async def handle_task_completed_event(event_data: Dict[str, Any]):
    """Handle task completed events."""
    print(f"Task completed event received: {event_data}")
    # Add your business logic here for when a task is completed


async def handle_task_deleted_event(event_data: Dict[str, Any]):
    """Handle task deleted events."""
    print(f"Task deleted event received: {event_data}")
    # Add your business logic here for when a task is deleted


# Register the handlers with the consumer
event_consumer.subscribe_to_topic("task-events", handle_task_created_event)