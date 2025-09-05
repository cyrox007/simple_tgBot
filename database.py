import aiosqlite
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from settings import config
from components.models.models import Base

# Для асинхронной работы с aiosqlite
async def get_async_db():
    async with aiosqlite.connect(config.DB_PATH) as db:
        yield db

# Для SQLAlchemy (опционально)
async_engine = create_async_engine(f'sqlite+aiosqlite:///{config.DB_PATH}')
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)