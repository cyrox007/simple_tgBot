from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    return builder.as_markup(resize_keyboard=True)