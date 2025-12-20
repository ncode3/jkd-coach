"""
User storage and management using Firestore.

Provides user CRUD operations with secure password handling.
"""
import uuid
from datetime import datetime
from typing import Optional, List
from google.cloud import firestore

from .models import UserCreate, UserInDB
from .jwt_handler import get_password_hash


class UserStore:
    """User storage layer using Firestore."""

    def __init__(self):
        """Initialize Firestore client and users collection."""
        self._db = firestore.Client()
        self._users_collection = self._db.collection('users')

    def create_user(self, user_data: UserCreate) -> UserInDB:
        """
        Create a new user with hashed password.

        Args:
            user_data: User creation data with plain password

        Returns:
            Created user object from database

        Raises:
            ValueError: If username or email already exists
        """
        # Check if username exists
        existing = self._users_collection.where(
            'username', '==', user_data.username
        ).limit(1).get()

        if len(list(existing)) > 0:
            raise ValueError(f"Username '{user_data.username}' already exists")

        # Check if email exists
        existing = self._users_collection.where(
            'email', '==', user_data.email
        ).limit(1).get()

        if len(list(existing)) > 0:
            raise ValueError(f"Email '{user_data.email}' already exists")

        # Create user document
        user_id = str(uuid.uuid4())
        user_doc = {
            'id': user_id,
            'username': user_data.username,
            'email': user_data.email,
            'full_name': user_data.full_name,
            'hashed_password': get_password_hash(user_data.password),
            'created_at': firestore.SERVER_TIMESTAMP,
            'is_active': True,
            'is_verified': False
        }

        self._users_collection.document(user_id).set(user_doc)

        # Retrieve the created document to get server timestamp
        created_doc = self._users_collection.document(user_id).get()
        doc_data = created_doc.to_dict()

        return UserInDB(
            id=doc_data['id'],
            username=doc_data['username'],
            email=doc_data['email'],
            full_name=doc_data.get('full_name'),
            hashed_password=doc_data['hashed_password'],
            created_at=doc_data['created_at'],
            is_active=doc_data.get('is_active', True),
            is_verified=doc_data.get('is_verified', False)
        )

    def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        """
        Get user by username.

        Args:
            username: Username to search for

        Returns:
            User object if found, None otherwise
        """
        docs = self._users_collection.where(
            'username', '==', username
        ).limit(1).get()

        docs_list = list(docs)
        if not docs_list:
            return None

        doc_data = docs_list[0].to_dict()
        return UserInDB(
            id=doc_data['id'],
            username=doc_data['username'],
            email=doc_data['email'],
            full_name=doc_data.get('full_name'),
            hashed_password=doc_data['hashed_password'],
            created_at=doc_data['created_at'],
            is_active=doc_data.get('is_active', True),
            is_verified=doc_data.get('is_verified', False)
        )

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Get user by email.

        Args:
            email: Email to search for

        Returns:
            User object if found, None otherwise
        """
        docs = self._users_collection.where(
            'email', '==', email
        ).limit(1).get()

        docs_list = list(docs)
        if not docs_list:
            return None

        doc_data = docs_list[0].to_dict()
        return UserInDB(
            id=doc_data['id'],
            username=doc_data['username'],
            email=doc_data['email'],
            full_name=doc_data.get('full_name'),
            hashed_password=doc_data['hashed_password'],
            created_at=doc_data['created_at'],
            is_active=doc_data.get('is_active', True),
            is_verified=doc_data.get('is_verified', False)
        )

    def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """
        Get user by ID.

        Args:
            user_id: User ID to search for

        Returns:
            User object if found, None otherwise
        """
        doc = self._users_collection.document(user_id).get()

        if not doc.exists:
            return None

        doc_data = doc.to_dict()
        return UserInDB(
            id=doc_data['id'],
            username=doc_data['username'],
            email=doc_data['email'],
            full_name=doc_data.get('full_name'),
            hashed_password=doc_data['hashed_password'],
            created_at=doc_data['created_at'],
            is_active=doc_data.get('is_active', True),
            is_verified=doc_data.get('is_verified', False)
        )

    def update_user_verified(self, user_id: str, is_verified: bool) -> bool:
        """
        Update user verification status.

        Args:
            user_id: User ID
            is_verified: New verification status

        Returns:
            True if update successful, False otherwise
        """
        try:
            self._users_collection.document(user_id).update({
                'is_verified': is_verified
            })
            return True
        except Exception:
            return False

    def deactivate_user(self, user_id: str) -> bool:
        """
        Deactivate a user account.

        Args:
            user_id: User ID

        Returns:
            True if deactivation successful, False otherwise
        """
        try:
            self._users_collection.document(user_id).update({
                'is_active': False
            })
            return True
        except Exception:
            return False

    def list_users(self, limit: int = 100) -> List[UserInDB]:
        """
        List all users (admin function).

        Args:
            limit: Maximum number of users to return

        Returns:
            List of user objects
        """
        docs = self._users_collection.limit(limit).stream()
        users = []

        for doc in docs:
            doc_data = doc.to_dict()
            users.append(UserInDB(
                id=doc_data['id'],
                username=doc_data['username'],
                email=doc_data['email'],
                full_name=doc_data.get('full_name'),
                hashed_password=doc_data['hashed_password'],
                created_at=doc_data['created_at'],
                is_active=doc_data.get('is_active', True),
                is_verified=doc_data.get('is_verified', False)
            ))

        return users
