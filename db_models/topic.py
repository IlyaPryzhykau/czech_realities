"""
This module defines the Topic model, which represents a specific topic
within a category. Each topic can have multiple questions.
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db_models.base import Base


MAX_NAME_LENGTH = 100


class Topic(Base):
    """
    Represents a topic entity.

    Attributes:
        name (str): The name of the topic, must be unique.
        category_id (int): A foreign key referencing the associated Category.
        category (Category): A SQLAlchemy relationship to the Category model.
        questions (list[Question]): A list of questions associated with
            this topic.
    """

    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='topics')
    questions = relationship(
        'Question', back_populates='topic', cascade='delete')

    def __str__(self):
        """
        Return the topic's name.
        """
        return self.name
