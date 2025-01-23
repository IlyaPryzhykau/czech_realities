from pydantic import BaseModel, Field


MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 200


class AnswerBase(BaseModel):
    text: str = Field(
        ...,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    image_url: str | None
    is_correct: bool = False
    question_id: int


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    text: str = Field(
        None,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    is_correct: bool | None = False
    question_id: int | None


class AnswerResponse(AnswerBase):
    id: int

    class Config:
        orm_mode = True
