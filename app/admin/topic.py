"""
This module defines an admin view for the Topic model, used by sqladmin.
"""

from sqladmin import ModelView

from app.models import Topic


class TopicAdmin(ModelView):
    """
    Admin configuration for the Topic model.
    """

    model = Topic
    name = 'Topic'
    name_plural = 'Topics'
    identity = 'topic'
    icon = 'fa-solid fa-book'
    pk_columns = (Topic.id, )

    column_list = ('id', 'name', 'category')

    column_labels = {
        'id': 'ID',
        'name': 'Topic name',
        'category': 'Category',
    }

    column_searchable_list = ('name', )
