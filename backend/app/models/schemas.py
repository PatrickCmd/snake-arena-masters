"""
Pydantic models for Snake Arena Masters API.

This module contains all request/response models and data schemas
based on the OpenAPI specification.
"""

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Enums
class GameMode(str, Enum):
    """Game mode enumeration."""

    PASS_THROUGH = "pass-through"
    WALLS = "walls"


class Direction(str, Enum):
    """Snake direction enumeration."""

    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


# Core Models
class Position(BaseModel):
    """Position on the game grid."""

    x: int = Field(..., ge=0, description="X coordinate")
    y: int = Field(..., ge=0, description="Y coordinate")


class GameState(BaseModel):
    """Complete game state."""

    snake: list[Position] = Field(..., description="Array of positions representing the snake body")
    food: Position
    direction: Direction
    score: int = Field(..., ge=0)
    isGameOver: bool = Field(default=False, alias="isGameOver")
    isPaused: bool = Field(default=False, alias="isPaused")
    mode: GameMode
    speed: int = Field(..., ge=1, description="Game speed in milliseconds between moves")

    model_config = ConfigDict(populate_by_name=True)


class User(BaseModel):
    """User account information."""

    id: str
    username: str
    email: EmailStr


class LeaderboardEntry(BaseModel):
    """Leaderboard entry."""

    id: str
    username: str
    score: int = Field(..., ge=0)
    mode: GameMode
    date: date


class ActivePlayer(BaseModel):
    """Active player with current game state."""

    id: str
    username: str
    score: int = Field(..., ge=0)
    mode: GameMode
    gameState: GameState = Field(..., alias="gameState")

    model_config = ConfigDict(populate_by_name=True)


# Request Models
class LoginRequest(BaseModel):
    """Login request payload."""

    email: EmailStr
    password: str = Field(..., min_length=6)


class SignupRequest(BaseModel):
    """Signup request payload."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)


class SubmitScoreRequest(BaseModel):
    """Submit score request payload."""

    score: int = Field(..., ge=0)
    mode: GameMode


# Response Models
class AuthResponse(BaseModel):
    """Authentication response."""

    success: bool
    user: User | None = None
    error: str | None = None


class SubmitScoreResponse(BaseModel):
    """Submit score response."""

    success: bool
    rank: int | None = None
    error: str | None = None


class ErrorResponse(BaseModel):
    """Generic error response."""

    error: str


# Token Models
class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""

    user_id: str | None = None
