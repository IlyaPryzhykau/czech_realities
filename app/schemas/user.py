"""
This module contains Pydantic schemas for handling User data,
integrating with FastAPI Users library.
"""

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    Schema for reading user data (e.g., returning user info).
    Inherits from BaseUser with an integer-based ID.
    """
    pass


class UserCreate(schemas.BaseUserCreate):
    """
    Schema for creating a new user (registration).
    Inherits from BaseUserCreate provided by FastAPI Users.
    """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    Schema for updating existing user data.
    Inherits from BaseUserUpdate provided by FastAPI Users.
    """
    pass
