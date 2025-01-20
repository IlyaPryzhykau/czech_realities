from random import randrange

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.crud.base import CRUDBase
from app.models import Question, Topic


class QuestionCRUD(CRUDBase):

    async def get_question_with_answers(
        self,
        question_id: int,
        session: AsyncSession
    ) -> Question | None:
        """
        Retrieve a Question by its ID, including related Answers and Topic.
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
            .limit(1)
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
            .limit(1)
        )
        random_question_id = result.scalar_one_or_none()
        return await self.get_question_with_answers(random_question_id, session)

    async def get_random_ticket(
        self,
        session: AsyncSession
    ) -> list[Question]:
        """
        Create a "ticket" by retrieving one random question for each Topic.
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
