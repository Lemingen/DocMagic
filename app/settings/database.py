from sqlalchemy import create_engine
from app.settings.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_async_engine(
    url = settings.get_database_url,
    echo = True
)

async_session_factory = sessionmaker(
    bind = engine,
    expire_on_commit = False,
    class_= AsyncSession
)

sync_engine = create_engine(
    url = settings.sync_database_url,
    echo = True
)

sync_session_factory = sessionmaker(bind=sync_engine)

class Base(DeclarativeBase):
    ...