import asyncio

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

from db import engine

# For Alembic migrations
# from exercise_2_sqlite.db import engine


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "t_book"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, index=True)
    author: Mapped[str] = mapped_column(String, nullable=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())
