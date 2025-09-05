from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from settings import config
from components.models.models import Base

# Создаем асинхронный движок
async_engine = create_async_engine(
    f'sqlite+aiosqlite:///{config.DB_PATH}',
    echo=True
)

# Создаем асинхронную сессию
AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def init_db():
    """Инициализация таблиц через SQLAlchemy"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_db_session():
    """Асинхронный контекстный менеджер для работы с сессиями"""
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()