from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.question import question_crud
from app.api.endpoints.validators import get_object_or_404
from app.schemas.question import (
    QuestionCreate, QuestionResponse, QuestionUpdate)


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
