"""
This module defines the SQLAlchemy database configuration, including
the base declarative class and an asynchronous session factory.
"""

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from inflection import pluralize

from app.core.config import settings


class PreBase:
    """
    A mixin class that provides a custom table naming convention and
    a primary key field 'id'.

    The table name is generated by pluralizing the lowercase class name.
    """

    @declared_attr
    def __tablename__(cls):
        return pluralize(cls.__name__.lower())

    id = Column(Integer, primary_key=True)


#: The declarative base class extended by PreBase.
Base = declarative_base(cls=PreBase)

#: An asynchronous SQLAlchemy engine for the app's database.
engine = create_async_engine(settings.database_url)

#: A session factory using AsyncSession for database interactions.
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """
    Provide a single async database session context for each request.

    Yields:
        AsyncSession: An async session to be used within a request scope.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
