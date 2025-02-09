"""
This module defines the SQLAlchemy database engine configuration and
provides a factory for creating asynchronous sessions.
"""
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

#: An asynchronous SQLAlchemy engine configured for the parser.
engine = create_async_engine(DATABASE_URL, echo=False)

#: A session factory for creating AsyncSession instances in the parser.
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def get_async_session():
    """
    Provide a single async database session context for each request.

    Yields:
        AsyncSession: An async session to be used within a request scope.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
