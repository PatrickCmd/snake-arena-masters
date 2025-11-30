"""
Test script to verify score submission works.
"""

import asyncio

import httpx


async def test_score_submission():
    """Test score submission endpoint."""
    base_url = "http://localhost:8000/api/v1"

    async with httpx.AsyncClient() as client:
        # Login
        print("1. Logging in...")
        login_response = await client.post(
            f"{base_url}/auth/login",
            data={"username": "demo@snake.game", "password": "demo123"},
        )
        print(f"   Status: {login_response.status_code}")

        if login_response.status_code != 200:
            print(f"   Error: {login_response.text}")
            return

        token = login_response.json()["access_token"]
        print(f"   Token: {token[:20]}...")

        # Submit score
        print("\n2. Submitting score...")
        score_response = await client.post(
            f"{base_url}/leaderboard/scores",
            json={"score": 9999, "mode": "walls"},
            headers={"Authorization": f"Bearer {token}"},
        )
        print(f"   Status: {score_response.status_code}")
        print(f"   Response: {score_response.json()}")

        # Get leaderboard
        print("\n3. Fetching leaderboard...")
        leaderboard_response = await client.get(f"{base_url}/leaderboard?mode=walls")
        print(f"   Status: {leaderboard_response.status_code}")
        leaderboard = leaderboard_response.json()
        print(f"   Top 3 scores:")
        for entry in leaderboard[:3]:
            print(f"     - {entry['username']}: {entry['score']}")


if __name__ == "__main__":
    print("Testing Score Submission\n" + "=" * 50)
    asyncio.run(test_score_submission())
