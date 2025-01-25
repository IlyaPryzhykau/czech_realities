"""
This module defines the Category model, which groups topics
together under a specific category name.
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.db import Base


MAX_NAME_LENGTH = 100


class Category(Base):
    """
    Represents a category entity.

    Attributes:
        name (str): The name of the category, must be unique.
        topics (list[Topic]): A list of topics that belong to this category.
    """

    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    topics = relationship(
        'Topic', back_populates='category', cascade='delete')

    def __str__(self):
        """
        Return the category's name.
        """
        return self.name
