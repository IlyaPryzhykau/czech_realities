from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Topic


class TopicCRUD(CRUDBase):

    async def get_topic_id_by_name(
            self,
            name: str,
            session: AsyncSession
    ) -> int | None:
        topic_id = await session.execute(
            select(Topic.id).where(Topic.name == name)
        )
        return topic_id.scalars().first()

    async def get_with_category(
            self,
            topic_id: int,
            session: AsyncSession
    ) -> Topic:
        topic = await session.execute(
            select(Topic).options(joinedload(Topic.category)).filter(
                Topic.id == topic_id
            )
        )
        return topic.scalars().first()


topic_crud = TopicCRUD(Topic)
