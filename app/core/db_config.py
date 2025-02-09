"""
This module defines the SQLAlchemy database engine configuration and
provides a factory for creating asynchronous sessions.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


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
