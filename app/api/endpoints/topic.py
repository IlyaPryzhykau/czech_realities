from fastapi import APIRouter, Depends
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.topic import topic_crud
from app.crud.category import category_crud
from app.api.endpoints.validators import (
    validate_name_duplicate, get_object_or_404)
from app.models import Topic
from app.schemas.topic import (
    TopicCreate, TopicUpdate, TopicResponse, TopicResponseWithCategoryName)


router = APIRouter()


@router.post(
    '/',
    response_model=TopicResponseWithCategoryName,
    dependencies=[Depends(current_superuser)]
)
async def create_topic(
        topic: TopicCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await get_object_or_404(topic.category_id, category_crud, session)
    await validate_name_duplicate(
        topic.name, session, topic_crud.get_topic_id_by_name)

    topic = await topic_crud.create(obj_in=topic, session=session)
    topic_with_category = await topic_crud.get_with_category(topic.id, session)

    return topic_with_category


@router.get(
    '/',
    response_model=list[TopicResponse]
)
async def get_all_topics(
        session: AsyncSession = Depends(get_async_session)
):
    return await topic_crud.get_multi(session=session)


@router.patch(
    '/{topic_id}',
    response_model=TopicResponse,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_topic(
        topic_id: int,
        obj_in: TopicUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    topic = await get_object_or_404(topic_id, topic_crud, session)

    if obj_in.name and obj_in.name != topic.name:
        await validate_name_duplicate(
            obj_in.name, session, topic_crud.get_topic_id_by_name)

    return await topic_crud.update(topic, obj_in, session)


@router.delete(
    '/{topic_id}',
    response_model=TopicResponse,
    dependencies=[Depends(current_superuser)]
)
async def delete_topic(
        topic_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    topic = await get_object_or_404(topic_id, topic_crud, session)
    await topic_crud.remove(topic, session)
    return topic
