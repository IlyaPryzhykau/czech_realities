"""
This module contains Pydantic schemas for handling Category data.
"""

from pydantic import BaseModel, Field


MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 100


class CategoryBase(BaseModel):
    """
    Base schema for Category containing shared fields and validation constraints.

    Attributes:
        name (str): The name of the category.
    """

    name: str = Field(
        ...,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )


class CategoryCreate(CategoryBase):
    """
    Schema for creating a new Category.
    Inherits all fields from CategoryBase.
    """
    pass


class CategoryUpdate(CategoryBase):
    """
    Schema for updating an existing Category.
    Inherits all fields from CategoryBase.
    """
    pass


class CategoryResponse(BaseModel):
    """
    Response schema for a Category entity.

    Attributes:
        id (int): The unique identifier of the Category.
        name (str): Name of the category.
    """

    id: int
    name: str

    class Config:
        from_attributes = True
