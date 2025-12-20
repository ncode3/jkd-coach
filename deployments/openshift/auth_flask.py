"""
Flask authentication module using JWT tokens.

Adapts the FastAPI authentication logic for Flask applications.
Uses the same JWT tokens and Firestore user store.
"""
import os
from functools import wraps
from typing import Optional
from flask import request, jsonify
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from google.cloud import firestore

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


# ============================================================================
# Password Functions
# ============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


# ============================================================================
# JWT Token Functions
# ============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of claims to encode
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


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.

    Args:
        token: The JWT token string

    Returns:
        Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None
    except Exception:
        return None


# ============================================================================
# User Store (Firestore)
# ============================================================================

class UserStore:
    """User storage using Firestore."""

    def __init__(self):
        """Initialize Firestore client."""
        self._db = firestore.Client()
        self._users_collection = self._db.collection('users')

    def create_user(self, username: str, email: str, password: str, full_name: str = None) -> dict:
        """
        Create a new user.

        Args:
            username: Unique username
            email: User email
            password: Plain text password (will be hashed)
            full_name: Optional full name

        Returns:
            Created user dict

        Raises:
            ValueError: If username or email already exists
        """
        # Check if username exists
        existing = list(self._users_collection.where('username', '==', username).limit(1).get())
        if existing:
            raise ValueError(f"Username '{username}' already exists")

        # Check if email exists
        existing = list(self._users_collection.where('email', '==', email).limit(1).get())
        if existing:
            raise ValueError(f"Email '{email}' already exists")

        # Create user document
        import uuid
        user_id = str(uuid.uuid4())
        user_doc = {
            'id': user_id,
            'username': username,
            'email': email,
            'full_name': full_name,
            'hashed_password': get_password_hash(password),
            'created_at': firestore.SERVER_TIMESTAMP,
            'is_active': True,
            'is_verified': False
        }

        self._users_collection.document(user_id).set(user_doc)

        # Return created user (without password)
        user_doc.pop('hashed_password')
        return user_doc

    def get_user_by_username(self, username: str) -> Optional[dict]:
        """Get user by username."""
        docs = list(self._users_collection.where('username', '==', username).limit(1).get())
        if not docs:
            return None
        return docs[0].to_dict()

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID."""
        doc = self._users_collection.document(user_id).get()
        if not doc.exists:
            return None
        return doc.to_dict()


# Initialize global user store
try:
    user_store = UserStore()
except Exception as e:
    print(f"⚠️  Warning: Could not initialize UserStore: {e}")
    user_store = None


# ============================================================================
# Flask Authentication Decorators
# ============================================================================

def get_current_user() -> Optional[dict]:
    """
    Get current user from request Authorization header.

    Returns:
        User dict if authenticated, None otherwise
    """
    if user_store is None:
        return None

    # Get Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    # Extract token
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None

    token = parts[1]

    # Decode token
    payload = decode_token(token)
    if not payload:
        return None

    user_id = payload.get('sub')
    if not user_id:
        return None

    # Get user from database
    user = user_store.get_user_by_id(user_id)
    if not user or not user.get('is_active', False):
        return None

    return user


def require_auth(f):
    """
    Decorator to require authentication for Flask routes.

    Usage:
        @app.route('/protected')
        @require_auth
        def protected_route():
            user = get_current_user()
            return {'user': user['username']}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return jsonify({
                'status': 'error',
                'message': 'Authentication required'
            }), 401

        return f(*args, **kwargs)

    return decorated_function


def optional_auth(f):
    """
    Decorator for optional authentication.
    Route can be accessed with or without authentication.

    Usage:
        @app.route('/optional')
        @optional_auth
        def optional_route():
            user = get_current_user()
            if user:
                return {'message': f'Hello {user["username"]}'}
            return {'message': 'Hello anonymous'}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Authentication is optional, just continue
        return f(*args, **kwargs)

    return decorated_function
