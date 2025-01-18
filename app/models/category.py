from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.db import Base


MAX_NAME_LENGTH = 100


class Category(Base):
    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    topics = relationship(
        'Topic', back_populates='category', cascade='delete')
