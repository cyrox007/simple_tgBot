from aiogram import types, Router, F

from handlers.quiz import next_question_or_finish
from utils.quiz_data import quiz_data
from database import get_db_session
from components.database.quiz_repository import get_quiz_index, save_user_answer

router = Router()

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_answer = callback.message.reply_markup.inline_keyboard[0][0].text
    
    async with get_db_session() as session:
        current_question_index = await get_quiz_index(session, user_id)
        await save_user_answer(session, user_id, current_question_index, user_answer, is_correct=True)
    
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    await callback.message.answer(f"✅ Вы ответили: {user_answer}\nВерно!")
    await next_question_or_finish(callback.message, user_id)

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_answer = callback.message.reply_markup.inline_keyboard[0][0].text
    
    async with get_db_session() as session:
        current_question_index = await get_quiz_index(session, user_id)
        await save_user_answer(session, user_id, current_question_index, user_answer, is_correct=False)
    
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    correct_option = quiz_data[current_question_index]['options'][quiz_data[current_question_index]['correct_option']]
    
    await callback.message.answer(f"❌ Вы ответили: {user_answer}\nПравильный ответ: {correct_option}")
    await next_question_or_finish(callback.message, user_id)