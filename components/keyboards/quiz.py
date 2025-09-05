from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from utils.quiz_data import quiz_data

def generate_quiz_keyboard(current_question_index: int):
    builder = InlineKeyboardBuilder()
    
    question_data = quiz_data[current_question_index]
    correct_option = question_data['options'][question_data['correct_option']]
    
    for option in question_data['options']:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == correct_option else "wrong_answer"
        ))
    
    builder.adjust(1)
    return builder.as_markup()
