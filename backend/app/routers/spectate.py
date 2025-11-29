"""
Spectate router for viewing active players and their game states.
"""

from fastapi import APIRouter, HTTPException, Path, status

from app.models.schemas import ActivePlayer
from app.services.database import db

router = APIRouter(prefix="/spectate", tags=["Spectate"])


@router.get("/players", response_model=list[ActivePlayer])
async def get_active_players():
    """
    Get list of currently active players.

    Returns all players currently in an active game session.
    """
    return db.get_active_players()


@router.get("/players/{playerId}", response_model=ActivePlayer)
async def get_player_game_state(
    playerId: str = Path(..., description="ID of the player to spectate"),
):
    """
    Get the current game state for a specific player.

    Returns detailed game state including snake position, food, score, etc.
    """
    player = db.get_active_player(playerId)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return player
