from fastapi import APIRouter

from app.api.endpoints import (
    category_router, question_router, topic_router,  user_router)


main_router = APIRouter()


main_router.include_router(
    category_router, prefix='/category', tags=['Category']
)

main_router.include_router(
    question_router, prefix='/question', tags=['Question']
)

main_router.include_router(
    topic_router, prefix='/topic', tags=['Topic']
)


main_router.include_router(user_router)
