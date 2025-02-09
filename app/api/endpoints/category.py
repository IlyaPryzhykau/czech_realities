"""
This module defines the CRUD API endpoints for managing Category resources.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_config import get_async_session
from app.core.user import current_superuser
from app.crud.category import category_crud
from app.api.endpoints.validators import (
    validate_name_duplicate, get_object_or_404)
from app.schemas.category import (
    CategoryCreate, CategoryUpdate, CategoryResponse)
from app.api.endpoints.constants import ERROR_CATEGORY_NOT_FOUND


router = APIRouter()


@router.post(
    '/',
    response_model=CategoryResponse,
    dependencies=[Depends(current_superuser)]
)
async def create_category(
        category: CategoryCreate,
        session: AsyncSession = Depends(get_async_session)
) -> CategoryResponse:
    """
    Create a new Category.

    Validates that the category name is not duplicated.

    Args:
        category (CategoryCreate): The category data to create.
        session (AsyncSession): The async DB session.

    Returns:
        CategoryResponse: The newly created category.
    """
    await validate_name_duplicate(
        category.name, session, category_crud.get_category_id_by_name)
    return await category_crud.create(category, session)


@router.get(
    '/',
    response_model=list[CategoryResponse]
)
async def get_all_category(
        session: AsyncSession = Depends(get_async_session)
) -> list[CategoryResponse]:
    """
    Retrieve all categories from the database.

    Args:
        session (AsyncSession): The async DB session.

    Returns:
        list[CategoryResponse]: A list of all categories.
    """
    return await category_crud.get_multi(session)


@router.patch(
    '/{category_id}',
    response_model=CategoryResponse,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_category(
        category_id: int,
        obj_in: CategoryUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> CategoryResponse:
    """
    Partially update an existing Category.

    Args:
        category_id (int): The ID of the category to update.
        obj_in (CategoryUpdate): Fields to update.
        session (AsyncSession): The async DB session.

    Returns:
        CategoryResponse: The updated category.
    """
    category = await get_object_or_404(
        category_id,
        category_crud,
        session,
        ERROR_CATEGORY_NOT_FOUND
    )
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
) -> CategoryResponse:
    """
    Delete an existing Category.

    Args:
        category_id (int): The ID of the category.
        session (AsyncSession): The async DB session.

    Returns:
        CategoryResponse: The deleted category.

    Raises:
        HTTPException(404): If the category with the given ID does not exist.
    """
    category = await get_object_or_404(
        category_id,
        category_crud,
        session,
        ERROR_CATEGORY_NOT_FOUND
    )
    await category_crud.remove(category, session)
    return category
