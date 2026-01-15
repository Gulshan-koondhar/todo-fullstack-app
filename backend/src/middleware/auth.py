from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
import jwt
from jwt import PyJWTError
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-here-32-chars-min")


class TokenData(BaseModel):
    """
    Model to hold token data including user ID.
    """
    user_id: UUID
    exp: Optional[datetime] = None


def verify_token(token: str) -> TokenData:
    """
    Verify JWT token and return token data.

    Args:
        token: The JWT token string

    Returns:
        TokenData: Contains user_id and expiration

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        exp: int = payload.get("exp")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: no user ID")

        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token expired")

        return TokenData(user_id=UUID(user_id), exp=datetime.fromtimestamp(exp) if exp else None)

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Get current user from JWT token in Authorization header.

    Args:
        credentials: HTTP authorization credentials from FastAPI security dependency

    Returns:
        TokenData: Contains user_id and expiration
    """
    token_data = verify_token(credentials.credentials)
    return token_data