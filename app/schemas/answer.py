"""
This module contains Pydantic schemas for handling Answer data.
"""

from pydantic import BaseModel, Field


MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 200


class AnswerBase(BaseModel):
    """
    Base schema for Answer containing shared fields and validation constraints.

    Attributes:
        text (str): The text content of the answer.
        image_url (str | None): An optional image URL.
        is_correct (bool): Indicates whether the answer is correct.
        question_id (int): ID of the associated question.
    """

    text: str = Field(
        ...,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    image_url: str | None
    is_correct: bool = False
    question_id: int


class AnswerCreate(AnswerBase):
    """
    Schema for creating a new Answer.
    Inherits all fields from AnswerBase.
    """
    pass


class AnswerUpdate(AnswerBase):
    """
    Schema for updating an existing Answer.

    Fields:
        text (str | None): Optional text override.
        is_correct (bool | None): Optional correct-flag override.
        question_id (int | None): Optional question ID override.
    """

    text: str = Field(
        None,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    is_correct: bool | None = False
    question_id: int | None


class AnswerResponse(BaseModel):
    """
    Response schema for an Answer entity.

    Attributes:
        id (int): The unique identifier of the Answer.
        text (str): Text of the answer.
        image_url (str | None): Optional image URL.
        is_correct (bool): Indicates if the answer is correct.
        question_id (int): ID of the associated question.
    """

    id: int
    text: str
    image_url: str | None
    is_correct: bool
    question_id: int

    class Config:
        from_attributes = True
