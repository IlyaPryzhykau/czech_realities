from sqladmin import ModelView
from app.models import Category


class CategoryAdmin(ModelView):
    model = Category
    name = 'Category'
    name_plural = 'Categories'
    icon = 'fa-solid fa-tags'
    column_list = ['id', 'name']
    pk_columns = [Category.id]
    identity = 'category'
