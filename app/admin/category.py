"""
This module defines an admin view for the Category model, used by sqladmin.
"""

from sqladmin import ModelView

from db_models import Category


class CategoryAdmin(ModelView):
    """
    Admin configuration for the Category model.
    """

    model = Category
    name = 'Category'
    name_plural = 'Categories'
    identity = 'category'
    icon = 'fa-solid fa-tags'
    pk_columns = (Category.id, )

    column_list = ('id', 'name')

    column_labels = {
        'id': 'ID',
        'name': 'Category name',
    }
