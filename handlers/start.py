from aiogram import types, Router
from aiogram.filters import Command

from components.keyboards.main_menu import get_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в квиз!", reply_markup=get_main_keyboard())
