from aiogram import types, Router, F
from aiogram.filters import Command

from database import get_db_session
from components.database.quiz_repository import get_user_stats, get_leaderboard

router = Router()

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    
    async with get_db_session() as session:
        last_result, overall_stats = await get_user_stats(session, user_id)
    
    if last_result:
        total_quizzes, avg_score, best_score = overall_stats or (0, 0, 0)
        
        response = (
            f"📊 Ваша статистика:\n\n"
            f"🎯 Последний результат:\n"
            f"   ✅ {last_result.correct_answers}/{last_result.total_questions} правильных ответов\n"
            f"   🏆 {last_result.score}% правильных ответов\n"
            f"   📅 {last_result.completed_at.strftime('%Y-%m-%d')}\n\n"
            f"📈 Общая статистика:\n"
            f"   🎮 Пройдено квизов: {total_quizzes}\n"
            f"   ⭐ Средний результат: {int(avg_score or 0)}%\n"
            f"   🏅 Лучший результат: {int(best_score or 0)}%"
        )
    else:
        response = "📊 Вы еще не проходили квиз. Начните с команды /quiz"
    
    await message.answer(response)

@router.message(Command("leaderboard"))
async def cmd_leaderboard(message: types.Message):
    async with get_db_session() as session:
        leaderboard = await get_leaderboard(session, limit=10)
    
    if leaderboard:
        response = "🏆 Таблица лидеров:\n\n"
        for i, (username, score, completed_at) in enumerate(leaderboard, 1):
            response += f"{i}. {username}: {score}% ({completed_at.strftime('%Y-%m-%d')})\n"
    else:
        response = "🏆 Пока никто не прошел квиз. Будьте первым! /quiz"
    
    await message.answer(response)