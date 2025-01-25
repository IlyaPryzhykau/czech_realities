"""
This module contains Pydantic schemas for handling Topic data,
linking each topic to a specific category.
"""

from pydantic import BaseModel, Field

from .category import CategoryResponse


MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 100


class TopicBase(BaseModel):
    """
    Base schema for Topic with shared fields and validation constraints.

    Attributes:
        name (str): The name of the topic.
        category_id (int): The ID of the associated category.
    """

    name: str = Field(
        ...,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    category_id: int


class TopicCreate(TopicBase):
    """
    Schema for creating a new Topic.
    Inherits all fields from TopicBase.
    """
    pass


class TopicUpdate(TopicBase):
    """
    Schema for updating an existing Topic.
    Inherits all fields from TopicBase.
    """
    pass


class TopicResponse(BaseModel):
    """
    Response schema for a Topic entity.

    Attributes:
        id (int): The unique identifier of the topic.
        name (str): The name of the topic.
        category_id (int): The ID of the associated category.
    """

    id: int
    name: str
    category_id: int

    class Config:
        from_attributes = True


class TopicResponseWithCategoryName(BaseModel):
    """
    Extended response schema for a Topic entity,
    including detailed category information.

    Attributes:
        id (int): The unique identifier of the topic.
        name (str): The name of the topic.
        category (CategoryResponse): Detailed category info.
    """

    id: int
    name: str
    category: CategoryResponse

    class Config:
        from_attributes = True
