"""
Leaderboard router for score management and leaderboard retrieval.
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import GameMode, LeaderboardEntry, SubmitScoreRequest, SubmitScoreResponse
from app.services import auth_service, leaderboard_service
from app.services.db_session import get_db
from app.utils.security import get_current_user_id

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    mode: GameMode | None = Query(None, description="Filter by game mode"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get leaderboard entries.

    Optionally filter by game mode (pass-through or walls).
    """
    return await leaderboard_service.get_leaderboard(db, mode)


@router.post("/scores", response_model=SubmitScoreResponse, status_code=status.HTTP_201_CREATED)
async def submit_score(
    request: SubmitScoreRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit a game score to the leaderboard.

    Only saves the score if it's better than the user's previous best for this mode.
    Requires authentication.
    """
    user = await auth_service.get_user_by_id(db, current_user_id)
    if not user:
        return SubmitScoreResponse(success=False, error="User not found")

    result = await leaderboard_service.add_leaderboard_entry(
        db, username=user.username, score=request.score, mode=request.mode
    )

    if not result["is_new_best"]:
        return SubmitScoreResponse(
            success=False,
            rank=result["rank"],
            error=f"Score not saved. Your best score is {result['previous_best']}",
        )

    return SubmitScoreResponse(success=True, rank=result["rank"])


@router.get("/best-score/{mode}", response_model=int | None)
async def get_user_best_score(
    mode: GameMode,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get the authenticated user's best score for a specific mode.

    Returns the best score or None if no scores exist.
    """
    user = await auth_service.get_user_by_id(db, current_user_id)
    if not user:
        return None

    best_score = await leaderboard_service.get_user_best_score(db, user.username, mode)
    return best_score
