"""
This module provides CRUD operations for the Category model,
including a method to retrieve category IDs by name.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from db_models import Category


class CategoryCRUD(CRUDBase):
    """
    Specialized CRUD for the Category model.

    Methods:
        get_category_id_by_name: Retrieve a category's ID by its name.
    """

    async def get_category_id_by_name(
            self,
            name: str,
            session: AsyncSession
    ) -> int | None:
        """
        Get the ID of a Category by its name.

        Args:
            name (str): The name of the Category.
            session (AsyncSession): The current database session.

        Returns:
            int | None: The ID of the category if found, otherwise None.
        """
        category_id = await session.execute(
            select(Category.id).where(Category.name == name)
        )
        return category_id.scalars().first()


category_crud = CategoryCRUD(Category)
