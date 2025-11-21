import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from fastapi.testclient import TestClient
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # in-memory БД

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(engine):
    """fixture создаёт транзакцию для каждого теста и откатывает её после теста."""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin_nested():  # начало вложенной транзакции
            yield session
            await session.rollback()  # откатываем изменения после теста

@pytest.fixture
def client(db_session):
    # Подменяем сессию в приложении на нашу fixture
    app.dependency_overrides[lambda: None] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}
