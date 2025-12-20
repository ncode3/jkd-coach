"""
Example client for SAMMO Fight IQ API with authentication.

Demonstrates how to:
1. Register a new user
2. Login and get access token
3. Use token to access protected endpoints
4. Log rounds, view stats, and manage data

Run: python examples/auth_client.py
"""
import sys
import requests
from typing import Optional, Dict, Any
from datetime import datetime


class SammoClient:
    """Client for SAMMO Fight IQ API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the client.

        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
        self.access_token: Optional[str] = None

    def register(
        self,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Register a new user.

        Args:
            username: Unique username
            email: User email
            password: Password (min 8 chars)
            full_name: Optional full name

        Returns:
            User information

        Raises:
            requests.HTTPError: If registration fails
        """
        data = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name
        }

        response = requests.post(f"{self.base_url}/auth/register", json=data)
        response.raise_for_status()

        return response.json()

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login and get access token.

        Args:
            username: Username
            password: Password

        Returns:
            Token information

        Raises:
            requests.HTTPError: If login fails
        """
        data = {
            "username": username,
            "password": password
        }

        response = requests.post(f"{self.base_url}/auth/login", json=data)
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data["access_token"]

        return token_data

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        if not self.access_token:
            raise ValueError("Not authenticated. Call login() first.")

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_profile(self) -> Dict[str, Any]:
        """
        Get current user profile.

        Returns:
            User profile information

        Raises:
            requests.HTTPError: If request fails
        """
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers=self._get_headers()
        )
        response.raise_for_status()

        return response.json()

    def log_round(
        self,
        pressure_score: float,
        ring_control_score: float,
        defense_score: float,
        clean_shots_taken: int,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Log a boxing round.

        Args:
            pressure_score: Pressure score (0-10)
            ring_control_score: Ring control score (0-10)
            defense_score: Defense score (0-10)
            clean_shots_taken: Number of clean shots taken
            notes: Optional notes about the round

        Returns:
            Round information with danger score and strategy

        Raises:
            requests.HTTPError: If request fails
        """
        data = {
            "pressure_score": pressure_score,
            "ring_control_score": ring_control_score,
            "defense_score": defense_score,
            "clean_shots_taken": clean_shots_taken,
            "notes": notes
        }

        response = requests.post(
            f"{self.base_url}/api/log_round",
            json=data,
            headers=self._get_headers()
        )
        response.raise_for_status()

        return response.json()

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get dashboard statistics.

        Returns:
            Dashboard stats including averages and game plan

        Raises:
            requests.HTTPError: If request fails
        """
        response = requests.get(
            f"{self.base_url}/api/dashboard_stats",
            headers=self._get_headers()
        )
        response.raise_for_status()

        return response.json()

    def get_rounds_history(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get round history.

        Args:
            limit: Maximum number of rounds to return

        Returns:
            List of rounds with metadata

        Raises:
            requests.HTTPError: If request fails
        """
        response = requests.get(
            f"{self.base_url}/api/rounds_history?limit={limit}",
            headers=self._get_headers()
        )
        response.raise_for_status()

        return response.json()

    def delete_round(self, round_id: str) -> Dict[str, Any]:
        """
        Delete a specific round.

        Args:
            round_id: ID of the round to delete

        Returns:
            Success message

        Raises:
            requests.HTTPError: If request fails
        """
        response = requests.delete(
            f"{self.base_url}/api/rounds/{round_id}",
            headers=self._get_headers()
        )
        response.raise_for_status()

        return response.json()


def main():
    """Example usage of the SAMMO client."""
    print("🥊 SAMMO Fight IQ - API Client Example\n")

    # Initialize client
    client = SammoClient()

    try:
        # Generate unique username for demo
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        username = f"fighter_{timestamp}"
        email = f"{username}@example.com"
        password = "SecurePass123!"

        print("1️⃣  Registering new user...")
        user = client.register(
            username=username,
            email=email,
            password=password,
            full_name="Demo Fighter"
        )
        print(f"   ✅ Registered: {user['username']} ({user['email']})")
        print(f"   User ID: {user['id']}\n")

        print("2️⃣  Logging in...")
        token_data = client.login(username, password)
        print(f"   ✅ Logged in successfully")
        print(f"   Token expires in: {token_data['expires_in']} seconds\n")

        print("3️⃣  Getting profile...")
        profile = client.get_profile()
        print(f"   ✅ Profile: {profile['username']}")
        print(f"   Created: {profile['created_at']}")
        print(f"   Active: {profile['is_active']}\n")

        print("4️⃣  Logging first round...")
        round1 = client.log_round(
            pressure_score=8.0,
            ring_control_score=7.5,
            defense_score=6.0,
            clean_shots_taken=2,
            notes="Great sparring session, felt strong"
        )
        print(f"   ✅ Round logged (ID: {round1['id']})")
        print(f"   Danger Score: {round1['danger_score']:.2f}")
        print(f"   Strategy: {round1['strategy']['title']}")
        print(f"   Advice: {round1['strategy']['text'][:60]}...\n")

        print("5️⃣  Logging second round...")
        round2 = client.log_round(
            pressure_score=6.0,
            ring_control_score=5.5,
            defense_score=4.0,
            clean_shots_taken=5,
            notes="Tough round, dropped guard too much"
        )
        print(f"   ✅ Round logged (ID: {round2['id']})")
        print(f"   Danger Score: {round2['danger_score']:.2f}")
        print(f"   Strategy: {round2['strategy']['title']}\n")

        print("6️⃣  Getting dashboard stats...")
        stats = client.get_dashboard_stats()
        print(f"   ✅ Total Rounds: {stats['total_rounds']}")
        print(f"   Average Pressure: {stats['averages']['pressure_score']:.1f}")
        print(f"   Average Defense: {stats['averages']['defense_score']:.1f}")
        print(f"   Average Shots Taken: {stats['averages']['clean_shots_taken']:.1f}")
        print(f"   Next Game Plan: {stats['next_game_plan']['title']}\n")

        print("7️⃣  Getting round history...")
        history = client.get_rounds_history(limit=10)
        print(f"   ✅ Total Rounds: {history['total']}")
        for i, round_data in enumerate(history['rounds'], 1):
            print(f"   Round {i}: Score {round_data.get('defense_score', 0):.1f}, "
                  f"Danger {round_data.get('danger_score', 0):.2f}")
        print()

        print("8️⃣  Deleting a round...")
        delete_result = client.delete_round(round1['id'])
        print(f"   ✅ {delete_result['message']}\n")

        print("9️⃣  Checking updated stats...")
        updated_stats = client.get_dashboard_stats()
        print(f"   ✅ Total Rounds Now: {updated_stats['total_rounds']}")
        print()

        print("✅ Demo completed successfully!")
        print("\n" + "="*60)
        print("Next steps:")
        print("- Explore the API docs at http://localhost:8000/docs")
        print("- Try the interactive Swagger UI")
        print("- Check AUTH_SETUP.md for more details")
        print("="*60)

    except requests.HTTPError as e:
        print(f"\n❌ HTTP Error: {e}")
        if e.response is not None:
            print(f"   Status Code: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
