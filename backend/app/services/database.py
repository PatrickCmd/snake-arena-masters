"""
Mock in-memory database for development.

This module provides a simple in-memory database using Python dictionaries.
It will be replaced with a real database in production.
"""

from datetime import date
from threading import Lock

from app.models.schemas import (
    ActivePlayer,
    Direction,
    GameMode,
    GameState,
    LeaderboardEntry,
    Position,
    User,
)
from app.utils.security import get_password_hash


class MockDatabase:
    """Thread-safe mock database."""

    def __init__(self):
        self._lock = Lock()
        self._users: dict[str, dict] = {}  # user_id -> {user: User, password_hash: str}
        self._users_by_email: dict[str, str] = {}  # email -> user_id
        self._leaderboard: list[LeaderboardEntry] = []
        self._active_players: dict[str, ActivePlayer] = {}
        self._next_user_id = 1
        self._next_leaderboard_id = 1
        self._next_player_id = 1

        # Initialize with demo data
        self._initialize_demo_data()

    def _initialize_demo_data(self):
        """Initialize database with demo data."""
        # Demo users
        demo_users = [
            ("1", "DemoPlayer", "demo@snake.game", "demo123"),
            ("2", "SnakeMaster", "master@snake.game", "master123"),
            ("3", "PyThonKing", "python@snake.game", "python123"),
            ("4", "NeonViper", "neon@snake.game", "neon123"),
            ("5", "PixelSnake", "pixel@snake.game", "pixel123"),
        ]

        for user_id, username, email, password in demo_users:
            user = User(id=user_id, username=username, email=email)
            self._users[user_id] = {"user": user, "password_hash": get_password_hash(password)}
            self._users_by_email[email] = user_id

        self._next_user_id = 6

        # Demo leaderboard entries (expanded)
        demo_entries = [
            LeaderboardEntry(
                id="1",
                username="SnakeMaster",
                score=2450,
                mode=GameMode.WALLS,
                date=date(2024, 1, 15),
            ),
            LeaderboardEntry(
                id="2",
                username="PyThonKing",
                score=2180,
                mode=GameMode.PASS_THROUGH,
                date=date(2024, 1, 14),
            ),
            LeaderboardEntry(
                id="3",
                username="NeonViper",
                score=1920,
                mode=GameMode.WALLS,
                date=date(2024, 1, 14),
            ),
            LeaderboardEntry(
                id="4",
                username="PixelSnake",
                score=1750,
                mode=GameMode.PASS_THROUGH,
                date=date(2024, 1, 13),
            ),
            LeaderboardEntry(
                id="5",
                username="RetroGamer",
                score=1680,
                mode=GameMode.WALLS,
                date=date(2024, 1, 13),
            ),
            LeaderboardEntry(
                id="6",
                username="DemoPlayer",
                score=1550,
                mode=GameMode.PASS_THROUGH,
                date=date(2024, 1, 12),
            ),
            LeaderboardEntry(
                id="7",
                username="SpeedRunner",
                score=1420,
                mode=GameMode.WALLS,
                date=date(2024, 1, 12),
            ),
            LeaderboardEntry(
                id="8",
                username="CasualGamer",
                score=1280,
                mode=GameMode.PASS_THROUGH,
                date=date(2024, 1, 11),
            ),
            LeaderboardEntry(
                id="9", username="ProSnake", score=1150, mode=GameMode.WALLS, date=date(2024, 1, 11)
            ),
            LeaderboardEntry(
                id="10",
                username="Beginner",
                score=890,
                mode=GameMode.PASS_THROUGH,
                date=date(2024, 1, 10),
            ),
        ]
        self._leaderboard = demo_entries
        self._next_leaderboard_id = 11

        # Demo active players (expanded with varied game states)
        demo_players = [
            ActivePlayer(
                id="ap1",
                username="LivePlayer1",
                score=340,
                mode=GameMode.WALLS,
                gameState=GameState(
                    snake=[
                        Position(x=10, y=10),
                        Position(x=9, y=10),
                        Position(x=8, y=10),
                        Position(x=7, y=10),
                    ],
                    food=Position(x=15, y=15),
                    direction=Direction.RIGHT,
                    score=340,
                    isGameOver=False,
                    isPaused=False,
                    mode=GameMode.WALLS,
                    speed=150,
                ),
            ),
            ActivePlayer(
                id="ap2",
                username="LivePlayer2",
                score=520,
                mode=GameMode.PASS_THROUGH,
                gameState=GameState(
                    snake=[
                        Position(x=5, y=5),
                        Position(x=5, y=6),
                        Position(x=5, y=7),
                        Position(x=5, y=8),
                        Position(x=5, y=9),
                    ],
                    food=Position(x=12, y=8),
                    direction=Direction.UP,
                    score=520,
                    isGameOver=False,
                    isPaused=False,
                    mode=GameMode.PASS_THROUGH,
                    speed=120,
                ),
            ),
            ActivePlayer(
                id="ap3",
                username="SpeedDemon",
                score=780,
                mode=GameMode.WALLS,
                gameState=GameState(
                    snake=[
                        Position(x=15, y=12),
                        Position(x=14, y=12),
                        Position(x=13, y=12),
                        Position(x=12, y=12),
                        Position(x=11, y=12),
                        Position(x=10, y=12),
                    ],
                    food=Position(x=8, y=8),
                    direction=Direction.LEFT,
                    score=780,
                    isGameOver=False,
                    isPaused=False,
                    mode=GameMode.WALLS,
                    speed=100,
                ),
            ),
        ]
        for player in demo_players:
            self._active_players[player.id] = player
        self._next_player_id = 4

    def _create_demo_game_state(self, mode: GameMode) -> GameState:
        """Create a demo game state."""
        return GameState(
            snake=[Position(x=10, y=10), Position(x=9, y=10), Position(x=8, y=10)],
            food=Position(x=15, y=15),
            direction=Direction.RIGHT,
            score=0,
            isGameOver=False,
            isPaused=False,
            mode=mode,
            speed=150,
        )

    # User operations
    def create_user(self, email: str, username: str, password_hash: str) -> User:
        """Create a new user."""
        with self._lock:
            if email in self._users_by_email:
                raise ValueError("Email already registered")

            user_id = str(self._next_user_id)
            self._next_user_id += 1

            user = User(id=user_id, username=username, email=email)
            self._users[user_id] = {"user": user, "password_hash": password_hash}
            self._users_by_email[email] = user_id

            return user

    def get_user_by_email(self, email: str) -> tuple[User, str] | None:
        """Get user and password hash by email."""
        with self._lock:
            user_id = self._users_by_email.get(email)
            if not user_id:
                return None
            user_data = self._users.get(user_id)
            if not user_data:
                return None
            return user_data["user"], user_data["password_hash"]

    def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        with self._lock:
            user_data = self._users.get(user_id)
            return user_data["user"] if user_data else None

    # Leaderboard operations
    def get_leaderboard(self, mode: GameMode | None = None) -> list[LeaderboardEntry]:
        """Get leaderboard entries, optionally filtered by mode."""
        with self._lock:
            if mode:
                return [entry for entry in self._leaderboard if entry.mode == mode]
            return self._leaderboard.copy()

    def add_leaderboard_entry(self, username: str, score: int, mode: GameMode) -> int:
        """Add a leaderboard entry and return the rank."""
        with self._lock:
            entry_id = str(self._next_leaderboard_id)
            self._next_leaderboard_id += 1

            entry = LeaderboardEntry(
                id=entry_id, username=username, score=score, mode=mode, date=date.today()
            )

            self._leaderboard.append(entry)
            # Sort by score descending
            self._leaderboard.sort(key=lambda x: x.score, reverse=True)

            # Find rank
            rank = next(i + 1 for i, e in enumerate(self._leaderboard) if e.id == entry_id)
            return rank

    # Active players operations
    def get_active_players(self) -> list[ActivePlayer]:
        """Get all active players."""
        with self._lock:
            return list(self._active_players.values())

    def get_active_player(self, player_id: str) -> ActivePlayer | None:
        """Get an active player by ID."""
        with self._lock:
            return self._active_players.get(player_id)


# Global database instance
db = MockDatabase()
