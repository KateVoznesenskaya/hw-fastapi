from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from config import DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST
from models import metadata
from typing import AsyncGenerator
from database import get_async_session
from main import app
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.pool import NullPool

engine_test = create_async_engine(f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}", poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
app.dependency_overrides[get_async_session] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def init_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)

@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac