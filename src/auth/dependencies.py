"""
FastAPI authentication dependencies.

Provides dependency injection for protected routes requiring authentication.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_handler import decode_token, verify_token
from .user_store import UserStore
from .models import UserInDB, TokenData

# HTTP Bearer token scheme
security = HTTPBearer()


def get_user_store() -> UserStore:
    """
    Dependency to get UserStore instance.

    Returns:
        UserStore instance
    """
    return UserStore()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_store: UserStore = Depends(get_user_store)
) -> UserInDB:
    """
    Dependency to get current authenticated user.

    Args:
        credentials: HTTP Bearer credentials from request
        user_store: User storage instance

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode and verify token
    token_data: Optional[TokenData] = decode_token(token)

    if token_data is None:
        raise credentials_exception

    # Get user from database
    user = user_store.get_user_by_id(token_data.user_id)

    if user is None:
        raise credentials_exception

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user)
) -> UserInDB:
    """
    Dependency to get current active user.

    Args:
        current_user: Current user from get_current_user dependency

    Returns:
        Current active user

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_verified_user(
    current_user: UserInDB = Depends(get_current_user)
) -> UserInDB:
    """
    Dependency to get current verified user.

    Args:
        current_user: Current user from get_current_user dependency

    Returns:
        Current verified user

    Raises:
        HTTPException: If user is not verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )
    return current_user


def optional_authentication(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    user_store: UserStore = Depends(get_user_store)
) -> Optional[UserInDB]:
    """
    Optional authentication dependency.

    Returns user if valid token provided, None otherwise (no error raised).

    Args:
        credentials: Optional HTTP Bearer credentials
        user_store: User storage instance

    Returns:
        User if authenticated, None otherwise
    """
    if credentials is None:
        return None

    token = credentials.credentials

    # Try to decode token
    token_data = decode_token(token)
    if token_data is None:
        return None

    # Try to get user
    user = user_store.get_user_by_id(token_data.user_id)
    if user is None or not user.is_active:
        return None

    return user
