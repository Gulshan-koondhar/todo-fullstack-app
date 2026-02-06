from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoPublic
from .base_service import BaseService


class TodoService(BaseService[Todo, TodoCreate, TodoUpdate]):
    """
    Service class for handling todo-related operations.
    """
    def __init__(self):
        super().__init__(Todo)

    def get_todos_by_user(self, db: Session, user_id: str, completed: Optional[bool] = None) -> List[Todo]:
        """
        Get all todos for a specific user, optionally filtered by completion status.
        """
        statement = select(Todo).where(Todo.user_id == user_id)
        if completed is not None:
            statement = statement.where(Todo.completed == completed)
        return db.exec(statement).all()

    def create_todo(self, db: Session, obj_in: TodoCreate, user_id: str) -> Todo:
        """
        Create a new todo for a specific user.
        """
        # Create Todo object with all required fields including user_id
        todo_data = obj_in.model_dump()
        todo_data['user_id'] = user_id
        todo = Todo(**todo_data)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def toggle_completion(self, db: Session, todo_id: str, user_id: str) -> Optional[Todo]:
        """
        Toggle the completion status of a todo for a specific user.
        """
        todo = db.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)).first()
        if todo:
            todo.completed = not todo.completed
            db.add(todo)
            db.commit()
            db.refresh(todo)
        return todo

    def to_public(self, todo: Todo) -> TodoPublic:
        """
        Convert a Todo model to a TodoPublic model for safe serialization.
        """
        return TodoPublic(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )


# Create a singleton instance for use throughout the application
todo_service = TodoService()