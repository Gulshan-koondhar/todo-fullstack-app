from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

from app.db.session import get_db
from app.core.deps import get_current_user_id
from app.models.user import User
from app.core.security import create_access_token


router = APIRouter()


class CreateUserRequest(BaseModel):
    """Request schema for creating a user account."""

    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8)

    @field_validator("email")
    @classmethod
    def valid_email(cls, v: str) -> str:
        """Validate email format."""
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least 1 uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least 1 lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least 1 number")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Password must contain at least 1 special character")
        return v


class LoginRequest(BaseModel):
    """Request schema for user login."""

    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    """Response schema for user operations."""

    id: str
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class AuthResponse(BaseModel):
    """Response schema for authentication operations."""

    user: UserResponse
    token: str


@router.post("/sign-up", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
):
    """
    Create a new user account and return JWT token.

    This endpoint is called by Better Auth when a user signs up.
    """
    # Check if email already exists
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create user
    user = User(
        email=request.email,
    )
    user.set_password(request.password)

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create JWT token with user info
    token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
        }
    )

    # Create user response
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

    return {
        "user": user_response.model_dump(mode="json"),
        "token": token,
    }


@router.post("/sign-in", response_model=AuthResponse)
async def sign_in(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Sign in a user and return JWT token.

    This endpoint is called by Better Auth when a user signs in.
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email.lower()).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT token with user info
    token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
        }
    )

    # Create user response
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

    return {
        "user": user_response.model_dump(mode="json"),
        "token": token,
    }


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    Get user by ID (for verification purposes).

    Returns 404 if user doesn't exist.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Get the current authenticated user's information.

    This endpoint extracts the user ID from the JWT token and returns the user details.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
