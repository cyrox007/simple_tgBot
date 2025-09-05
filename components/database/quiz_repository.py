from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from components.models.models import QuizState, QuizResult, UserAnswer

async def get_quiz_index(session: AsyncSession, user_id: int) -> int:
    """Получение текущего индекса вопроса для пользователя"""
    result = await session.execute(
        select(QuizState.question_index)
        .where(QuizState.user_id == user_id)
    )
    quiz_state = result.scalar_one_or_none()
    
    if quiz_state is not None:
        return quiz_state
    else:
        # Создаем новую запись
        new_state = QuizState(user_id=user_id, question_index=0)
        session.add(new_state)
        await session.commit()
        return 0

async def update_quiz_index(session: AsyncSession, user_id: int, index: int):
    """Обновление индекса вопроса"""
    result = await session.execute(
        select(QuizState).where(QuizState.user_id == user_id)
    )
    quiz_state = result.scalar_one_or_none()
    
    if quiz_state:
        quiz_state.question_index = index
    else:
        quiz_state = QuizState(user_id=user_id, question_index=index)
        session.add(quiz_state)
    
    await session.commit()

async def save_user_answer(session: AsyncSession, user_id: int, question_index: int, user_answer: str, is_correct: bool):
    """Сохранение ответа пользователя"""
    user_answer_obj = UserAnswer(
        user_id=user_id,
        question_index=question_index,
        user_answer=user_answer,
        is_correct=is_correct,
        answered_at=datetime.now()
    )
    session.add(user_answer_obj)
    await session.commit()

async def save_quiz_result(session: AsyncSession, user_id: int, username: str, total_questions: int, correct_answers: int):
    """Сохранение результата квиза"""
    score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    
    quiz_result = QuizResult(
        user_id=user_id,
        username=username,
        total_questions=total_questions,
        correct_answers=correct_answers,
        score=score,
        completed_at=datetime.now()
    )
    session.add(quiz_result)
    await session.commit()

async def get_user_stats(session: AsyncSession, user_id: int):
    """Получение статистики пользователя"""
    # Последний результат
    last_result = await session.execute(
        select(QuizResult)
        .where(QuizResult.user_id == user_id)
        .order_by(QuizResult.completed_at.desc())
        .limit(1)
    )
    last_result = last_result.scalar_one_or_none()
    
    # Общая статистика
    overall_stats = await session.execute(
        select(
            func.count(QuizResult.id).label('total_quizzes'),
            func.avg(QuizResult.score).label('avg_score'),
            func.max(QuizResult.score).label('best_score')
        )
        .where(QuizResult.user_id == user_id)
    )
    overall_stats = overall_stats.first()
    
    return last_result, overall_stats

async def get_leaderboard(session: AsyncSession, limit: int = 10):
    """Получение таблицы лидеров"""
    result = await session.execute(
        select(QuizResult.username, QuizResult.score, QuizResult.completed_at)
        .order_by(QuizResult.score.desc(), QuizResult.completed_at.desc())
        .limit(limit)
    )
    return result.all()

async def get_correct_answers_count(session: AsyncSession, user_id: int):
    """Подсчет правильных ответов"""
    result = await session.execute(
        select(func.count(UserAnswer.id))
        .where(UserAnswer.user_id == user_id)
        .where(UserAnswer.is_correct == True)
    )
    return result.scalar() or 0