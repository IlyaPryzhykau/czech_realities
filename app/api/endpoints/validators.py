"""
This module contains helper functions (validators) for API
endpoints, including:
    - get_object_or_404: Fetch an object and raise 404 if not found
    - validate_name_duplicate: Check if a name already exists before
        creating/updating
"""

from typing import Awaitable, Callable, TypeVar, Generic

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.constants import ERROR_OBJECT_NOT_FOUND, ERROR_NAME_ALREADY_EXIST


T = TypeVar('T')


async def get_object_or_404(
        object_id: int,
        crud: Generic[T],
        session: AsyncSession,
        not_found_message: str = ERROR_OBJECT_NOT_FOUND
):
    """
    Retrieve an object by ID using a CRUD instance, or raise 404 if not found.

    Args:
        object_id (int): The ID of the object to retrieve.
        crud (Generic[T]): An instance of the CRUD class to perform
            the get operation.
        session (AsyncSession): The async DB session.
        not_found_message (str): The error message if the object does not exist.

    Returns:
        T: The retrieved object.

    Raises:
        HTTPException(404): If the object does not exist.
    """
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
    """
    Validate that the given name is not already in use.

    Args:
        name (str): The name to check for duplicates.
        session (AsyncSession): The async DB session.
        get_id_by_name (Callable): A function that returns
            an entity ID by name.

    Raises:
        HTTPException(400): If the name already exists.
    """
    entity_id = await get_id_by_name(name, session)
    if entity_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_NAME_ALREADY_EXIST
        )
