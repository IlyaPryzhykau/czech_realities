from sqladmin import ModelView
from app.models import Question


class QuestionAdmin(ModelView):
    model = Question
    name = 'Question'
    name_plural = 'Questions'
    icon = 'fa-solid fa-question'
    column_list = ['id', 'text', 'topic_id', 'update_date']
    pk_columns = [Question.id]
    identity = 'question'
