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


def test_get_best_score_authenticated(client, auth_headers):
    """Test getting best score when authenticated."""
    # First submit a score
    client.post(
        "/api/v1/leaderboard/scores", json={"score": 500, "mode": "walls"}, headers=auth_headers
    )
    
    # Get best score
    response = client.get("/api/v1/leaderboard/best-score/walls", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    best_score = response.json()
    assert best_score == 500


def test_get_best_score_no_scores(client, auth_headers):
    """Test getting best score when user has no scores for that mode."""
    response = client.get("/api/v1/leaderboard/best-score/pass-through", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    # Should return null/None when no scores exist
    assert response.json() is None


def test_get_best_score_unauthenticated(client):
    """Test getting best score without authentication."""
    response = client.get("/api/v1/leaderboard/best-score/walls")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_submit_lower_score_not_saved(client, auth_headers):
    """Test that lower scores are not saved."""
    # Submit initial high score
    response1 = client.post(
        "/api/v1/leaderboard/scores", json={"score": 1000, "mode": "walls"}, headers=auth_headers
    )
    assert response1.status_code == status.HTTP_201_CREATED
    assert response1.json()["success"] is True
    
    # Try to submit lower score
    response2 = client.post(
        "/api/v1/leaderboard/scores", json={"score": 500, "mode": "walls"}, headers=auth_headers
    )
    assert response2.status_code == status.HTTP_201_CREATED
    data = response2.json()
    assert data["success"] is False
    assert "best score is 1000" in data["error"]
    
    # Verify best score is still 1000
    response3 = client.get("/api/v1/leaderboard/best-score/walls", headers=auth_headers)
    assert response3.json() == 1000


def test_submit_higher_score_saved(client, auth_headers):
    """Test that higher scores are saved."""
    # Submit initial score
    response1 = client.post(
        "/api/v1/leaderboard/scores", json={"score": 500, "mode": "walls"}, headers=auth_headers
    )
    assert response1.json()["success"] is True
    
    # Submit higher score
    response2 = client.post(
        "/api/v1/leaderboard/scores", json={"score": 1000, "mode": "walls"}, headers=auth_headers
    )
    assert response2.status_code == status.HTTP_201_CREATED
    data = response2.json()
    assert data["success"] is True
    
    # Verify best score is now 1000
    response3 = client.get("/api/v1/leaderboard/best-score/walls", headers=auth_headers)
    assert response3.json() == 1000
