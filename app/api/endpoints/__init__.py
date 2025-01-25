"""
This package initializes and exports API router modules for different
resources such as answers, categories, questions, topics, and users.
"""

from .answer import router as answer_router  # noqa
from .category import router as category_router  # noqa
from .question import router as question_router  # noqa
from .topic import router as topic_router  # noqa
from .user import router as user_router  # noqa
