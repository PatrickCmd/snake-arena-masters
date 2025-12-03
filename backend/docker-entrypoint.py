"""
Docker entrypoint script to initialize database and start the application.
"""

import asyncio
import sys

from app.config import settings
from app.models.db import Base
from app.services.db_session import engine


async def init_database():
    """Initialize database tables."""
    print("🔧 Initializing database...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False


async def seed_database():
    """Seed database with demo data if empty."""
    from datetime import date

    from app.models.db import LeaderboardEntryDB, UserDB
    from app.services.db_session import AsyncSessionLocal
    from app.utils.security import get_password_hash
    from sqlalchemy import select

    print("🌱 Checking if database needs seeding...")

    async with AsyncSessionLocal() as session:
        # Check if data already exists
        result = await session.execute(select(UserDB))
        if result.first():
            print("⚠️  Database already contains data. Skipping seed.")
            return True

        try:
            # Create demo users
            demo_users = [
                ("DemoPlayer", "demo@snake.game", "demo123"),
                ("SnakeMaster", "master@snake.game", "master123"),
                ("PyThonKing", "python@snake.game", "python123"),
            ]

            print(f"Creating {len(demo_users)} demo users...")
            for username, email, password in demo_users:
                user = UserDB(
                    username=username, email=email, password_hash=get_password_hash(password)
                )
                session.add(user)

            await session.flush()

            # Create demo leaderboard entries
            demo_entries = [
                ("SnakeMaster", 2450, "walls", date(2024, 1, 15)),
                ("PyThonKing", 2180, "pass-through", date(2024, 1, 14)),
                ("DemoPlayer", 1550, "pass-through", date(2024, 1, 12)),
            ]

            print(f"Creating {len(demo_entries)} leaderboard entries...")
            for username, score, mode, entry_date in demo_entries:
                entry = LeaderboardEntryDB(
                    username=username, score=score, mode=mode, date=entry_date
                )
                session.add(entry)

            await session.commit()
            print("✅ Database seeded successfully!")
            print(f"\n🔑 Demo Credentials:")
            print(f"   Email: demo@snake.game")
            print(f"   Password: demo123")
            return True

        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            await session.rollback()
            return False


async def main():
    """Main entrypoint function."""
    print(f"🚀 Starting Snake Arena Masters Backend")
    print(f"📊 Database: {settings.database_url}")

    # Initialize database
    if not await init_database():
        sys.exit(1)

    # Seed database
    if not await seed_database():
        print("⚠️  Warning: Database seeding failed, but continuing...")

    print("✅ Initialization complete!")


if __name__ == "__main__":
    asyncio.run(main())
