"""
This module defines the User model, integrating FastAPI Users
with SQLAlchemy for persistence.
"""

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from db_models.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Represents a user entity for authentication and user management.

    Inherits from:
        SQLAlchemyBaseUserTable[int]: FastAPI Users' base user class for integer-based IDs.
        Base: The custom base model to integrate with the application's database.
    """

    pass
