from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt


# Security scheme
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Extract user_id from JWT token in Authorization header.

    Args:
        credentials: HTTP Bearer token credentials

    Returns:
        The user_id (UUID) from the token's 'sub' claim

    Raises:
        HTTPException: If token is invalid or missing user_id
    """
    token = credentials.credentials

    try:
        from app.core.config import settings
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def verify_path_user_matches_token(
    path_user_id: str,
    token_user_id: str = Depends(get_current_user_id),
) -> str:
    """
    Verify that the user_id in the path matches the authenticated user.

    This ensures users can only access their own resources.

    Args:
        path_user_id: User ID from the URL path
        token_user_id: User ID extracted from JWT token

    Returns:
        The verified user_id

    Raises:
        HTTPException: If user IDs don't match
    """
    if path_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )
    return path_user_id
