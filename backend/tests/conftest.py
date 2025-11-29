"""
Pytest configuration and fixtures for testing.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.database import MockDatabase


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def test_db():
    """Create a fresh test database."""
    return MockDatabase()


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
