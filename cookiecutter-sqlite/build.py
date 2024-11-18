# Use this script to create the database and run the migrations
import asyncio
from pathlib import Path

from engine import engine

root = Path(__file__).parent


async def main():
    try:
        desc = input("Enter a description for the migration: ")
        print(await engine.create_migrations(root, True, desc))
    except Exception as e:
        print(f"Error: {e}")
        print(await engine.diagnose_issues(root))


if __name__ == "__main__":
    asyncio.run(main())
