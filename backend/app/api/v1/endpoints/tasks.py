from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel, Field, field_validator
from typing import Optional as OptionalType
from datetime import datetime
from uuid import UUID
import re

from app.db.session import get_db
from app.core.deps import get_current_user_id
from app.models.task import Task
from app.models.user import User
from src.mcp_tools.event_publisher import dapr_publisher


router = APIRouter()


# Pydantic models for request/response
class CreateTaskRequest(BaseModel):
    """Request schema for creating a task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: OptionalType[str] = Field(None, max_length=1000)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace only."""
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()


class UpdateTaskRequest(BaseModel):
    """Request schema for updating a task (partial updates allowed)."""

    title: OptionalType[str] = Field(None, min_length=1, max_length=200)
    description: OptionalType[str] = Field(None, max_length=1000)
    completed: OptionalType[bool] = None
    in_progress: OptionalType[bool] = Field(None, validation_alias="inProgress")  # Accept inProgress from frontend, map to in_progress in model

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: OptionalType[str]) -> OptionalType[str]:
        """Validate title is not empty or whitespace only if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip() if v else v

    model_config = {
        "populate_by_name": True
    }


class TaskResponse(BaseModel):
    """Response schema for a single task."""

    id: str
    title: str
    description: OptionalType[str]
    completed: bool
    in_progress: bool = Field(validation_alias="inProgress", serialization_alias="inProgress")
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class TasksListResponse(BaseModel):
    """Response schema for listing tasks."""

    tasks: list[TaskResponse]
    count: int


@router.get("", response_model=TasksListResponse)
async def list_tasks(
    user_id: str,
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    db: Session = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
):
    """
    List all tasks for the authenticated user.

    Tasks are sorted by creation date (newest first).
    """
    # Verify user_id matches token
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    # Build query with user_id filter
    query = db.query(Task).filter(Task.user_id == user_id)

    # Apply optional completed filter
    if completed is not None:
        query = query.filter(Task.completed == completed)

    # Order by created_at descending (newest first)
    tasks_list = query.order_by(Task.created_at.desc()).all()

    return {
        "tasks": tasks_list,
        "count": len(tasks_list),
    }


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    user_id: str,
    db: Session = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
):
    """
    Create a new task for the authenticated user.
    """
    # Verify user_id matches token
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    # Create task with user_id from token
    task = Task(
        title=request.title,
        description=request.description,
        user_id=user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    # Publish CREATE_TASK event to Kafka via Dapr
    try:
        await dapr_publisher.publish_create_task_event(
            task_id=str(task.id),
            user_id=user_id,
            title=request.title,
            description=request.description
        )
    except Exception as e:
        # Log the error but don't fail the task creation
        print(f"Warning: Failed to publish CREATE_TASK event: {str(e)}")

    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
):
    """
    Get a specific task by ID.

    Returns 404 if task doesn't exist or user doesn't own it
    (prevents enumeration attacks).
    """
    # Verify user_id matches token
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    task = db.query(Task).filter(
        and_(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


class TaskCompletionRequest(BaseModel):
    """Request schema for completing a task."""
    completed: bool = True


@router.put("/{task_id}/completion", response_model=TaskResponse)
async def complete_task(
    task_completion_request: TaskCompletionRequest,
    task_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
):
    """
    Mark a task as completed or incomplete.
    """
    # Verify user_id matches token
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    task = db.query(Task).filter(
        and_(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update completion status
    task.completed = task_completion_request.completed
    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    # Publish COMPLETE_TASK event to Kafka via Dapr if marking as completed
    try:
        if task_completion_request.completed:
            await dapr_publisher.publish_complete_task_event(
                task_id=task_id,
                user_id=user_id,
                completed_by=user_id
            )
    except Exception as e:
        # Log the error but don't fail the task completion
        print(f"Warning: Failed to publish COMPLETE_TASK event: {str(e)}")

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    request: UpdateTaskRequest,
    task_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
):
    """
    Update an existing task.

    Partial updates are supported - only provided fields will be updated.
    """
    # Verify user_id matches token
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    task = db.query(Task).filter(
        and_(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Store original values for the event
    original_title = task.title
    original_description = task.description

    # Update fields if provided
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    # Publish UPDATE_TASK event to Kafka via Dapr
    try:
        # Determine which fields were updated
        updated_fields = {}
        if request.title is not None:
            updated_fields['title'] = request.title
        if request.description is not None:
            updated_fields['description'] = request.description
        if request.completed is not None:
            updated_fields['completed'] = request.completed
        if request.in_progress is not None:
            updated_fields['in_progress'] = request.in_progress

        await dapr_publisher.publish_update_task_event(
            task_id=task_id,
            user_id=user_id,
            title=updated_fields.get('title'),
            description=updated_fields.get('description')
        )
    except Exception as e:
        # Log the error but don't fail the task update
        print(f"Warning: Failed to publish UPDATE_TASK event: {str(e)}")

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    user_id: str,
    db: Session = Depends(get_db),
    token_user_id: str = Depends(get_current_user_id),
):
    """
    Delete a task permanently.

    Returns 404 if task doesn't exist or user doesn't own it
    (prevents enumeration attacks).
    """
    # Verify user_id matches token
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    task = db.query(Task).filter(
        and_(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Publish DELETE_TASK event to Kafka via Dapr before deleting
    try:
        await dapr_publisher.publish_delete_task_event(
            task_id=task_id,
            user_id=user_id
        )
    except Exception as e:
        # Log the error but don't fail the task deletion
        print(f"Warning: Failed to publish DELETE_TASK event: {str(e)}")

    db.delete(task)
    db.commit()

    return None
