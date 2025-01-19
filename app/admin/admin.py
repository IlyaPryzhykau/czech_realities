from sqladmin import Admin

from app.core.config import settings
from app.core.db import engine
from app.admin.base import BasicAuthBackend
from app.admin.category import CategoryAdmin
from app.admin.topic import TopicAdmin
from app.admin.question import QuestionAdmin


auth_backend = BasicAuthBackend(secret_key=settings.secret)


def create_admin(app):
    admin = Admin(app=app, engine=engine, authentication_backend=auth_backend)
    admin.add_view(CategoryAdmin)
    admin.add_view(TopicAdmin)
    admin.add_view(QuestionAdmin)
