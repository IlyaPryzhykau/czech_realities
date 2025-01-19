from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import Question


class QuestionCRUD(CRUDBase):
    async def get_question_with_answers(
            self,
            question_id: int,
            session: AsyncSession
    ) -> Question:
        question = await session.execute(
            select(
                Question
            ).options(
                joinedload(Question.answers),
                joinedload(Question.topic)
            ).filter(
                Question.id == question_id
            )
        )
        return question.scalars().first()


question_crud = QuestionCRUD(Question)
