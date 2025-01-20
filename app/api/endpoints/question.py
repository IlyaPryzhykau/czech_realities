from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.question import question_crud
from app.api.endpoints.validators import get_object_or_404
from app.schemas.question import (
    QuestionCreate, QuestionResponse, QuestionUpdate, QuestionResponseWithTopicAndAnswers)


router = APIRouter()


@router.post(
    '/',
    response_model=QuestionResponse,
    dependencies=[Depends(current_superuser)]
)
async def create_question(
        question: QuestionCreate,
        session: AsyncSession = Depends(get_async_session)
):

    return await question_crud.create(obj_in=question, session=session)


@router.get(
    '/',
    response_model=list[QuestionResponse]
)
async def get_all_questions(
        session: AsyncSession = Depends(get_async_session)
):
    return await question_crud.get_multi(session=session)


@router.get(
    '/random-one',
    response_model=QuestionResponseWithTopicAndAnswers
)
async def get_random_question(
        session: AsyncSession = Depends(get_async_session)
):
    return await question_crud.get_random_question(session=session)


@router.get(
    '/random-ticket',
    response_model=list[QuestionResponseWithTopicAndAnswers]
)
async def get_random_question(
        session: AsyncSession = Depends(get_async_session)
):
    return await question_crud.get_random_ticket(session=session)


@router.patch(
    '/{question_id}',
    response_model=QuestionResponse,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_question(
        question_id: int,
        obj_in: QuestionUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    question = await get_object_or_404(question_id, question_crud, session)

    return await question_crud.update(question, obj_in, session)


@router.delete(
    '/{question_id}',
    response_model=QuestionResponse,
    dependencies=[Depends(current_superuser)]
)
async def delete_question(
        question_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    question = await get_object_or_404(question_id, question_crud, session)
    await question_crud.remove(question, session)
    return question
