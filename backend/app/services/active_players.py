"""
In-memory storage for active players.

Active players and their game states are kept in memory for performance.
This data is transient and does not need to be persisted to the database.
"""

from threading import Lock

from app.models.schemas import ActivePlayer, Direction, GameMode, GameState, Position

# Demo active players (in-memory)
_active_players: dict[str, ActivePlayer] = {}
_lock = Lock()


def _initialize_demo_players():
    """Initialize demo active players."""
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

    with _lock:
        for player in demo_players:
            _active_players[player.id] = player


# Initialize on module load
_initialize_demo_players()


def get_active_players() -> list[ActivePlayer]:
    """Get all active players."""
    with _lock:
        return list(_active_players.values())


def get_active_player(player_id: str) -> ActivePlayer | None:
    """Get an active player by ID."""
    with _lock:
        return _active_players.get(player_id)
