"""
This module initializes and configures the admin interface,
adding model views for various resources (Category, Topic,
Question, and Answer).
"""

from sqladmin import Admin

from app.core.config import settings
from app.core.db_config import engine
from app.admin.base import BasicAuthBackend
from app.admin.answer import AnswerAdmin
from app.admin.category import CategoryAdmin
from app.admin.topic import TopicAdmin
from app.admin.question import QuestionAdmin


auth_backend = BasicAuthBackend(secret_key=settings.secret)


def create_admin(app):
    """
    Attach the Admin interface to a FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=auth_backend,
        base_url='/admin',
    )
    admin.add_view(CategoryAdmin)
    admin.add_view(TopicAdmin)
    admin.add_view(QuestionAdmin)
    admin.add_view(AnswerAdmin)
