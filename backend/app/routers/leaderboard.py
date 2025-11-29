"""
Leaderboard router for score management and leaderboard retrieval.
"""

from fastapi import APIRouter, Depends, Query, status

from app.models.schemas import (
    GameMode,
    LeaderboardEntry,
    SubmitScoreRequest,
    SubmitScoreResponse,
)
from app.services.auth_service import auth_service
from app.services.database import db
from app.utils.security import get_current_user_id

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
async def get_leaderboard(mode: GameMode | None = Query(None, description="Filter by game mode")):
    """
    Get leaderboard entries.

    Optionally filter by game mode (pass-through or walls).
    """
    return db.get_leaderboard(mode)


@router.post("/scores", response_model=SubmitScoreResponse, status_code=status.HTTP_201_CREATED)
async def submit_score(
    request: SubmitScoreRequest, current_user_id: str = Depends(get_current_user_id)
):
    """
    Submit a game score to the leaderboard.

    Requires authentication.
    """
    user = auth_service.get_user_by_id(current_user_id)
    if not user:
        return SubmitScoreResponse(success=False, error="User not found")

    rank = db.add_leaderboard_entry(username=user.username, score=request.score, mode=request.mode)

    return SubmitScoreResponse(success=True, rank=rank)
