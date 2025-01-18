from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


MAX_NAME_LENGTH = 100


class Topic(Base):
    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='topics')
    questions = relationship(
        'Question', back_populates='topic', cascade='delete')
