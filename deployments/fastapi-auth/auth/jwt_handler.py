"""
JWT token generation and validation utilities.

Handles JWT token creation, validation, and decoding using HS256 algorithm.
"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from .models import TokenData

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The plain text password
        hashed_password: The hashed password to compare against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of claims to encode in the token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token with longer expiration.

    Args:
        data: Dictionary of claims to encode in the token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """
    Decode and validate a JWT token.

    Args:
        token: The JWT token string to decode

    Returns:
        TokenData object if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        exp_timestamp: int = payload.get("exp")

        if user_id is None or username is None:
            return None

        exp = datetime.fromtimestamp(exp_timestamp)

        return TokenData(
            user_id=user_id,
            username=username,
            exp=exp
        )
    except InvalidTokenError:
        return None
    except Exception:
        return None


def verify_token(token: str) -> bool:
    """
    Verify if a token is valid and not expired.

    Args:
        token: The JWT token string to verify

    Returns:
        True if token is valid, False otherwise
    """
    token_data = decode_token(token)
    if token_data is None:
        return False

    # Check if token is expired
    if token_data.exp < datetime.utcnow():
        return False

    return True


def extract_token_from_header(authorization: str) -> Optional[str]:
    """
    Extract JWT token from Authorization header.

    Args:
        authorization: The Authorization header value (e.g., "Bearer <token>")

    Returns:
        The token string if valid format, None otherwise
    """
    if not authorization:
        return None

    parts = authorization.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    return parts[1]
