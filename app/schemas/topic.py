from pydantic import BaseModel, Field

from .category import CategoryResponse


MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 100


class TopicBase(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    category_id: int


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicBase):
    pass


class TopicResponse(TopicBase):
    id: int

    class Config:
        orm_made = True


class TopicResponseWithCategoryName(TopicBase):
    id: int
    category: CategoryResponse

    class Config:
        orm_mode = True

