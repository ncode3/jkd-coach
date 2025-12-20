"""
Authentication routes for user registration and login.

Provides endpoints for user management and JWT token generation.
"""
from datetime import timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from .models import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    UserInDB
)
from .jwt_handler import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from .user_store import UserStore
from .dependencies import get_user_store, get_current_user, get_current_active_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    user_store: UserStore = Depends(get_user_store)
) -> UserResponse:
    """
    Register a new user.

    Creates a new user account with the provided credentials.

    Args:
        user_data: User registration data
        user_store: User storage instance

    Returns:
        Created user information (without sensitive data)

    Raises:
        HTTPException: If username or email already exists
    """
    try:
        user = user_store.create_user(user_data)

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at,
            is_active=user.is_active,
            is_verified=user.is_verified
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    user_store: UserStore = Depends(get_user_store)
) -> Token:
    """
    Login and get access token.

    Authenticates user and returns JWT access token.

    Args:
        credentials: User login credentials
        user_store: User storage instance

    Returns:
        JWT access token and metadata

    Raises:
        HTTPException: If credentials are invalid or user inactive
    """
    # Get user by username
    user = user_store.get_user_by_username(credentials.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserInDB = Depends(get_current_active_user)
) -> UserResponse:
    """
    Get current authenticated user information.

    Returns the profile information of the currently authenticated user.

    Args:
        current_user: Current authenticated user from dependency

    Returns:
        User profile information
    """
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        created_at=current_user.created_at,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token_str: str,
    user_store: UserStore = Depends(get_user_store)
) -> Token:
    """
    Refresh access token using refresh token.

    Args:
        refresh_token_str: The refresh token
        user_store: User storage instance

    Returns:
        New JWT access token

    Raises:
        HTTPException: If refresh token is invalid
    """
    # Decode refresh token
    token_data = decode_token(refresh_token_str)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user
    user = user_store.get_user_by_id(token_data.user_id)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/verify/{user_id}")
async def verify_user_email(
    user_id: str,
    user_store: UserStore = Depends(get_user_store),
    current_user: UserInDB = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Verify user email (admin or self only).

    Args:
        user_id: User ID to verify
        user_store: User storage instance
        current_user: Current authenticated user

    Returns:
        Success message

    Raises:
        HTTPException: If not authorized or user not found
    """
    # Only allow users to verify their own account or admin
    # For now, allow self-verification
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to verify this user"
        )

    success = user_store.update_user_verified(user_id, True)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {"message": "User verified successfully"}


@router.delete("/deactivate/{user_id}")
async def deactivate_user_account(
    user_id: str,
    user_store: UserStore = Depends(get_user_store),
    current_user: UserInDB = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Deactivate user account (admin or self only).

    Args:
        user_id: User ID to deactivate
        user_store: User storage instance
        current_user: Current authenticated user

    Returns:
        Success message

    Raises:
        HTTPException: If not authorized or user not found
    """
    # Only allow users to deactivate their own account
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to deactivate this user"
        )

    success = user_store.deactivate_user(user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {"message": "User deactivated successfully"}
