"""
This module defines the CRUD API endpoints for managing Answer resources.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.answer import answer_crud
from app.crud.question import question_crud
from app.api.endpoints.validators import get_object_or_404
from app.schemas.answer import AnswerCreate, AnswerResponse, AnswerUpdate
from app.api.endpoints.constants import ERROR_ANSWER_NOT_FOUND, ERROR_QUESTION_NOT_FOUND


router = APIRouter()


@router.post(
    '/',
    response_model=AnswerResponse,
    dependencies=[Depends(current_superuser)]
)
async def create_question(
        answer: AnswerCreate,
        session: AsyncSession = Depends(get_async_session)
) -> AnswerResponse:
    """
    Create a new Answer.

    Checks if the specified Question exists before creation.

    Args:
        answer (AnswerCreate): The answer data to create.
        session (AsyncSession): The async DB session.

    Returns:
        AnswerResponse: The newly created answer.
    """
    await get_object_or_404(
        answer.question_id,
        question_crud,
        session,
        ERROR_QUESTION_NOT_FOUND
    )

    return await answer_crud.create(answer, session)


@router.get(
    '/',
    response_model=list[AnswerResponse]
)
async def get_all_answers(
        session: AsyncSession = Depends(get_async_session)
) -> list[AnswerResponse]:
    """
    Retrieve all answers from the database.

    Args:
        session (AsyncSession): The async DB session.

    Returns:
        list[AnswerResponse]: A list of all answers.
    """
    return await answer_crud.get_multi(session)


@router.get(
    '/{answer_id}',
    response_model=AnswerResponse
)
async def get_answer_by_id(
        answer_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> AnswerResponse:
    """
    Retrieve a single Answer by its ID.

    Args:
        answer_id (int): The ID of the answer.
        session (AsyncSession): The async DB session.

    Returns:
        AnswerResponse: The answer if found.

    Raises:
        HTTPException(404): If the answer with the given ID does not exist.
    """
    return await get_object_or_404(
        answer_id,
        answer_crud,
        session,
        ERROR_ANSWER_NOT_FOUND
    )


@router.patch(
    '/{answer_id}',
    response_model=AnswerResponse,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_answer(
        answer_id: int,
        obj_in: AnswerUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> AnswerResponse:
    """
    Partially update an existing Answer.

    Validates question existence if question_id is changed.

    Args:
        answer_id (int): The ID of the answer to update.
        obj_in (AnswerUpdate): Fields to update.
        session (AsyncSession): The async DB session.

    Returns:
        AnswerResponse: The updated answer.
    """
    answer = await get_object_or_404(
        answer_id,
        answer_crud,
        session,
        ERROR_ANSWER_NOT_FOUND
    )
    if obj_in.question_id and obj_in.question_id != answer.question_id:
        await get_object_or_404(
            obj_in.question_id,
            question_crud,
            session,
            ERROR_QUESTION_NOT_FOUND
        )
    return await answer_crud.update(answer, obj_in, session)


@router.delete(
    '/{answer_id}',
    response_model=AnswerResponse,
    dependencies=[Depends(current_superuser)]
)
async def delete_answer(
        answer_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> AnswerResponse:
    """
    Delete an existing Answer by its ID.

    Args:
        answer_id (int): The ID of the answer.
        session (AsyncSession): The async DB session.

    Returns:
        AnswerResponse: The deleted answer.

    Raises:
        HTTPException(404): If the answer with the given ID does not exist.
    """
    answer = await get_object_or_404(
        answer_id,
        answer_crud,
        session,
        ERROR_ANSWER_NOT_FOUND
    )
    await answer_crud.remove(db_obj=answer, session=session)
    return answer
