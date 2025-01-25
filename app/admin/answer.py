"""
This module defines an admin view for the Answer model, used by sqladmin.
"""

from sqladmin import ModelView

from app.models import Answer


class AnswerAdmin(ModelView):
    """
    Admin configuration for the Answer model.

    Attributes:
        model (Type[Answer]): The SQLAlchemy model class.
        name (str): The display name for the model in the admin panel.
        name_plural (str): The plural display name in the admin panel.
        identity (str): The unique identity/path for this admin view.
        icon (str): A Font Awesome icon class for display.
        pk_columns (tuple): Primary key columns for identifying objects.
        column_list (tuple): Columns to display in the admin list view.
        column_labels (dict): Custom labels for columns.
    """

    model = Answer
    name = 'Answer'
    name_plural = 'Answers'
    identity = 'answer'
    icon = 'fa-solid fa-pen-question'
    pk_columns = (Answer.id, )

    column_list = ('id', 'text', 'image_url', 'is_correct', 'question')

    column_labels = {
        'id': 'ID',
        'text': 'Answer text',
        'image_url': 'Image URL',
        'is_correct': 'Correct?',
        'question': 'Question',
    }
