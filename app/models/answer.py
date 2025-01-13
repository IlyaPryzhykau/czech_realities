from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


MAX_NAME_LENGTH = 200


class Answer(Base):
    text = Column(String(MAX_NAME_LENGTH), nullable=False)
    image_url = Column(String, nullable=True)
    is_correct = Column(Boolean, nullable=False, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question', back_populates='answers')
