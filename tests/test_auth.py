"""
Tests for authentication system.

Run with: pytest tests/test_auth.py -v
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.auth.jwt_handler import (
    create_access_token,
    decode_token,
    verify_token,
    get_password_hash,
    verify_password,
    extract_token_from_header
)
from src.auth.models import TokenData


class TestPasswordHashing:
    """Test password hashing functionality."""

    def test_password_hashing(self):
        """Test that password hashing works correctly."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)

        # Hashed password should not equal plain password
        assert hashed != password

        # Should be able to verify correct password
        assert verify_password(password, hashed) is True

        # Should reject incorrect password
        assert verify_password("WrongPassword", hashed) is False

    def test_different_hashes_for_same_password(self):
        """Test that same password produces different hashes (salt)."""
        password = "SamePassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Hashes should be different due to salt
        assert hash1 != hash2

        # Both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    """Test JWT token generation and validation."""

    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "user123", "username": "testuser"}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self):
        """Test decoding a valid token."""
        user_id = "user123"
        username = "testuser"
        data = {"sub": user_id, "username": username}

        token = create_access_token(data)
        decoded = decode_token(token)

        assert decoded is not None
        assert decoded.user_id == user_id
        assert decoded.username == username
        assert isinstance(decoded.exp, datetime)

    def test_decode_invalid_token(self):
        """Test decoding an invalid token."""
        invalid_token = "invalid.token.string"
        decoded = decode_token(invalid_token)

        assert decoded is None

    def test_verify_valid_token(self):
        """Test verifying a valid token."""
        data = {"sub": "user123", "username": "testuser"}
        token = create_access_token(data)

        assert verify_token(token) is True

    def test_verify_invalid_token(self):
        """Test verifying an invalid token."""
        invalid_token = "invalid.token.string"

        assert verify_token(invalid_token) is False

    def test_expired_token(self):
        """Test that expired tokens are rejected."""
        data = {"sub": "user123", "username": "testuser"}

        # Create token that expires immediately
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))

        # Token should be invalid due to expiration
        assert verify_token(token) is False

    def test_token_expiration_time(self):
        """Test that token expiration is set correctly."""
        data = {"sub": "user123", "username": "testuser"}
        expires_in = timedelta(minutes=15)

        token = create_access_token(data, expires_delta=expires_in)
        decoded = decode_token(token)

        assert decoded is not None

        # Check expiration is roughly correct (within 1 minute tolerance)
        expected_exp = datetime.utcnow() + expires_in
        time_diff = abs((decoded.exp - expected_exp).total_seconds())
        assert time_diff < 60  # Within 1 minute


class TestHeaderExtraction:
    """Test token extraction from authorization headers."""

    def test_extract_valid_bearer_token(self):
        """Test extracting token from valid Bearer header."""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token"
        header = f"Bearer {token}"

        extracted = extract_token_from_header(header)
        assert extracted == token

    def test_extract_case_insensitive(self):
        """Test that Bearer keyword is case insensitive."""
        token = "test.token.string"
        header = f"bearer {token}"

        extracted = extract_token_from_header(header)
        assert extracted == token

    def test_extract_invalid_format(self):
        """Test extracting from invalid header format."""
        # Missing Bearer prefix
        assert extract_token_from_header("token.string") is None

        # Wrong prefix
        assert extract_token_from_header("Basic token.string") is None

        # Empty header
        assert extract_token_from_header("") is None

        # None header
        assert extract_token_from_header(None) is None

    def test_extract_multiple_spaces(self):
        """Test that extra spaces break extraction."""
        token = "test.token.string"
        header = f"Bearer  {token}  extra"

        # Should fail with extra parts
        extracted = extract_token_from_header(header)
        assert extracted is None


class TestTokenData:
    """Test TokenData model."""

    def test_token_data_creation(self):
        """Test creating TokenData instance."""
        user_id = "user123"
        username = "testuser"
        exp = datetime.utcnow() + timedelta(minutes=30)

        token_data = TokenData(
            user_id=user_id,
            username=username,
            exp=exp
        )

        assert token_data.user_id == user_id
        assert token_data.username == username
        assert token_data.exp == exp


class TestAuthModels:
    """Test authentication Pydantic models."""

    def test_user_create_validation(self):
        """Test UserCreate model validation."""
        from src.auth.models import UserCreate

        # Valid user
        user = UserCreate(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"

        # Test minimum username length
        with pytest.raises(Exception):
            UserCreate(
                username="ab",  # Too short (min 3)
                email="test@example.com",
                password="SecurePass123!"
            )

        # Test minimum password length
        with pytest.raises(Exception):
            UserCreate(
                username="testuser",
                email="test@example.com",
                password="short"  # Too short (min 8)
            )

    def test_user_login_validation(self):
        """Test UserLogin model validation."""
        from src.auth.models import UserLogin

        login = UserLogin(
            username="testuser",
            password="SecurePass123!"
        )

        assert login.username == "testuser"
        assert login.password == "SecurePass123!"

    def test_token_response(self):
        """Test Token model."""
        from src.auth.models import Token

        token = Token(
            access_token="test.token.string",
            token_type="bearer",
            expires_in=1800
        )

        assert token.access_token == "test.token.string"
        assert token.token_type == "bearer"
        assert token.expires_in == 1800


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
