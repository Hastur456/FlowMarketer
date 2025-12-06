# tests/conftest.py
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import delete

from app.models.base import Base
from app.database.session import set_test_session_maker


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Event loop для всех тестов"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_engine():
    """Создать тестовый engine"""
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
    
    # Создать все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Удалить все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(async_engine):
    """Тестовая сессия для каждого теста"""
    async_session_maker_test = async_sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
    )
    
    # ✅ УСТАНОВИТЬ тестовый session_maker
    set_test_session_maker(async_session_maker_test)
    
    async with async_session_maker_test() as session:
        # ✅ Очистить ВСЕ таблицы ДО теста
        for table in Base.metadata.tables.values():
            await session.execute(delete(table))
        await session.commit()
        
        yield session
        
        # ✅ Очистить ПОСЛЕ теста
        for table in Base.metadata.tables.values():
            await session.execute(delete(table))
        await session.commit()
    
    # ✅ СБРОСИТЬ в None после теста
    set_test_session_maker(None)
