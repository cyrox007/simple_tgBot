from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from components.keyboards.quiz import generate_quiz_keyboard
from utils.quiz_data import quiz_data
from database import get_db_session
from components.database.quiz_repository import clear_user_answers, get_quiz_index, update_quiz_index, save_quiz_result, get_correct_answers_count

router = Router()

@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)

async def new_quiz(message: types.Message):
    user_id = message.from_user.id
    async with get_db_session() as session:
        # Очищаем предыдущие ответы
        await clear_user_answers(session, user_id)
        await update_quiz_index(session, user_id, 0)
        await session.commit()
    
    await get_question(message, user_id)

async def get_question(message: types.Message, user_id: int):
    async with get_db_session() as session:
        current_question_index = await get_quiz_index(session, user_id)
    
    if current_question_index < len(quiz_data):
        kb = generate_quiz_keyboard(current_question_index)
        await message.answer(f"Вопрос {current_question_index + 1}/{len(quiz_data)}:\n{quiz_data[current_question_index]['question']}", reply_markup=kb)
    else:
        await message.answer("Квиз уже завершен. Начните заново с помощью команды /quiz.")

async def next_question_or_finish(message: types.Message, user_id: int):
    async with get_db_session() as session:
        current_question_index = await get_quiz_index(session, user_id)
        current_question_index += 1
        await update_quiz_index(session, user_id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(message, user_id)
    else:
        await finish_quiz(message, user_id)

async def finish_quiz(message: types.Message, user_id: int):
    async with get_db_session() as session:
        total_questions = len(quiz_data)
        correct_answers = await get_correct_answers_count(session, user_id)
        username = message.from_user.username or message.from_user.first_name
        
        await save_quiz_result(session, user_id, username, total_questions, correct_answers)
    
    score = int((correct_answers / total_questions) * 100)
    
    await message.answer(
        f"🎉 Квиз завершен!\n\n"
        f"📊 Ваш результат:\n"
        f"✅ Правильных ответов: {correct_answers}/{total_questions}\n"
        f"🏆 Процент правильных: {score}%\n\n"
        f"Чтобы посмотреть статистику, используйте /stats\n"
        f"Чтобы увидеть таблицу лидеров, используйте /leaderboard"
    )