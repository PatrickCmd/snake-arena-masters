"""Integration tests for the best score feature."""

import pytest


@pytest.mark.asyncio
async def test_best_score_flow_end_to_end(async_client, auth_headers):
    """Test the complete best score flow from login to score submission."""
    # 1. Verify no best score exists initially
    response = await async_client.get("/api/v1/leaderboard/best-score/walls", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() is None

    # 2. Submit first score
    response = await async_client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 100, "mode": "walls"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["rank"] == 1

    # 3. Verify best score is now 100
    response = await async_client.get("/api/v1/leaderboard/best-score/walls", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == 100

    # 4. Try to submit lower score (should fail)
    response = await async_client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 50, "mode": "walls"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is False
    assert "best score is 100" in data["error"]

    # 5. Verify best score is still 100
    response = await async_client.get("/api/v1/leaderboard/best-score/walls", headers=auth_headers)
    assert response.json() == 100

    # 6. Submit higher score (should succeed)
    response = await async_client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 200, "mode": "walls"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True

    # 7. Verify best score is now 200
    response = await async_client.get("/api/v1/leaderboard/best-score/walls", headers=auth_headers)
    assert response.json() == 200

    # 8. Verify leaderboard shows the best score
    response = await async_client.get("/api/v1/leaderboard?mode=walls")
    assert response.status_code == 200
    leaderboard = response.json()
    assert len(leaderboard) == 2  # Two scores submitted (100 and 200)
    assert leaderboard[0]["score"] == 200
    assert leaderboard[0]["username"] == "DemoPlayer"


@pytest.mark.asyncio
async def test_multiple_users_best_scores(async_client):
    """Test that best scores are tracked separately for different users."""
    # Login as first user
    response = await async_client.post(
        "/api/v1/auth/login", data={"username": "demo@snake.game", "password": "demo123"}
    )
    token1 = response.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Login as second user
    response = await async_client.post(
        "/api/v1/auth/login", data={"username": "test@snake.game", "password": "test123"}
    )
    token2 = response.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User 1 submits score
    response = await async_client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 150, "mode": "walls"},
        headers=headers1,
    )
    assert response.json()["success"] is True

    # User 2 submits score
    response = await async_client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 250, "mode": "walls"},
        headers=headers2,
    )
    assert response.json()["success"] is True

    # Verify each user has their own best score
    response = await async_client.get("/api/v1/leaderboard/best-score/walls", headers=headers1)
    assert response.json() == 150

    response = await async_client.get("/api/v1/leaderboard/best-score/walls", headers=headers2)
    assert response.json() == 250

    # User 1 tries to submit lower score
    response = await async_client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 100, "mode": "walls"},
        headers=headers1,
    )
    assert response.json()["success"] is False

    # User 1's best score unchanged
    response = await async_client.get("/api/v1/leaderboard/best-score/walls", headers=headers1)
    assert response.json() == 150


@pytest.mark.asyncio
async def test_best_score_different_modes(async_client, auth_headers):
    """Test that best scores are tracked separately for different game modes."""
    # Submit score for walls mode
    response = await async_client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 100, "mode": "walls"},
        headers=auth_headers,
    )
    assert response.json()["success"] is True

    # Submit score for pass-through mode
    response = await async_client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 200, "mode": "pass-through"},
        headers=auth_headers,
    )
    assert response.json()["success"] is True

    # Verify different best scores for different modes
    response = await async_client.get("/api/v1/leaderboard/best-score/walls", headers=auth_headers)
    assert response.json() == 100

    response = await async_client.get(
        "/api/v1/leaderboard/best-score/pass-through", headers=auth_headers
    )
    assert response.json() == 200


@pytest.mark.asyncio
async def test_leaderboard_ranking_with_best_scores(async_client):
    """Test that leaderboard ranking works correctly with best-score-only logic."""
    # Create multiple users and submit scores
    users = [
        ("demo@snake.game", "demo123", [100, 150, 120]),  # Best: 150
        ("test@snake.game", "test123", [200, 180, 250]),  # Best: 250
    ]

    for email, password, scores in users:
        # Login
        response = await async_client.post(
            "/api/v1/auth/login", data={"username": email, "password": password}
        )
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Submit scores
        for score in scores:
            await async_client.post(
                "/api/v1/leaderboard/scores",
                json={"score": score, "mode": "walls"},
                headers=headers,
            )

    # Get leaderboard
    response = await async_client.get("/api/v1/leaderboard?mode=walls")
    leaderboard = response.json()

    # Should have 4 entries (only best scores saved: 150, 250 for user 1; 200, 250 for user 2)
    # Actually: 100, 150 from demo; 200, 250 from test (lower scores not saved)
    assert len(leaderboard) == 4
    assert leaderboard[0]["score"] == 250
    assert leaderboard[0]["username"] == "TestUser"
    assert leaderboard[1]["score"] == 200
    assert leaderboard[2]["score"] == 150
    assert leaderboard[2]["username"] == "DemoPlayer"


@pytest.mark.asyncio
async def test_authentication_required_for_best_score(async_client):
    """Test that authentication is required to get best score."""
    response = await async_client.get("/api/v1/leaderboard/best-score/walls")
    assert response.status_code == 401
