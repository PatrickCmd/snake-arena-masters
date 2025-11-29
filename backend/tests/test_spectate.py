"""
Tests for spectate endpoints.
"""

from fastapi import status


def test_get_active_players(client):
    """Test getting list of active players."""
    response = client.get("/api/v1/spectate/players")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Verify player structure
    player = data[0]
    assert "id" in player
    assert "username" in player
    assert "score" in player
    assert "mode" in player
    assert "gameState" in player


def test_get_player_game_state_valid_id(client):
    """Test getting game state for valid player ID."""
    # First get active players
    response = client.get("/api/v1/spectate/players")
    players = response.json()
    player_id = players[0]["id"]

    # Get specific player
    response = client.get(f"/api/v1/spectate/players/{player_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == player_id
    assert "gameState" in data

    # Verify game state structure
    game_state = data["gameState"]
    assert "snake" in game_state
    assert "food" in game_state
    assert "direction" in game_state
    assert "score" in game_state


def test_get_player_game_state_invalid_id(client):
    """Test getting game state for invalid player ID."""
    response = client.get("/api/v1/spectate/players/invalid-id")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_active_player_has_valid_game_state(client):
    """Test that active players have valid game state."""
    response = client.get("/api/v1/spectate/players")
    players = response.json()

    for player in players:
        game_state = player["gameState"]

        # Verify snake is a list of positions
        assert isinstance(game_state["snake"], list)
        assert len(game_state["snake"]) > 0

        # Verify food position
        assert "x" in game_state["food"]
        assert "y" in game_state["food"]

        # Verify direction is valid
        assert game_state["direction"] in ["UP", "DOWN", "LEFT", "RIGHT"]

        # Verify mode is valid
        assert player["mode"] in ["pass-through", "walls"]
