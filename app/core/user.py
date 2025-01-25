"""
This module integrates FastAPI Users with SQLAlchemy, providing user database
and management functionalities (user creation, authentication, etc.).
"""

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Provide a SQLAlchemy user database instance for FastAPI Users.

    Args:
        session (AsyncSession): The async database session.

    Yields:
        SQLAlchemyUserDatabase: A FastAPI Users DB adapter for user operations.
    """
    yield SQLAlchemyUserDatabase(session, User)


#: A bearer token transport specifying the token URL for JWT authentication.
bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """
    Create a JWT strategy for authentication using the configured secret key.

    Returns:
        JWTStrategy: A JWT-based auth strategy with a 3600-second lifetime.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


#: An authentication backend using JWT tokens.
auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    A user manager extending FastAPI Users' BaseUserManager for integer-based IDs.

    Methods:
        validate_password: Perform custom password checks
            (length, no email in password).
        on_after_register: Action to perform after user registration.
    """

    async def validate_password(
        self,
        password: str,
        user: UserCreate | User,
    ) -> None:
        """
        Validate the given password for certain constraints.

        Args:
            password (str): The password to validate.
            user (UserCreate | User): The user object or creation schema.

        Raises:
            InvalidPasswordException: If the password fails the checks (length,
            contains email, etc.).
        """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
            self, user: User, request: Request | None = None
    ):
        """
        Hook method called after a user is successfully registered.

        Args:
            user (User): The newly registered user.
            request (Request | None): Optional FastAPI request object.
        """
        print(f'User {user.email} has been registered.')


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Provide an instance of UserManager for handling user logic.

    Args:
        user_db (SQLAlchemyUserDatabase): The user database adapter.

    Yields:
        UserManager: A user manager instance.
    """
    yield UserManager(user_db)


#: FastAPI Users object configured with our custom user manager and backend.
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

#: Dependency that provides the currently active user (non-superuser).
current_user = fastapi_users.current_user(active=True)

#: Dependency that provides the currently active user but
# requires superuser privileges.
current_superuser = fastapi_users.current_user(active=True, superuser=True)
