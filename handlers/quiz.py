from aiogram import Router, F, types
from aiogram.filters import Command
import aiosqlite

from settings import config
from utils.quiz_data import quiz_data
from components.keyboards.quiz import generate_quiz_keyboard


router = Router()

@router.message(F.text == "Начать игру")
@router.message(Command('quiz'))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)


async def new_quiz(message: types.Message):
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0)
    await get_question(message, user_id)

async def get_quiz_index(user_id: int):
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def update_quiz_index(user_id: int, index: int):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)',
            (user_id, index)
        )
        await db.commit()

async def get_question(message: types.Message, user_id: int):
    current_question_index = await get_quiz_index(user_id)

    if current_question_index < len(quiz_data):
        kb = generate_quiz_keyboard(current_question_index)
        await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)
    else: 
        await message.answer("Квиз уже завершен. Начните заново с помощью команды /quiz.")

async def next_question_or_finish(message: types.Message, user_id: int):
    current_question_index = await get_quiz_index(user_id)
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(message, user_id)
    else:
        await message.answer("Это был последний вопрос. Квиз завершен!")