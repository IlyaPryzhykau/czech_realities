"""
This module defines the CRUD API endpoints for managing Question resources.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_config import get_async_session
from app.core.user import current_superuser
from app.crud.question import question_crud
from app.crud.topic import topic_crud
from app.api.endpoints.validators import get_object_or_404
from app.schemas.question import (
    QuestionCreate, QuestionResponse, QuestionUpdate,
    QuestionResponseWithTopicAndAnswers)
from app.api.endpoints.constants import (
    ERROR_QUESTION_NOT_FOUND, ERROR_TOPIC_NOT_FOUND)


router = APIRouter()


@router.post(
    '/',
    response_model=QuestionResponse,
    dependencies=[Depends(current_superuser)]
)
async def create_question(
        question: QuestionCreate,
        session: AsyncSession = Depends(get_async_session)
) -> QuestionResponse:
    """
    Create a new Question.

    Validates the existence of a Topic before creation.

    Args:
        question (QuestionCreate): The question data to create.
        session (AsyncSession): The async DB session.

    Returns:
        QuestionResponse: The newly created question.
    """
    await get_object_or_404(
        question.topic_id,
        topic_crud,
        session,
        ERROR_TOPIC_NOT_FOUND
    )

    return await question_crud.create(question, session)


@router.get(
    '/',
    response_model=list[QuestionResponse]
)
async def get_all_questions(
        session: AsyncSession = Depends(get_async_session)
) -> list[QuestionResponse]:
    """
    Retrieve all questions from the database.

    Args:
        session (AsyncSession): The async DB session.

    Returns:
        list[QuestionResponse]: A list of questions.
    """
    return await question_crud.get_multi(session)


@router.get(
    '/random-one',
    response_model=QuestionResponseWithTopicAndAnswers
)
async def get_random_question(
        session: AsyncSession = Depends(get_async_session)
) -> QuestionResponseWithTopicAndAnswers | None:
    """
    Retrieve a single random question from all available questions.

    Args:
        session (AsyncSession): The async DB session.

    Returns:
        QuestionResponseWithTopicAndAnswers | None: The random question
        if any exist, otherwise None.
    """
    return await question_crud.get_random_question(session)


@router.get(
    '/by-topic/{topic_id}',
    response_model=list[QuestionResponseWithTopicAndAnswers]
)
async def get_questions_by_topic(
        topic_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> list[QuestionResponseWithTopicAndAnswers]:
    """
    Retrieve all questions belonging to a specific topic.

    Args:
        topic_id (int): The ID of the topic.
        session (AsyncSession): The async DB session.

    Returns:
        list[QuestionResponseWithTopicAndAnswers]: A list of questions
        for the given topic.
    """
    await get_object_or_404(
        topic_id,
        topic_crud,
        session,
        ERROR_TOPIC_NOT_FOUND
    )
    return await question_crud.get_all_questions_by_topic(topic_id, session)


@router.get(
    '/random-ticket',
    response_model=list[QuestionResponseWithTopicAndAnswers]
)
async def get_random_question(
        session: AsyncSession = Depends(get_async_session)
) -> list[QuestionResponseWithTopicAndAnswers]:
    """
    Retrieve a 'ticket' containing one random question for each topic.

    Args:
        session (AsyncSession): The async DB session.

    Returns:
        list[QuestionResponseWithTopicAndAnswers]: A list of random questions
        (one per topic).
    """
    return await question_crud.get_random_ticket(session)


@router.get(
    '/{question_id}',
    response_model=QuestionResponseWithTopicAndAnswers
)
async def get_question_by_id(
        question_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> QuestionResponseWithTopicAndAnswers:
    """
    Retrieve a single question by its ID, including its topic and answers.

    Args:
        question_id (int): The ID of the question.
        session (AsyncSession): The async DB session.

    Returns:
        QuestionResponseWithTopicAndAnswers: The question with related topic
        and answers.

    Raises:
        HTTPException(404): If the question does not exist.
    """
    await get_object_or_404(
        question_id,
        question_crud,
        session,
        ERROR_QUESTION_NOT_FOUND
    )

    return await question_crud.get_question_with_answers(question_id, session)


@router.patch(
    '/{question_id}',
    response_model=QuestionResponse,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_question(
        question_id: int,
        obj_in: QuestionUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> QuestionResponse:
    """
    Partially update an existing Question.

    Validates Topic existence if the topic_id is changed.

    Args:
        question_id (int): The ID of the question.
        obj_in (QuestionUpdate): Fields to update.
        session (AsyncSession): The async DB session.

    Returns:
        QuestionResponse: The updated question.
    """
    question = await get_object_or_404(
        question_id,
        question_crud,
        session,
        ERROR_QUESTION_NOT_FOUND
    )
    if obj_in.topic_id and obj_in.topic_id != question.topic_id:
        await get_object_or_404(
            question.topic_id,
            topic_crud,
            session,
            ERROR_TOPIC_NOT_FOUND
        )

    return await question_crud.update(question, obj_in, session)


@router.delete(
    '/{question_id}',
    response_model=QuestionResponse,
    dependencies=[Depends(current_superuser)]
)
async def delete_question(
        question_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> QuestionResponse:
    """
    Delete an existing Question.

    Args:
        question_id (int): The ID of the question to delete.
        session (AsyncSession): The async DB session.

    Returns:
        QuestionResponse: The deleted question.

    Raises:
        HTTPException(404): If the question does not exist.
    """
    question = await get_object_or_404(
        question_id,
        question_crud,
        session,
        ERROR_QUESTION_NOT_FOUND
    )
    await question_crud.remove(question, session)
    return question
