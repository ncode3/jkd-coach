"""
Authentication data models for SAMMO Fight IQ.

Defines user models, token schemas, and authentication-related data structures.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model with common fields."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation model with password."""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """User login credentials."""
    username: str
    password: str


class UserInDB(UserBase):
    """User model as stored in database."""
    id: str
    hashed_password: str
    created_at: datetime
    is_active: bool = True
    is_verified: bool = False


class UserResponse(UserBase):
    """User response model (no sensitive data)."""
    id: str
    created_at: datetime
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    """Data stored in JWT token."""
    user_id: str
    username: str
    exp: datetime


class RefreshToken(BaseModel):
    """Refresh token request."""
    refresh_token: str
