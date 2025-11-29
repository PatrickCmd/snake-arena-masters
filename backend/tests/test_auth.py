"""
Tests for authentication endpoints.
"""

from fastapi import status


def test_login_success(client):
    """Test successful login with valid credentials."""
    response = client.post(
        "/api/v1/auth/login", data={"username": "demo@snake.game", "password": "demo123"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_email(client):
    """Test login with invalid email."""
    response = client.post(
        "/api/v1/auth/login", data={"username": "invalid@email.com", "password": "password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_invalid_password(client):
    """Test login with invalid password."""
    response = client.post(
        "/api/v1/auth/login", data={"username": "demo@snake.game", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_signup_success(client):
    """Test successful user registration."""
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "newuser@test.com", "username": "NewUser", "password": "password123"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["success"] is True
    assert data["user"]["username"] == "NewUser"
    assert data["user"]["email"] == "newuser@test.com"


def test_signup_existing_email(client):
    """Test signup with existing email."""
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "demo@snake.game", "username": "AnotherUser", "password": "password"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["success"] is False
    assert "error" in data


def test_get_current_user_authenticated(client, auth_headers):
    """Test getting current user when authenticated."""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "demo@snake.game"
    assert data["username"] == "DemoPlayer"


def test_get_current_user_unauthenticated(client):
    """Test getting current user without authentication."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout(client, auth_headers):
    """Test logout endpoint."""
    response = client.post("/api/v1/auth/logout", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
