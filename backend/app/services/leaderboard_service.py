"""
Leaderboard database service.

This module provides database operations for leaderboard entries.
"""

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import LeaderboardEntryDB
from app.models.schemas import GameMode, LeaderboardEntry


async def get_leaderboard(
    db: AsyncSession, mode: GameMode | None = None
) -> list[LeaderboardEntry]:
    """
    Get leaderboard entries, optionally filtered by mode.

    Args:
        db: Database session
        mode: Optional game mode filter

    Returns:
        List of leaderboard entries sorted by score (descending)
    """
    query = select(LeaderboardEntryDB).order_by(LeaderboardEntryDB.score.desc())

    if mode:
        query = query.where(LeaderboardEntryDB.mode == mode.value)

    result = await db.execute(query)
    db_entries = result.scalars().all()

    return [
        LeaderboardEntry(
            id=str(entry.id),
            username=entry.username,
            score=entry.score,
            mode=GameMode(entry.mode),
            date=entry.date,
        )
        for entry in db_entries
    ]


async def get_user_best_score(
    db: AsyncSession, username: str, mode: GameMode
) -> int | None:
    """
    Get user's best score for a specific mode.

    Args:
        db: Database session
        username: Player username
        mode: Game mode

    Returns:
        Best score or None if no scores exist
    """
    result = await db.execute(
        select(LeaderboardEntryDB)
        .where(LeaderboardEntryDB.username == username, LeaderboardEntryDB.mode == mode.value)
        .order_by(LeaderboardEntryDB.score.desc())
        .limit(1)
    )
    best_entry = result.scalar_one_or_none()
    return best_entry.score if best_entry else None


async def add_leaderboard_entry(
    db: AsyncSession, username: str, score: int, mode: GameMode
) -> dict:
    """
    Add a leaderboard entry only if it's better than the user's previous best.

    Args:
        db: Database session
        username: Player username
        score: Score achieved
        mode: Game mode

    Returns:
        Dict with rank and whether it was a new best score
    """
    # Check user's previous best score
    previous_best = await get_user_best_score(db, username, mode)

    # Only save if this is a new best score
    if previous_best is not None and score <= previous_best:
        # Calculate rank for current score (even though we're not saving it)
        result = await db.execute(
            select(LeaderboardEntryDB).where(
                LeaderboardEntryDB.mode == mode.value, LeaderboardEntryDB.score > score
            )
        )
        higher_scores = len(result.scalars().all())
        return {
            "rank": higher_scores + 1,
            "is_new_best": False,
            "previous_best": previous_best,
        }

    # Create entry
    db_entry = LeaderboardEntryDB(
        username=username, score=score, mode=mode.value, date=date.today()
    )
    db.add(db_entry)
    await db.flush()
    await db.refresh(db_entry)

    # Calculate rank by counting entries with higher scores in the same mode
    result = await db.execute(
        select(LeaderboardEntryDB).where(
            LeaderboardEntryDB.mode == mode.value, LeaderboardEntryDB.score > score
        )
    )
    higher_scores = len(result.scalars().all())

    return {
        "rank": higher_scores + 1,
        "is_new_best": True,
        "previous_best": previous_best,
    }
