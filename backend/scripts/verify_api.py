"""
API Verification Script

This script tests all endpoints of the running Snake Arena Masters API
to ensure they work correctly. Run this against a live server.

Usage:
    python scripts/verify_api.py [--url http://localhost:8000]
"""

import argparse
import sys
from typing import Any

import httpx


class Colors:
    """ANSI color codes for terminal output."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


class APIVerifier:
    """Verify API endpoints are working correctly."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api/v1"
        self.client = httpx.Client(timeout=10.0)
        self.token: str | None = None
        self.passed = 0
        self.failed = 0

    def print_header(self, text: str):
        """Print a section header."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")

    def print_test(self, name: str, passed: bool, details: str = ""):
        """Print test result."""
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"{status} - {name}")
        if details:
            print(f"  {Colors.YELLOW}{details}{Colors.RESET}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def verify_health(self) -> bool:
        """Verify health endpoint."""
        try:
            response = self.client.get(f"{self.base_url}/health")
            passed = response.status_code == 200
            self.print_test("Health Check", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Health Check", False, f"Error: {e}")
            return False

    def verify_root(self) -> bool:
        """Verify root endpoint."""
        try:
            response = self.client.get(f"{self.base_url}/")
            passed = response.status_code == 200 and "message" in response.json()
            self.print_test("Root Endpoint", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Root Endpoint", False, f"Error: {e}")
            return False

    def verify_login(self) -> bool:
        """Verify login endpoint and get token."""
        try:
            response = self.client.post(
                f"{self.api_url}/auth/login",
                data={"username": "demo@snake.game", "password": "demo123"},
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                self.token = data.get("access_token")
                passed = self.token is not None
            self.print_test("Login", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Login", False, f"Error: {e}")
            return False

    def verify_signup(self) -> bool:
        """Verify signup endpoint."""
        try:
            response = self.client.post(
                f"{self.api_url}/auth/signup",
                json={
                    "email": f"test{self.passed}@test.com",
                    "username": f"TestUser{self.passed}",
                    "password": "testpass123",
                },
            )
            passed = response.status_code == 201
            if passed:
                data = response.json()
                passed = data.get("success") is True
            self.print_test("Signup", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Signup", False, f"Error: {e}")
            return False

    def verify_get_current_user(self) -> bool:
        """Verify get current user endpoint."""
        if not self.token:
            self.print_test("Get Current User", False, "No auth token available")
            return False

        try:
            response = self.client.get(
                f"{self.api_url}/auth/me", headers={"Authorization": f"Bearer {self.token}"}
            )
            passed = response.status_code == 200
            if passed:
                data = response.json()
                passed = "username" in data and "email" in data
            self.print_test("Get Current User", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Get Current User", False, f"Error: {e}")
            return False

    def verify_logout(self) -> bool:
        """Verify logout endpoint."""
        if not self.token:
            self.print_test("Logout", False, "No auth token available")
            return False

        try:
            response = self.client.post(
                f"{self.api_url}/auth/logout", headers={"Authorization": f"Bearer {self.token}"}
            )
            passed = response.status_code == 204
            self.print_test("Logout", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Logout", False, f"Error: {e}")
            return False

    def verify_get_leaderboard(self) -> bool:
        """Verify get leaderboard endpoint."""
        try:
            response = self.client.get(f"{self.api_url}/leaderboard")
            passed = response.status_code == 200
            if passed:
                data = response.json()
                passed = isinstance(data, list) and len(data) > 0
            self.print_test("Get Leaderboard", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Get Leaderboard", False, f"Error: {e}")
            return False

    def verify_get_leaderboard_filtered(self) -> bool:
        """Verify get leaderboard with filter."""
        try:
            response = self.client.get(f"{self.api_url}/leaderboard?mode=walls")
            passed = response.status_code == 200
            if passed:
                data = response.json()
                passed = isinstance(data, list)
                if passed and len(data) > 0:
                    passed = all(entry["mode"] == "walls" for entry in data)
            self.print_test("Get Leaderboard (Filtered)", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Get Leaderboard (Filtered)", False, f"Error: {e}")
            return False

    def verify_submit_score(self) -> bool:
        """Verify submit score endpoint."""
        if not self.token:
            self.print_test("Submit Score", False, "No auth token available")
            return False

        try:
            response = self.client.post(
                f"{self.api_url}/leaderboard/scores",
                json={"score": 1000, "mode": "walls"},
                headers={"Authorization": f"Bearer {self.token}"},
            )
            passed = response.status_code == 201
            if passed:
                data = response.json()
                passed = data.get("success") is True and "rank" in data
            self.print_test("Submit Score", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Submit Score", False, f"Error: {e}")
            return False

    def verify_get_active_players(self) -> bool:
        """Verify get active players endpoint."""
        try:
            response = self.client.get(f"{self.api_url}/spectate/players")
            passed = response.status_code == 200
            if passed:
                data = response.json()
                passed = isinstance(data, list) and len(data) > 0
            self.print_test("Get Active Players", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Get Active Players", False, f"Error: {e}")
            return False

    def verify_get_player_game_state(self) -> bool:
        """Verify get player game state endpoint."""
        try:
            # First get active players
            response = self.client.get(f"{self.api_url}/spectate/players")
            if response.status_code != 200:
                self.print_test("Get Player Game State", False, "Could not get active players")
                return False

            players = response.json()
            if not players:
                self.print_test("Get Player Game State", False, "No active players")
                return False

            player_id = players[0]["id"]
            response = self.client.get(f"{self.api_url}/spectate/players/{player_id}")
            passed = response.status_code == 200
            if passed:
                data = response.json()
                passed = "gameState" in data and "snake" in data["gameState"]
            self.print_test("Get Player Game State", passed, f"Status: {response.status_code}")
            return passed
        except Exception as e:
            self.print_test("Get Player Game State", False, f"Error: {e}")
            return False

    def run_all_tests(self) -> bool:
        """Run all verification tests."""
        print(f"\n{Colors.BOLD}Snake Arena Masters - API Verification{Colors.RESET}")
        print(f"Testing API at: {Colors.YELLOW}{self.base_url}{Colors.RESET}")

        # Test server connectivity
        self.print_header("Server Connectivity")
        if not self.verify_health():
            print(f"\n{Colors.RED}Server is not responding. Is it running?{Colors.RESET}")
            return False
        self.verify_root()

        # Test authentication endpoints
        self.print_header("Authentication Endpoints")
        self.verify_login()
        self.verify_signup()
        self.verify_get_current_user()
        self.verify_logout()

        # Re-login for protected endpoints
        self.verify_login()

        # Test leaderboard endpoints
        self.print_header("Leaderboard Endpoints")
        self.verify_get_leaderboard()
        self.verify_get_leaderboard_filtered()
        self.verify_submit_score()

        # Test spectate endpoints
        self.print_header("Spectate Endpoints")
        self.verify_get_active_players()
        self.verify_get_player_game_state()

        # Print summary
        self.print_summary()

        return self.failed == 0

    def print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}Test Summary{Colors.RESET}")
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.RESET}")

        if self.failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.RESET}\n")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed{Colors.RESET}\n")

    def __del__(self):
        """Clean up HTTP client."""
        self.client.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Verify Snake Arena Masters API")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the API server (default: http://localhost:8000)",
    )
    args = parser.parse_args()

    verifier = APIVerifier(args.url)
    success = verifier.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
