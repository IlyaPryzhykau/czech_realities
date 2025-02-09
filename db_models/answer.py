"""
This module defines the Answer model, which represents an individual answer
for a given question. Each answer can optionally be linked to an image
and flagged as correct or incorrect.
"""

from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db_models.base import Base


MAX_NAME_LENGTH = 200


class Answer(Base):
    """
    Represents an answer entity.

    Attributes:
        text (str): The text content of the answer.
        image_url (str | None): An optional URL to an image for this answer.
        is_correct (bool): Indicates if the answer is correct.
        question_id (int): A foreign key referencing the associated Question.
        question (Question): A SQLAlchemy relationship to the Question model.
    """

    text = Column(String(MAX_NAME_LENGTH), nullable=False)
    image_url = Column(String, nullable=True)
    is_correct = Column(Boolean, nullable=False, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question', back_populates='answers')

    def __str__(self):
        """
        Return the answer's text representation.
        """
        return self.text
