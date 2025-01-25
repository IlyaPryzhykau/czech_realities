"""
This module handles database initialization tasks, such as creating
a first superuser if none exists.
"""

import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate


#: An async context manager that provides an AsyncSession.
get_async_session_context = contextlib.asynccontextmanager(get_async_session)

#: An async context manager that provides a FastAPI Users DB adapter.
get_user_db_context = contextlib.asynccontextmanager(get_user_db)

#: An async context manager that provides a FastAPI Users Manager instance.
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False):
    """
        Create a new user account, optionally as a superuser.

        Args:
            email (str): The email address for the user.
            password (str): The user's password.
            is_superuser (bool): If True, the user is granted superuser rights.
        """
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser
                        )
                    )
    except UserAlreadyExists:
        # If the user already exists, do nothing.
        pass


async def create_first_superuser():
    """
    Create the first superuser if the relevant environment variables
    for email and password are set and a superuser doesn't already exist.
    """
    if (settings.first_superuser_email is not None
            and settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
