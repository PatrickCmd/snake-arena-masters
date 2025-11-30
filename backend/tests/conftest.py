"""
Pytest configuration and fixtures for testing.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.models.db import Base
from app.services.db_session import get_db
from app.utils.security import get_password_hash

# Test database URL (in-memory SQLite)
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
        # Seed with demo user
        from app.models.db import LeaderboardEntryDB, UserDB
        from datetime import date

        demo_user = UserDB(
            username="DemoPlayer",
            email="demo@snake.game",
            password_hash=get_password_hash("demo123"),
        )
        session.add(demo_user)

        # Add some leaderboard entries for testing
        demo_entries = [
            LeaderboardEntryDB(username="Player1", score=1000, mode="walls", date=date.today()),
            LeaderboardEntryDB(
                username="Player2", score=800, mode="pass-through", date=date.today()
            ),
            LeaderboardEntryDB(username="Player3", score=600, mode="walls", date=date.today()),
        ]
        for entry in demo_entries:
            session.add(entry)

        await session.commit()

        yield session


@pytest.fixture
def client(test_db):
    """Create a test client with database override."""

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(client):
    """Get an authentication token for testing."""
    # Login with demo user
    response = client.post(
        "/api/v1/auth/login", data={"username": "demo@snake.game", "password": "demo123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Get authorization headers with token."""
    return {"Authorization": f"Bearer {auth_token}"}
