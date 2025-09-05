from aiogram import types, Router, F
from aiogram.filters import Command

from handlers.quiz import get_quiz_index, next_question_or_finish
from utils.quiz_data import quiz_data
from database import get_async_db

router = Router()

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer("Верно!")
    await next_question_or_finish(callback.message, callback.from_user.id)

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['options'][quiz_data[current_question_index]['correct_option']]
    
    await callback.message.answer(f"Неправильно. Правильный ответ: {correct_option}")
    await next_question_or_finish(callback.message, callback.from_user.id)