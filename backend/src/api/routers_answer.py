from fastapi import APIRouter

from api.endpoints import answer_router


answers_router = APIRouter()

answers_router.include_router(
    answer_router, prefix='/answers', tags=['Answer'])
