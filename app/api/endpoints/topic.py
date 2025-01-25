"""
This module defines the CRUD API endpoints for managing Topic resources.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.topic import topic_crud
from app.crud.category import category_crud
from app.api.endpoints.validators import (
    validate_name_duplicate, get_object_or_404)
from app.schemas.topic import (
    TopicCreate, TopicUpdate, TopicResponse, TopicResponseWithCategoryName)
from app.api.endpoints.constants import (
    ERROR_CATEGORY_NOT_FOUND, ERROR_TOPIC_NOT_FOUND)


router = APIRouter()


@router.post(
    '/',
    response_model=TopicResponseWithCategoryName,
    dependencies=[Depends(current_superuser)]
)
async def create_topic(
        topic: TopicCreate,
        session: AsyncSession = Depends(get_async_session)
) -> TopicResponseWithCategoryName:
    """
    Create a new Topic.

    Validates category existence and name duplication before creation.

    Args:
        topic (TopicCreate): The topic data to create.
        session (AsyncSession): The async DB session.

    Returns:
        TopicResponseWithCategoryName: The newly created topic with
        category details.
    """
    await get_object_or_404(
        topic.category_id,
        category_crud,
        session,
        ERROR_CATEGORY_NOT_FOUND
    )
    await validate_name_duplicate(
        topic.name, session, topic_crud.get_topic_id_by_name)

    topic_db = await topic_crud.create(topic, session)
    topic_with_category = await topic_crud.get_with_category(
        topic_db.id, session)

    return topic_with_category


@router.get(
    '/',
    response_model=list[TopicResponse]
)
async def get_all_topics(
        session: AsyncSession = Depends(get_async_session)
) -> list[TopicResponse]:
    """
    Retrieve all topics from the database.

    Args:
        session (AsyncSession): The async DB session.

    Returns:
        list[TopicResponse]: A list of all topics.
    """
    return await topic_crud.get_multi(session)


@router.patch(
    '/{topic_id}',
    response_model=TopicResponse,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_topic(
        topic_id: int,
        obj_in: TopicUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> TopicResponse:
    """
    Partially update an existing Topic.

    Validates name duplication and category existence if changed.

    Args:
        topic_id (int): The ID of the topic.
        obj_in (TopicUpdate): Fields to update.
        session (AsyncSession): The async DB session.

    Returns:
        TopicResponse: The updated topic.
    """
    topic = await get_object_or_404(topic_id, topic_crud, session)

    if obj_in.name and obj_in.name != topic.name:
        await validate_name_duplicate(
            obj_in.name, session, topic_crud.get_topic_id_by_name)

    if obj_in.category_id and obj_in.category_id != topic.category_id:
        await get_object_or_404(
            obj_in.category_id,
            category_crud,
            session,
            ERROR_CATEGORY_NOT_FOUND
        )

    return await topic_crud.update(topic, obj_in, session)


@router.delete(
    '/{topic_id}',
    response_model=TopicResponse,
    dependencies=[Depends(current_superuser)]
)
async def delete_topic(
        topic_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> TopicResponse:
    """
    Delete an existing Topic.

    Args:
        topic_id (int): The ID of the topic.
        session (AsyncSession): The async DB session.

    Returns:
        TopicResponse: The deleted topic.

    Raises:
        HTTPException(404): If the topic does not exist.
    """
    topic = await get_object_or_404(
        topic_id,
        topic_crud,
        session,
        ERROR_TOPIC_NOT_FOUND
    )
    await topic_crud.remove(topic, session)
    return topic
