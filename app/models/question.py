from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


MAX_NAME_LENGTH = 300


class Question(Base):
    text = Column(String(MAX_NAME_LENGTH), nullable=False)
    image_url = Column(String, nullable=True)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    update_date = Column(DateTime)
    topic = relationship('Topic', back_populates='questions')
    answers = relationship(
        'Answer', back_populates='question', cascade='delete')
