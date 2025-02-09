"""
DatabasePipeline module: defines an asynchronous pipeline to save
scraped items into a database (categories, topics, questions, answers)
in a strictly sequential order via an asyncio.Lock.
"""

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from .db_config import get_async_session
from db_models import Category, Topic, Question, Answer
from parser.items import AnswerItem, CategoryItem, QuestionItem, TopicItem


class DatabasePipeline:
    """
    A Scrapy pipeline that saves CategoryItem, TopicItem, QuestionItem,
    and AnswerItem into a database using SQLAlchemy AsyncSession.

    This pipeline uses an asyncio.Lock to ensure that items are saved
    strictly one at a time, preventing race conditions.
    """

    def __init__(self):
        # Блокировка, чтобы гарантировать последовательную запись
        self.db_lock = asyncio.Lock()

    @classmethod
    def from_crawler(cls, crawler):
        """
        Class method called by Scrapy to create the pipeline.

        Args:
            crawler (scrapy.crawler.Crawler): The crawler instance.

        Returns:
            DatabasePipeline: The instantiated pipeline object.
        """
        return cls()

    async def process_item(self, item, spider):
        """
        Main entry point for processing each item. Ensures
        that only one item is processed at a time via db_lock.

        Args:
            item (scrapy.Item): The item to be processed.
            spider (scrapy.Spider): The spider that scraped the item.

        Returns:
            scrapy.Item: The same item, unchanged.
        """
        async with self.db_lock:  # блокируем, пока обрабатываем текущий item
            async with get_async_session() as session:
                try:
                    if isinstance(item, CategoryItem):
                        await self.save_category(session, item, spider)
                    elif isinstance(item, TopicItem):
                        await self.save_topic(session, item, spider)
                    elif isinstance(item, QuestionItem):
                        await self.save_question(session, item, spider)
                    elif isinstance(item, AnswerItem):
                        await self.save_answer(session, item, spider)
                except SQLAlchemyError as e:
                    spider.logger.error(f"Database error: {e}")
                    await session.rollback()
                except Exception as e:
                    spider.logger.error(f"Unexpected error: {e}")
                    await session.rollback()

        return item

    async def save_category(self, session: AsyncSession, item: CategoryItem, spider):
        """
        Save a category to the database if it doesn't already exist.
        """
        spider.logger.debug(f"Saving category: {item['name']}")
        result = await session.execute(
            select(Category).where(Category.name == item['name'])
        )
        category_obj = result.scalar()

        if not category_obj:
            new_category = Category(name=item['name'])
            session.add(new_category)
            await session.commit()
            spider.logger.info(f"Category created: {item['name']}")

    async def save_topic(self, session: AsyncSession, item: TopicItem, spider):
        """
        Save a topic to the database if it doesn't already exist.
        Links the topic to a category by name.
        """
        spider.logger.debug(f"Saving topic: {item['name']} (category={item['category_name']})")

        # Сначала ищем категорию
        result_cat = await session.execute(
            select(Category).where(Category.name == item['category_name'])
        )
        category_obj = result_cat.scalar()
        if not category_obj:
            raise ValueError(f"Category '{item['category_name']}' not found in DB")

        # Проверяем, есть ли уже такой топик
        result_topic = await session.execute(
            select(Topic).where(
                Topic.name == item['name'],
                Topic.category_id == category_obj.id
            )
        )
        topic_obj = result_topic.scalar()

        if not topic_obj:
            new_topic = Topic(
                name=item['name'],
                category_id=category_obj.id
            )
            session.add(new_topic)
            await session.commit()
            spider.logger.info(f"Topic created: {item['name']}")

    async def save_question(self, session: AsyncSession, item: QuestionItem, spider):
        """
        Save a question to the database if it doesn't already exist.
        Links the question to a topic by topic_name.
        """
        question_text = item['text'].strip()
        image_url = item.get('image_url')
        update_date = item.get('update_date')

        spider.logger.debug(f"Saving question: {question_text[:50]}... (topic={item['topic_name']})")

        # Ищем топик
        result_topic = await session.execute(
            select(Topic).where(Topic.name == item['topic_name'].strip())
        )
        topic_obj = result_topic.scalar()

        if not topic_obj:
            raise ValueError(f"Topic '{item['topic_name']}' not found in DB")

        # Проверяем, есть ли уже такой вопрос
        result_q = await session.execute(
            select(Question).where(
                Question.text == question_text,
                Question.topic_id == topic_obj.id
            )
        )
        question_obj = result_q.scalar()

        if not question_obj:
            spider.logger.debug(
                f"Creating new question: {question_text[:50]}... (topic={topic_obj.name})"
            )
            question_obj = Question(
                text=question_text,
                image_url=image_url,
                update_date=update_date,
                topic_id=topic_obj.id
            )
            session.add(question_obj)
            await session.commit()
            spider.logger.info(f"Question created: {question_text[:50]}...")

    async def save_answer(self, session: AsyncSession, item: AnswerItem, spider):
        """
        Save an answer to the database if it doesn't already exist.
        Links the answer to a question by question_text.
        """
        answer_text = item['text'].strip()
        image_url = item.get('image_url')
        is_correct = item.get('is_correct')

        spider.logger.debug(f"Saving answer: {answer_text[:50]}... (question='{item['question_text'][:50]}...')")

        # Ищем вопрос
        result_q = await session.execute(
            select(Question).where(
                Question.text == item['question_text'].strip()
            )
        )
        question_obj = result_q.scalar()
        if not question_obj:
            raise ValueError(f"Question '{item['question_text']}' not found in DB")

        # Проверяем, есть ли уже такой ответ
        result_a = await session.execute(
            select(Answer).where(
                Answer.text == answer_text,
                Answer.question_id == question_obj.id
            )
        )
        answer_obj = result_a.scalar()

        if not answer_obj:
            spider.logger.debug(f"Creating new answer: {answer_text[:50]}...")
            new_answer = Answer(
                text=answer_text,
                image_url=image_url,
                is_correct=is_correct,
                question_id=question_obj.id
            )
            session.add(new_answer)
            await session.commit()
            spider.logger.info(f"Answer created: {answer_text[:50]}...")
