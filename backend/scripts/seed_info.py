"""
Seed script to display mock database information.

This script shows all the demo users and their credentials
that are available in the mock database.
"""

from app.services.database import db


def main():
    """Display mock database information."""
    print("\n" + "=" * 60)
    print("SNAKE ARENA MASTERS - MOCK DATABASE")
    print("=" * 60)

    # Display users
    print("\n📝 DEMO USERS (for testing login):")
    print("-" * 60)
    demo_credentials = [
        ("DemoPlayer", "demo@snake.game", "demo123"),
        ("SnakeMaster", "master@snake.game", "master123"),
        ("PyThonKing", "python@snake.game", "python123"),
        ("NeonViper", "neon@snake.game", "neon123"),
        ("PixelSnake", "pixel@snake.game", "pixel123"),
    ]

    for username, email, password in demo_credentials:
        print(f"  Username: {username:15} | Email: {email:25} | Password: {password}")

    # Display leaderboard stats
    print("\n🏆 LEADERBOARD ENTRIES:")
    print("-" * 60)
    leaderboard = db.get_leaderboard()
    print(f"  Total entries: {len(leaderboard)}")
    print(f"  Top score: {leaderboard[0].score} by {leaderboard[0].username}")

    walls_entries = db.get_leaderboard(mode="walls")
    pass_through_entries = db.get_leaderboard(mode="pass-through")
    print(f"  Walls mode: {len(walls_entries)} entries")
    print(f"  Pass-through mode: {len(pass_through_entries)} entries")

    # Display active players
    print("\n👥 ACTIVE PLAYERS:")
    print("-" * 60)
    active_players = db.get_active_players()
    print(f"  Total active: {len(active_players)}")
    for player in active_players:
        print(f"  - {player.username}: {player.score} points ({player.mode} mode)")

    print("\n" + "=" * 60)
    print("💡 TIP: Use 'make run' to start the server")
    print("📚 API Docs: http://localhost:8000/docs")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
