from sqladmin import ModelView
from app.models import Topic


class TopicAdmin(ModelView):
    model = Topic
    name = 'Topic'
    name_plural = 'Topics'
    icon = 'fa-solid fa-book'
    column_list = ['id', 'name', 'category_id']
    pk_columns = [Topic.id]
    identity = 'topic'
