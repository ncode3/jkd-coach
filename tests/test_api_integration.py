"""
Integration tests for the authenticated API.

These tests require the API server to be running.

Run with: pytest tests/test_api_integration.py -v
or: python tests/test_api_integration.py
"""
import pytest
import requests
from datetime import datetime
from typing import Optional


BASE_URL = "http://localhost:8000"


class TestAuthenticationFlow:
    """Test the complete authentication flow."""

    def setup_method(self):
        """Set up test data."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.username = f"test_user_{timestamp}"
        self.email = f"{self.username}@example.com"
        self.password = "TestPass123!"
        self.full_name = "Test User"
        self.access_token: Optional[str] = None

    def test_01_health_check(self):
        """Test health check endpoint (no auth required)."""
        response = requests.get(f"{BASE_URL}/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_02_register_user(self):
        """Test user registration."""
        payload = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "full_name": self.full_name
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == self.username
        assert data["email"] == self.email
        assert data["full_name"] == self.full_name
        assert "id" in data
        assert "created_at" in data
        assert data["is_active"] is True

    def test_03_register_duplicate_username(self):
        """Test that duplicate username fails."""
        payload = {
            "username": self.username,
            "email": "different@example.com",
            "password": self.password
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=payload)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_04_login(self):
        """Test user login."""
        payload = {
            "username": self.username,
            "password": self.password
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0

        # Store token for subsequent tests
        self.access_token = data["access_token"]

    def test_05_login_wrong_password(self):
        """Test login with wrong password."""
        payload = {
            "username": self.username,
            "password": "WrongPassword123!"
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_06_get_profile(self):
        """Test getting user profile with valid token."""
        if not self.access_token:
            pytest.skip("No access token available")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == self.username
        assert data["email"] == self.email

    def test_07_get_profile_no_token(self):
        """Test that profile endpoint requires authentication."""
        response = requests.get(f"{BASE_URL}/auth/me")

        assert response.status_code == 403  # No credentials provided

    def test_08_get_profile_invalid_token(self):
        """Test that invalid token is rejected."""
        headers = {"Authorization": "Bearer invalid.token.string"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)

        assert response.status_code == 401


class TestBoxingRoundsAPI:
    """Test boxing rounds API endpoints."""

    def setup_method(self):
        """Set up test data and authenticate."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.username = f"test_boxer_{timestamp}"
        self.email = f"{self.username}@example.com"
        self.password = "BoxerPass123!"

        # Register and login
        register_payload = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "full_name": "Test Boxer"
        }
        requests.post(f"{BASE_URL}/auth/register", json=register_payload)

        login_payload = {
            "username": self.username,
            "password": self.password
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        self.access_token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.round_ids = []

    def test_01_log_round(self):
        """Test logging a boxing round."""
        payload = {
            "pressure_score": 8.0,
            "ring_control_score": 7.5,
            "defense_score": 6.0,
            "clean_shots_taken": 2,
            "notes": "Great sparring session"
        }

        response = requests.post(
            f"{BASE_URL}/api/log_round",
            json=payload,
            headers=self.headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "id" in data
        assert "danger_score" in data
        assert 0.0 <= data["danger_score"] <= 1.0
        assert "strategy" in data
        assert "title" in data["strategy"]
        assert "text" in data["strategy"]

        self.round_ids.append(data["id"])

    def test_02_log_round_no_auth(self):
        """Test that logging round requires authentication."""
        payload = {
            "pressure_score": 8.0,
            "ring_control_score": 7.5,
            "defense_score": 6.0,
            "clean_shots_taken": 2
        }

        response = requests.post(f"{BASE_URL}/api/log_round", json=payload)

        assert response.status_code == 403

    def test_03_log_multiple_rounds(self):
        """Test logging multiple rounds."""
        rounds = [
            {
                "pressure_score": 7.0,
                "ring_control_score": 6.5,
                "defense_score": 5.0,
                "clean_shots_taken": 3,
                "notes": "Round 1"
            },
            {
                "pressure_score": 6.0,
                "ring_control_score": 5.5,
                "defense_score": 4.0,
                "clean_shots_taken": 5,
                "notes": "Round 2"
            }
        ]

        for round_data in rounds:
            response = requests.post(
                f"{BASE_URL}/api/log_round",
                json=round_data,
                headers=self.headers
            )
            assert response.status_code == 200
            self.round_ids.append(response.json()["id"])

    def test_04_get_dashboard_stats(self):
        """Test getting dashboard statistics."""
        response = requests.get(
            f"{BASE_URL}/api/dashboard_stats",
            headers=self.headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "averages" in data
        assert "total_rounds" in data
        assert "next_game_plan" in data
        assert data["total_rounds"] >= 1  # We logged at least one round

    def test_05_get_rounds_history(self):
        """Test getting rounds history."""
        response = requests.get(
            f"{BASE_URL}/api/rounds_history",
            headers=self.headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "rounds" in data
        assert "total" in data
        assert data["total"] >= 1
        assert len(data["rounds"]) >= 1

        # Verify rounds are sorted by date (most recent first)
        if len(data["rounds"]) > 1:
            dates = [r.get("date") for r in data["rounds"] if r.get("date")]
            assert dates == sorted(dates, reverse=True)

    def test_06_get_rounds_with_limit(self):
        """Test getting rounds history with limit."""
        response = requests.get(
            f"{BASE_URL}/api/rounds_history?limit=1",
            headers=self.headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["rounds"]) <= 1

    def test_07_delete_round(self):
        """Test deleting a round."""
        if not self.round_ids:
            pytest.skip("No rounds to delete")

        round_id = self.round_ids[0]
        response = requests.delete(
            f"{BASE_URL}/api/rounds/{round_id}",
            headers=self.headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_08_delete_nonexistent_round(self):
        """Test deleting a nonexistent round."""
        fake_id = "nonexistent-round-id"
        response = requests.delete(
            f"{BASE_URL}/api/rounds/{fake_id}",
            headers=self.headers
        )

        assert response.status_code == 404

    def test_09_user_isolation(self):
        """Test that users can only see their own rounds."""
        # Create another user
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        other_username = f"other_user_{timestamp}"
        other_email = f"{other_username}@example.com"

        register_payload = {
            "username": other_username,
            "email": other_email,
            "password": "OtherPass123!"
        }
        requests.post(f"{BASE_URL}/auth/register", json=register_payload)

        login_payload = {
            "username": other_username,
            "password": "OtherPass123!"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        other_token = response.json()["access_token"]
        other_headers = {"Authorization": f"Bearer {other_token}"}

        # Try to access first user's rounds
        response = requests.get(
            f"{BASE_URL}/api/dashboard_stats",
            headers=other_headers
        )

        assert response.status_code == 200
        data = response.json()
        # Other user should have 0 rounds
        assert data["total_rounds"] == 0


def run_tests():
    """Run all integration tests."""
    print("🥊 Running SAMMO Fight IQ API Integration Tests\n")
    print("⚠️  Make sure the API server is running at http://localhost:8000\n")

    # Run pytest programmatically
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
