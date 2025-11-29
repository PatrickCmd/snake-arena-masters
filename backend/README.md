# Snake Arena Masters - Backend API

Backend API for the Snake Arena Masters multiplayer snake game, built with FastAPI.

## Features

- 🔐 **JWT Authentication** - Secure user authentication with password hashing
- 🏆 **Leaderboard System** - Track and display high scores by game mode
- 👀 **Live Spectating** - Watch active players in real-time
- 📊 **Mock Database** - In-memory database for development (easily replaceable)
- ✅ **Comprehensive Tests** - Full test coverage with pytest
- 📚 **Auto-generated API Docs** - Interactive Swagger UI and ReDoc

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **Pydantic** - Data validation using Python type annotations
- **python-jose** - JWT token generation and validation
- **passlib** - Password hashing with argon2
- **pytest** - Testing framework
- **ruff** - Fast Python linter and formatter
- **uvicorn** - ASGI server

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── leaderboard.py   # Leaderboard endpoints
│   │   └── spectate.py      # Spectate endpoints
│   ├── services/
│   │   ├── auth_service.py  # Auth business logic
│   │   └── database.py      # Mock database
│   └── utils/
│       └── security.py      # JWT & password utilities
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   ├── test_leaderboard.py  # Leaderboard tests
│   └── test_spectate.py     # Spectate tests
├── pyproject.toml           # Project dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer

### Installation

1. **Install dependencies:**
   ```bash
   uv sync --dev
   ```

2. **Run the development server:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` - User login (returns JWT token)
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user (requires auth)

### Leaderboard

- `GET /api/v1/leaderboard` - Get leaderboard entries (optional `?mode=` filter)
- `POST /api/v1/leaderboard/scores` - Submit score (requires auth)

### Spectate

- `GET /api/v1/spectate/players` - Get active players
- `GET /api/v1/spectate/players/{playerId}` - Get player game state

## Testing

Run all tests:
```bash
uv run pytest
```

Run with verbose output:
```bash
uv run pytest -v
```

Run with coverage:
```bash
uv run pytest --cov=app tests/
```

## Configuration

Configuration is managed via `app/config.py` using Pydantic Settings. You can override settings using environment variables or a `.env` file.

Key settings:
- `SECRET_KEY` - JWT secret key (change in production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30)
- `CORS_ORIGINS` - Allowed CORS origins

Example `.env` file:
```env
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Authentication Flow

1. **Register** a new user via `/api/v1/auth/signup`
2. **Login** with email/password via `/api/v1/auth/login` to get a JWT token
3. **Use the token** in subsequent requests:
   ```
   Authorization: Bearer <your-token>
   ```

## Mock Database

The current implementation uses an in-memory mock database (`app/services/database.py`). This is perfect for development and testing but will be replaced with a real database (PostgreSQL, MongoDB, etc.) in production.

The mock database includes:
- Thread-safe operations
- Demo data for testing
- Easy-to-replace interface

## Development

### Adding a New Endpoint

1. Define Pydantic models in `app/models/schemas.py`
2. Create router in `app/routers/`
3. Add business logic to `app/services/`
4. Include router in `app/main.py`
5. Write tests in `tests/`

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Document functions with docstrings
- Keep functions focused and modular

## Demo Credentials

The mock database includes multiple demo users for testing:

```bash
# View all demo users and database info
make seed-info
```

Quick test credentials:
- **Email:** demo@snake.game | **Password:** demo123
- **Email:** master@snake.game | **Password:** master123
- **Email:** python@snake.game | **Password:** python123

The database also includes:
- **10 leaderboard entries** across both game modes
- **3 active players** with live game states
- **5 demo users** ready for authentication testing

## Next Steps

- [ ] Replace mock database with PostgreSQL/MongoDB
- [ ] Add WebSocket support for real-time game updates
- [ ] Implement rate limiting
- [ ] Add user profile management
- [ ] Deploy to production

## License

Part of the Snake Arena Masters project.
