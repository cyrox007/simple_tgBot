from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QuizState(Base):
    __tablename__ = 'quiz_state'
    
    user_id = Column(Integer, primary_key=True)
    question_index = Column(Integer, default=0)

class QuizResult(Base):
    __tablename__ = 'quiz_results'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    score = Column(Integer)
    completed_at = Column(DateTime)

class UserAnswer(Base):
    __tablename__ = 'user_answers'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    question_index = Column(Integer)
    user_answer = Column(String)
    is_correct = Column(Integer)
    answered_at = Column(DateTime)