from typing import Awaitable, Callable, TypeVar, Generic

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.category import category_crud
from app.crud.topic import topic_crud
from app.models import Category


T = TypeVar("T")


async def get_object_or_404(
        object_id: int,
        crud: Generic[T],
        session: AsyncSession,
        not_found_message: str = "Object doesn't exist."
) :
    obj = await crud.get(object_id, session)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=not_found_message
        )
    return obj


async def validate_name_duplicate(
        name: str,
        session: AsyncSession,
        get_id_by_name: Callable[[str, AsyncSession], Awaitable[int | None]]
) -> None:
    entity_id = await get_id_by_name(name, session)
    if entity_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This name already exist.'
        )
