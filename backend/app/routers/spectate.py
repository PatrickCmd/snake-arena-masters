"""
Spectate router for viewing active players and their game states.
"""

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import ActivePlayer
from app.services import active_players

router = APIRouter(prefix="/spectate", tags=["Spectate"])


@router.get("/players", response_model=list[ActivePlayer])
async def get_active_players():
    """
    Get all currently active players.

    Returns a list of players currently in a game session.
    """
    return active_players.get_active_players()


@router.get("/players/{player_id}", response_model=ActivePlayer)
async def get_player_game_state(player_id: str):
    """
    Get the current game state for a specific player.

    Args:
        player_id: The unique identifier of the player

    Returns:
        The player's current game state
    """
    player = active_players.get_active_player(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found or not currently playing"
        )
    return player
