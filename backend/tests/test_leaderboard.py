"""
Tests for leaderboard endpoints.
"""

from fastapi import status


def test_get_all_leaderboard_entries(client):
    """Test getting all leaderboard entries."""
    response = client.get("/api/v1/leaderboard")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_leaderboard_filtered_by_walls(client):
    """Test getting leaderboard filtered by walls mode."""
    response = client.get("/api/v1/leaderboard?mode=walls")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    for entry in data:
        assert entry["mode"] == "walls"


def test_get_leaderboard_filtered_by_pass_through(client):
    """Test getting leaderboard filtered by pass-through mode."""
    response = client.get("/api/v1/leaderboard?mode=pass-through")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    for entry in data:
        assert entry["mode"] == "pass-through"


def test_submit_score_authenticated(client, auth_headers):
    """Test submitting score when authenticated."""
    response = client.post(
        "/api/v1/leaderboard/scores", json={"score": 1000, "mode": "walls"}, headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["success"] is True
    assert "rank" in data
    assert isinstance(data["rank"], int)


def test_submit_score_unauthenticated(client):
    """Test submitting score without authentication."""
    response = client.post("/api/v1/leaderboard/scores", json={"score": 1000, "mode": "walls"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_submit_score_invalid_mode(client, auth_headers):
    """Test submitting score with invalid mode."""
    response = client.post(
        "/api/v1/leaderboard/scores",
        json={"score": 1000, "mode": "invalid-mode"},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_submit_score_negative(client, auth_headers):
    """Test submitting negative score."""
    response = client.post(
        "/api/v1/leaderboard/scores", json={"score": -100, "mode": "walls"}, headers=auth_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
