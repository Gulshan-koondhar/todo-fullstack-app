from sqlmodel import Session, select
from typing import List, Optional
from app.models.task import Task as TaskModel
from ..services.base_service import BaseService


class TaskServiceAdapter:
    """
    Adapter service to work with the Task model used by the main API,
    allowing the AI agent to interact with the same model as the API endpoints.
    """

    def __init__(self):
        # This service adapts to work with the Task model from app.models
        pass

    def get_tasks_by_user(self, db: Session, user_id: str, completed: Optional[bool] = None) -> List[TaskModel]:
        """
        Get all tasks for a specific user, optionally filtered by completion status.
        """
        statement = select(TaskModel).where(TaskModel.user_id == user_id)
        if completed is not None:
            statement = statement.where(TaskModel.completed == completed)
        return db.exec(statement).all()

    def create_task(self, db: Session, title: str, description: Optional[str] = None, user_id: str = None) -> TaskModel:
        """
        Create a new task for a specific user.
        """
        task = TaskModel(
            title=title,
            description=description,
            user_id=user_id,
            completed=False  # Default to not completed
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def toggle_completion(self, db: Session, task_id: str, user_id: str) -> Optional[TaskModel]:
        """
        Toggle the completion status of a task for a specific user.
        """
        task = db.exec(select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user_id)).first()
        if task:
            task.completed = not task.completed
            db.add(task)
            db.commit()
            db.refresh(task)
        return task

    def get_task(self, db: Session, id: str) -> Optional[TaskModel]:
        """
        Get a task by ID.
        """
        statement = select(TaskModel).where(TaskModel.id == id)
        return db.exec(statement).first()

    def update_task(self, db: Session, db_obj: TaskModel, title: str = None, description: str = None, completed: bool = None) -> TaskModel:
        """
        Update an existing task.
        """
        if title is not None:
            db_obj.title = title
        if description is not None:
            db_obj.description = description
        if completed is not None:
            db_obj.completed = completed
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_task(self, db: Session, id: str) -> TaskModel:
        """
        Remove a task by ID.
        """
        task = self.get_task(db, id)
        if task:
            db.delete(task)
            db.commit()
        return task


# Create a singleton instance for use throughout the application
task_service_adapter = TaskServiceAdapter()