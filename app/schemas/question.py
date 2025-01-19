from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator, field_serializer


MAX_NAME_LENGTH = 300
DATE_FORMAT = '%d.%m.%Y'
TIME_EXAMPLE = '12.12.2021'


class QuestionBase(BaseModel):
    text: str = Field(..., max_length=MAX_NAME_LENGTH)
    image_url: str | None = None
    topic_id: int
    update_date: date = Field(..., example=TIME_EXAMPLE)

    @field_validator('update_date', mode='before')
    def parse_update_date(cls, value):
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
        if value > datetime.now().date():
            raise ValueError('Update date cannot be in the future.')
        return value

    @field_serializer('update_date', when_used='json')
    def format_update_date(self, value: date) -> str:
        return value.strftime(DATE_FORMAT)


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    text: str | None = Field(None, max_length=MAX_NAME_LENGTH)
    topic_id: int | None
    update_date: date = Field(None, example=TIME_EXAMPLE)


class QuestionResponse(QuestionBase):
    id: int

    class Config:
        orm_mode = True
