from sqlalchemy.ext.asyncio import AsyncSession

from crud.answer import answer_crud
from crud.auth import user_crud
from models import User
from schemas.answer import AnswersResponse, AnswerCreate


async def add_answers(
    answers: list[AnswerCreate], session: AsyncSession, user: User
) -> list[AnswersResponse]:
    """Add list of answers and experience points to the user"""
    answers = await answer_crud.many_create(answers, session, user)
    await user_crud.add_points(user, session)
    return answers
