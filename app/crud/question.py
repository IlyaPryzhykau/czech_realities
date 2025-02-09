"""
This module provides CRUD operations for the Question model, including
methods for retrieving random questions and generating a random 'ticket.'
"""

from random import randrange

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.crud.base import CRUDBase
from db_models import Question, Topic


QUESTION_LIMIT = 1


class QuestionCRUD(CRUDBase):
    """
    Specialized CRUD for the Question model.

    Methods:
        get_question_with_answers: Retrieve a question and its related answers.
        get_random_question: Retrieve a random question from all
            available questions.
        get_random_question_by_topic: Retrieve a random question
            for a specific topic.
        get_all_questions_by_topic: Retrieve all questions for a given topic.
        get_random_ticket: Retrieve a list of random questions (one per topic).
    """

    async def get_question_with_answers(
        self,
        question_id: int,
        session: AsyncSession
    ) -> Question | None:
        """
        Retrieve a Question by its ID, including related Answers and Topic.

        Args:
            question_id (int): The ID of the question to retrieve.
            session (AsyncSession): The current database session.

        Returns:
            Question | None: The Question object with answers and topic
            if found, otherwise None.
        """
        result = await session.execute(
            select(Question)
            .options(
                joinedload(Question.answers),
                joinedload(Question.topic)
            )
            .filter(Question.id == question_id)
        )
        return result.scalars().first()

    async def get_random_question(
        self,
        session: AsyncSession
    ) -> Question | None:
        """
        Retrieve a random Question from all available questions.

        Args:
            session (AsyncSession): The current database session.

        Returns:
            Question | None: A random Question object if any exist,
            otherwise None.
        """
        result = await session.execute(
            select(func.count()).select_from(Question))
        quantity = result.scalar()
        if not quantity:
            return None

        offset_value = randrange(quantity)
        result = await session.execute(
            select(Question.id)
            .offset(offset_value)
            .limit(QUESTION_LIMIT)
        )

        random_question_id = result.scalar_one_or_none()

        return await self.get_question_with_answers(
            random_question_id, session)

    async def get_random_question_by_topic(
        self,
        topic_id: int,
        session: AsyncSession
    ) -> Question | None:
        """
        Retrieve a random Question for the specified Topic.

        Args:
            topic_id (int): The ID of the topic.
            session (AsyncSession): The current database session.

        Returns:
            Question | None: A random Question for the topic if any exist,
            otherwise None.
        """
        result = await session.execute(
            select(func.count()).select_from(Question)
            .filter(Question.topic_id == topic_id)
        )
        quantity = result.scalar()
        if not quantity:
            return None

        offset_value = randrange(quantity)
        result = await session.execute(
            select(Question.id)
            .filter(Question.topic_id == topic_id)
            .offset(offset_value)
            .limit(QUESTION_LIMIT)
        )
        random_question_id = result.scalar_one_or_none()
        return await self.get_question_with_answers(
            random_question_id, session)

    async def get_all_questions_by_topic(
            self,
            topic_id: int,
            session: AsyncSession
    ) -> list[Question]:
        """
        Retrieve all questions for a given topic.

        Args:
            topic_id (int): The ID of the topic.
            session (AsyncSession): The current database session.

        Returns:
            list[Question]: A list of Question objects for the given topic.
        """
        result = await session.execute(
            select(Question).
            options(
                joinedload(Question.answers),
                joinedload(Question.topic)
            )
            .filter(Question.topic_id == topic_id)
        )
        result = result.unique()
        return list(result.scalars().all())

    async def get_random_ticket(
        self,
        session: AsyncSession
    ) -> list[Question]:
        """
        Create a "ticket" by retrieving one random question for each Topic.

        Args:
            session (AsyncSession): The current database session.

        Returns:
            list[Question]: A list of randomly selected Question objects,
            one per topic (if available).
        """
        ticket = []
        topics_result = await session.execute(select(Topic.id))
        topic_ids = topics_result.scalars().all()

        for topic_id in topic_ids:
            random_question = await self.get_random_question_by_topic(
                topic_id, session)
            if random_question:
                ticket.append(random_question)

        return ticket


question_crud = QuestionCRUD(Question)
