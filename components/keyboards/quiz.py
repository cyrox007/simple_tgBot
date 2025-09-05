from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from utils.quiz_data import quiz_data

def generate_quiz_keyboard(current_question_index: int):
    builder = InlineKeyboardBuilder()
    
    question_data = quiz_data[current_question_index]
    correct_option_index = question_data['correct_option']
    
    for i, option in enumerate(question_data['options']):
        # Передаем индекс варианта ответа в callback data
        callback_data = f"answer_{i}_{correct_option_index}"
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=callback_data
        ))
    
    builder.adjust(1)
    return builder.as_markup()
