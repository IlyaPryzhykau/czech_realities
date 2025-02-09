"""
This module defines an admin view for the Question model, used by sqladmin.
"""

from sqladmin import ModelView

from db_models import Question


class QuestionAdmin(ModelView):
    """
    Admin configuration for the Question model.
    """

    model = Question
    name = 'Question'
    name_plural = 'Questions'
    identity = 'question'
    icon = 'fa-solid fa-question'
    pk_columns = (Question.id, )

    column_list = ('id', 'text', 'image_url', 'topic', 'update_date')

    column_labels = {
        'id': 'ID',
        'text': 'Question text',
        'image_url': 'Image URL',
        'topic': 'Topic',
        'update_date': 'Update date',
    }

    column_searchable_list = ('text', )
