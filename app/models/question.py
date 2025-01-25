"""
This module defines the Question model, which represents a question
belonging to a specific topic. A question can have multiple answers
and may include an image URL.
"""

from sqlalchemy import Column,  String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.core.db import Base


MAX_NAME_LENGTH = 300
TEXT_PREVIEW_LIMIT = 30


class Question(Base):
    """
    Represents a question entity.

    Attributes:
        text (str): The text content of the question.
        image_url (str | None): An optional URL to an image for this question.
        topic_id (int): A foreign key referencing the associated Topic.
        update_date (date): The date the question was last updated.
        topic (Topic): A SQLAlchemy relationship to the Topic model.
        answers (list[Answer]): A list of answers for this question.
    """

    text = Column(String(MAX_NAME_LENGTH), nullable=False)
    image_url = Column(String, nullable=True)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    update_date = Column(Date, nullable=False)
    topic = relationship('Topic', back_populates='questions')
    answers = relationship(
        'Answer', back_populates='question', cascade='delete')

    def __str__(self):
        """
        Return a shortened version of the question text
        (limited by TEXT_PREVIEW_LIMIT).
        """
        return self.text if len(self.text) < TEXT_PREVIEW_LIMIT \
            else self.text[:TEXT_PREVIEW_LIMIT] + "..."
