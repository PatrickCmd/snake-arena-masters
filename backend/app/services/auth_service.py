"""
Authentication service for user management and authentication.
"""

from app.models.schemas import User
from app.services.database import db
from app.utils.security import get_password_hash, verify_password


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def authenticate_user(email: str, password: str) -> User | None:
        """Authenticate a user with email and password."""
        result = db.get_user_by_email(email)
        if not result:
            return None

        user, password_hash = result
        if not verify_password(password, password_hash):
            return None

        return user

    @staticmethod
    def create_user(email: str, username: str, password: str) -> User:
        """Create a new user."""
        password_hash = get_password_hash(password)
        return db.create_user(email, username, password_hash)

    @staticmethod
    def get_user_by_id(user_id: str) -> User | None:
        """Get a user by ID."""
        return db.get_user_by_id(user_id)


auth_service = AuthService()
