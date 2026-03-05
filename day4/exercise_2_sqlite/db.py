from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DB_FILE = Path(__file__).resolve().parent / "books.db"
DB_URL = f"sqlite+aiosqlite:///{DB_FILE}"

engine = create_async_engine(DB_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
