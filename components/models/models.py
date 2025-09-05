from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QUIZ_STATE(Base):
    __tablename__ = 'quiz_state'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    question_index = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Quiz_state(id={self.id})>"