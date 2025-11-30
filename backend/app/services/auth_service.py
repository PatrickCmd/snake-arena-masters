"""
Authentication service for user management and authentication.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import User
from app.services import user_service
from app.utils.security import get_password_hash, verify_password


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """
    Authenticate a user with email and password.

    Args:
        db: Database session
        email: User email
        password: Plain text password

    Returns:
        User if authenticated, None otherwise
    """
    result = await user_service.get_user_by_email(db, email)
    if not result:
        return None

    user, password_hash = result
    if not verify_password(password, password_hash):
        return None

    return user


async def create_user(db: AsyncSession, email: str, username: str, password: str) -> User:
    """
    Create a new user.

    Args:
        db: Database session
        email: User email
        username: Username
        password: Plain text password

    Returns:
        Created user
    """
    password_hash = get_password_hash(password)
    return await user_service.create_user(db, email, username, password_hash)


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    """
    Get a user by ID.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User or None if not found
    """
    return await user_service.get_user_by_id(db, user_id)
