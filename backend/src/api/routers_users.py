from fastapi import APIRouter

from api.endpoints import (
    user_router,
    question_router
)

users_router = APIRouter()
users_router.include_router(user_router)
users_router.include_router(
    question_router, prefix="/forms", tags=["Question"]
)
