from pydantic import BaseModel, Field


MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 100


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True
