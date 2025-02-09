"""
This module defines a generic CRUD base class (CRUDBase) for SQLAlchemy models.
It provides common operations (Create, Read, Update, Delete).
"""

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import User


class CRUDBase:
    """
    A base class for generic CRUD operations on a given SQLAlchemy model.
    """

    def __init__(self, model):
        """
        Initialize the CRUD base with a specific model.

        Args:
            model: The SQLAlchemy model class.
        """
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """
        Retrieve a single object by its ID.

        Args:
            obj_id (int): The primary key of the object.
            session (AsyncSession): The current database session.

        Returns:
            The model instance if found, otherwise None.
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """
        Retrieve all objects of this model.

        Args:
            session (AsyncSession): The current database session.

        Returns:
            A list of all model instances.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: User | None = None
    ):
        """
        Create a new object in the database.

        Args:
            obj_in: A Pydantic model or dictionary containing creation data.
            session (AsyncSession): The current database session.
            user (User | None): Optionally associate this object
                with a user (if applicable).

        Returns:
            The newly created model instance.
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        """
        Update an existing object in the database.

        Args:
            db_obj: The current database model instance.
            obj_in: A Pydantic model or dictionary with updated data (exclude_unset fields).
            session (AsyncSession): The current database session.

        Returns:
            The updated model instance.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """
        Remove (delete) an object from the database.

        Args:
            db_obj: The model instance to delete.
            session (AsyncSession): The current database session.

        Returns:
            The deleted model instance.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj
