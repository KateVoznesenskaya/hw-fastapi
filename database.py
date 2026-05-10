from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from typing import AsyncGenerator

engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session