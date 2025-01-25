"""
This module provides CRUD operations for the Answer model.
"""

from app.crud.base import CRUDBase
from app.models import Answer


class AnswerCRUD(CRUDBase):
    """
    Specialized CRUD for the Answer model.

    Inherits from:
        CRUDBase: Base class providing standard CRUD methods
        (get, create, etc.).
    """
    pass


answer_crud = AnswerCRUD(Answer)
