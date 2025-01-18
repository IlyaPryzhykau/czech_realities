from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.category import category_crud
from app.api.endpoints.validators import (
    validate_name_duplicate, get_object_or_404)
from app.schemas.category import (
    CategoryCreate, CategoryUpdate, CategoryResponse)


router = APIRouter()


@router.post(
    '/',
    response_model=CategoryResponse,
    dependencies=[Depends(current_superuser)]
)
async def create_category(
        category: CategoryCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await validate_name_duplicate(
        category.name, session, category_crud.get_category_id_by_name)
    return await category_crud.create(obj_in=category, session=session)


@router.get(
    '/',
    response_model=list[CategoryResponse]
)
async def get_all_category(
        session: AsyncSession = Depends(get_async_session)
):
    return await category_crud.get_multi(session=session)


@router.patch(
    '/{category_id}',
    response_model=CategoryResponse,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_category(
        category_id: int,
        obj_in: CategoryUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    category = await get_object_or_404(category_id, category_crud, session)
    await validate_name_duplicate(
        obj_in.name, session, category_crud.get_category_id_by_name)
    return await category_crud.update(category, obj_in, session)


@router.delete(
    '/{category_id}',
    response_model=CategoryResponse,
    dependencies=[Depends(current_superuser)]
)
async def delete_category(
        category_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    category = await get_object_or_404(category_id, category_crud, session)
    await category_crud.remove(category, session)
    return category
