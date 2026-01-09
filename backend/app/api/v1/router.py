from fastapi import APIRouter
from app.api.v1.endpoints import tasks, auth

api_router = APIRouter()

# Include task endpoints
api_router.include_router(
    tasks.router,
    prefix="/users/{user_id}/tasks",
    tags=["tasks"],
)

# Include auth endpoints
api_router.include_router(
    auth.router,
    prefix="/users",
    tags=["users"],
)
