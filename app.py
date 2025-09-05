import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher

from settings import config
from database import init_db
from handlers.start import router as start_router
from handlers.quiz import router as quiz_router
from handlers.callbacks import router as callbacks_router
from handlers.stats import router as stats_router

async def create_app():
    # Инициализация базы данных
    await init_db()
    
    # Создание бота и диспетчера
    bot = Bot(token=config.API_TOKEN)
    dp = Dispatcher()
    
    # Подключение роутеров
    dp.include_router(start_router)
    dp.include_router(quiz_router)
    dp.include_router(callbacks_router)
    dp.include_router(stats_router)
    
    # Запуск поллинга
    await dp.start_polling(bot)