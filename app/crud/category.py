from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Category


class CategoryCRUD(CRUDBase):

    async def get_category_id_by_name(
            self,
            name: str,
            session: AsyncSession
    ) -> int | None:
        category_id = await session.execute(
            select(Category.id).where(Category.name == name)
        )
        return category_id.scalars().first()


category_crud = CategoryCRUD(Category)
