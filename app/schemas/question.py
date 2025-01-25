"""
This module contains Pydantic schemas for handling Question data,
including validation and formatting for date fields.
"""

from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator, field_serializer

from .answer import AnswerResponse
from .topic import TopicResponse


MAX_NAME_LENGTH = 300
DATE_FORMAT = '%d.%m.%Y'
TIME_EXAMPLE = '12.12.2021'


class QuestionBase(BaseModel):
    """
    Base schema for Question with shared fields and custom date validation.

    Attributes:
        text (str): The question text with a maximum length constraint.
        image_url (str | None): Optional URL for an attached image.
        update_date (date): The date when the question was last updated.
    """

    text: str = Field(..., max_length=MAX_NAME_LENGTH)
    image_url: str | None = None
    update_date: date = Field(..., example=TIME_EXAMPLE)

    @field_validator('update_date', mode='before')
    def parse_update_date(cls, value):
        """
        Convert a string date into a date object if needed,
        ensuring it follows DATE_FORMAT (%d.%m.%Y).
        """
        if isinstance(value, str):
            try:
                return datetime.strptime(value, DATE_FORMAT).date()
            except ValueError:
                raise ValueError(
                    'Update date must be in format "day.month.year"'
                    '(e.g., "18.01.2025").'
                )
        if not isinstance(value, date):
            raise ValueError('Update date must be a valid date.')
        return value

    @field_validator('update_date', mode='after')
    def validate_update_date(cls, value):
        """
        Ensure the update_date is not in the future.
        """
        if value > datetime.now().date():
            raise ValueError('Update date cannot be in the future.')
        return value

    @field_serializer('update_date', when_used='json')
    def format_update_date(self, value: date) -> str:
        """
        Serialize the update_date field as a string in
        the specified DATE_FORMAT.
        """
        return value.strftime(DATE_FORMAT)


class QuestionCreate(QuestionBase):
    """
    Schema for creating a new Question.
    Includes the topic_id field.
    """
    topic_id: int


class QuestionUpdate(QuestionBase):
    """
    Schema for updating an existing Question.

    Attributes:
        text (str | None): Optional text override.
        topic_id (int | None): Optional topic override.
        update_date (date | None): Optional date override.
    """
    text: str | None = Field(None, max_length=MAX_NAME_LENGTH)
    topic_id: int | None
    update_date: date = Field(None, example=TIME_EXAMPLE)


class QuestionResponse(QuestionBase):
    """
    Response schema for a Question entity.

    Attributes:
        id (int): The unique identifier of the Question.
        text (str): Question text.
        image_url (str | None): Optional URL for an image.
        update_date (date): Last update date.
        topic_id (int): ID of the associated topic.
    """

    id: int
    text: str
    image_url: str | None
    update_date: date
    topic_id: int

    class Config:
        from_attributes = True


class QuestionResponseWithTopicAndAnswers(QuestionBase):
    """
    Extended response schema for a Question entity,
    including related Topic and Answers.

    Attributes:
        id (int): The unique identifier of the Question.
        text (str): Question text.
        image_url (str | None): Optional URL for an image.
        topic (TopicResponse): Detailed information about the associated topic.
        answers (list[AnswerResponse]): A list of related answers.
        update_date (date): Last update date.
    """

    id: int
    text: str
    image_url: str | None
    topic: TopicResponse
    answers: list[AnswerResponse]
    update_date: date

    class Config:
        from_attributes = True
