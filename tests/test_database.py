import pytest
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from app.settings import database
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import text


@pytest.mark.asyncio
async def test_get_async_session_returns_session():
    # получаем генератор
    session_generator = database.get_async_session()
    session = await anext(session_generator)

    assert isinstance(session, AsyncSession)
    await session.close()

def test_base_is_declarative():
    assert hasattr(database.Base, '__table__') is False  # базовый класс не имеет таблицы

def test_async_engine_created():
    assert isinstance(database.engine, AsyncEngine)

@pytest.mark.asyncio
async def test_async_session_factory():
    session = database.async_session_factory()
    assert isinstance(session, AsyncSession)
    await session.close()

def test_sync_engine_created():
    assert isinstance(database.sync_engine, Engine)

def test_sync_session_factory():
    session = database.sync_session_factory()
    assert isinstance(session, Session)
    session.close()

def test_sync_engine_connect():
    with database.sync_engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1