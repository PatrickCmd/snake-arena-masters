"""
Seed script to populate the database with demo data.

Run this script to add demo users and leaderboard entries to the database.
"""

import asyncio
from datetime import date

from app.config import settings
from app.models.db import Base, LeaderboardEntryDB, UserDB
from app.services.db_session import engine
from app.utils.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def seed_database():
    """Seed the database with demo data."""
    print("🌱 Seeding database...")

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        # Check if data already exists
        from sqlalchemy import select

        result = await session.execute(select(UserDB))
        if result.first():
            print("⚠️  Database already contains data. Skipping seed.")
            return

        # Create demo users
        demo_users = [
            ("DemoPlayer", "demo@snake.game", "demo123"),
            ("SnakeMaster", "master@snake.game", "master123"),
            ("PyThonKing", "python@snake.game", "python123"),
            ("NeonViper", "neon@snake.game", "neon123"),
            ("PixelSnake", "pixel@snake.game", "pixel123"),
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
            ("NeonViper", 1920, "walls", date(2024, 1, 14)),
            ("PixelSnake", 1750, "pass-through", date(2024, 1, 13)),
            ("RetroGamer", 1680, "walls", date(2024, 1, 13)),
            ("DemoPlayer", 1550, "pass-through", date(2024, 1, 12)),
            ("SpeedRunner", 1420, "walls", date(2024, 1, 12)),
            ("CasualGamer", 1280, "pass-through", date(2024, 1, 11)),
            ("ProSnake", 1150, "walls", date(2024, 1, 11)),
            ("Beginner", 890, "pass-through", date(2024, 1, 10)),
        ]

        print(f"Creating {len(demo_entries)} leaderboard entries...")
        for username, score, mode, entry_date in demo_entries:
            entry = LeaderboardEntryDB(
                username=username, score=score, mode=mode, date=entry_date
            )
            session.add(entry)

        await session.commit()

    print("✅ Database seeded successfully!")
    print(f"\n📊 Demo Data Summary:")
    print(f"   Users: {len(demo_users)}")
    print(f"   Leaderboard Entries: {len(demo_entries)}")
    print(f"\n🔑 Demo Credentials:")
    print(f"   Email: demo@snake.game")
    print(f"   Password: demo123")
    print(f"\n💾 Database: {settings.database_url}")


if __name__ == "__main__":
    asyncio.run(seed_database())
