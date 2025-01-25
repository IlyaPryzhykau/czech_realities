"""
This module provides CRUD operations for the Topic model, including
methods to retrieve topic IDs by name or fetch a topic with its category.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Topic


class TopicCRUD(CRUDBase):
    """
    Specialized CRUD for the Topic model.

    Methods:
        get_topic_id_by_name: Retrieve a topic's ID by its name.
        get_with_category: Retrieve a topic with its related category.
    """

    async def get_topic_id_by_name(
            self,
            name: str,
            session: AsyncSession
    ) -> int | None:
        """
        Get the ID of a Topic by its name.

        Args:
            name (str): The name of the topic.
            session (AsyncSession): The current database session.

        Returns:
            int | None: The ID of the topic if found, otherwise None.
        """
        topic_id = await session.execute(
            select(Topic.id).where(Topic.name == name)
        )
        return topic_id.scalars().first()

    async def get_with_category(
            self,
            topic_id: int,
            session: AsyncSession
    ) -> Topic | None:
        """
        Retrieve a Topic by its ID along with its related Category.

        Args:
            topic_id (int): The ID of the topic.
            session (AsyncSession): The current database session.

        Returns:
            Topic | None: The Topic object with its category if found,
            otherwise None.
        """
        topic = await session.execute(
            select(Topic)
            .options(joinedload(Topic.category))
            .filter(Topic.id == topic_id)
        )
        return topic.scalars().first()


topic_crud = TopicCRUD(Topic)
