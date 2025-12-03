"""
Application configuration using Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    app_name: str = "Snake Arena Masters API"
    api_v1_prefix: str = "/api/v1"

    # Security
    secret_key: str = "your-secret-key-change-in-production-please-use-a-strong-random-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost",  # Docker frontend
        "http://frontend",  # Docker service name
        "https://snake-arena-frontend.onrender.com",  # Render frontend
        "https://snake-arena-backend.onrender.com",  # Render backend (for docs)
    ]

    # Database
    database_url: str = "sqlite+aiosqlite:///./snake_arena.db"
    # For production, use: postgresql+asyncpg://user:password@localhost/dbname

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
