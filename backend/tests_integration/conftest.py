"""
Integration test configuration and fixtures.

These tests use a real SQLite database to test the full stack.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.models.db import Base
from app.services.db_session import get_db
from app.utils.security import get_password_hash

# Integration test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_db_engine():
    """Create a test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def test_db(test_db_engine):
    """Create a test database session."""
    AsyncSessionLocal = async_sessionmaker(
        test_db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        # Seed with demo users
        from app.models.db import UserDB

        demo_users = [
            UserDB(
                username="DemoPlayer",
                email="demo@snake.game",
                password_hash=get_password_hash("demo123"),
            ),
            UserDB(
                username="TestUser",
                email="test@snake.game",
                password_hash=get_password_hash("test123"),
            ),
        ]
        for user in demo_users:
            session.add(user)

        await session.commit()

        yield session


@pytest_asyncio.fixture
async def async_client(test_db):
    """Create an async test client with database override."""

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    from httpx import ASGITransport

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_token(async_client):
    """Get an authentication token for testing."""
    response = await async_client.post(
        "/api/v1/auth/login", data={"username": "demo@snake.game", "password": "demo123"}
    )
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def auth_headers(auth_token):
    """Get authorization headers with token."""
    return {"Authorization": f"Bearer {auth_token}"}
