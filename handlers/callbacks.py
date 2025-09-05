import re
from aiogram import types, Router, F

from handlers.quiz import next_question_or_finish
from utils.quiz_data import quiz_data
from database import get_db_session
from components.database.quiz_repository import get_quiz_index, save_user_answer

router = Router()

ANSWER_PATTERN = re.compile(r"answer_(\d+)_(\d+)")

@router.callback_query(F.data.startswith("answer_"))
async def handle_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    # Парсим callback data
    match = ANSWER_PATTERN.match(callback.data)
    if not match:
        await callback.answer("Ошибка обработки ответа")
        return
    
    selected_index = int(match.group(1))
    correct_index = int(match.group(2))
    
    # Получаем данные вопроса
    async with get_db_session() as session:
        current_question_index = await get_quiz_index(session, user_id)
    
    question_data = quiz_data[current_question_index]
    user_answer_text = question_data['options'][selected_index]
    correct_answer_text = question_data['options'][correct_index]
    is_correct = (selected_index == correct_index)
    
    # Сохраняем ответ
    async with get_db_session() as session:
        await save_user_answer(session, user_id, current_question_index, user_answer_text, is_correct)
        await session.commit()
    
    # Удаляем кнопки
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    # Отправляем результат
    if is_correct:
        await callback.message.answer(f"✅ Вы ответили: {user_answer_text}\nВерно!")
    else:
        await callback.message.answer(f"❌ Вы ответили: {user_answer_text}\nПравильный ответ: {correct_answer_text}")
    
    await next_question_or_finish(callback.message, user_id)