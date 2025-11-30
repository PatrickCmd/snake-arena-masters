"""
User database service.

This module provides database operations for users.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import UserDB
from app.models.schemas import User


async def create_user(db: AsyncSession, email: str, username: str, password_hash: str) -> User:
    """
    Create a new user.

    Args:
        db: Database session
        email: User email
        username: Username
        password_hash: Hashed password

    Returns:
        User: Created user

    Raises:
        ValueError: If email already exists
    """
    # Check if email exists
    result = await db.execute(select(UserDB).where(UserDB.email == email))
    if result.scalar_one_or_none():
        raise ValueError("Email already registered")

    # Create user
    db_user = UserDB(email=email, username=username, password_hash=password_hash)
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)

    return User(id=str(db_user.id), username=db_user.username, email=db_user.email)


async def get_user_by_email(db: AsyncSession, email: str) -> tuple[User, str] | None:
    """
    Get user and password hash by email.

    Args:
        db: Database session
        email: User email

    Returns:
        Tuple of (User, password_hash) or None if not found
    """
    result = await db.execute(select(UserDB).where(UserDB.email == email))
    db_user = result.scalar_one_or_none()

    if not db_user:
        return None

    user = User(id=str(db_user.id), username=db_user.username, email=db_user.email)
    return user, db_user.password_hash


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    """
    Get user by ID.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User or None if not found
    """
    try:
        user_id_int = int(user_id)
    except ValueError:
        return None

    result = await db.execute(select(UserDB).where(UserDB.id == user_id_int))
    db_user = result.scalar_one_or_none()

    if not db_user:
        return None

    return User(id=str(db_user.id), username=db_user.username, email=db_user.email)
