from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.auth import org_crud
from crud.question import question_crud
from models import Question, Organization


async def check_question_exists(question_id: int, session: AsyncSession) -> Question:
    question = await question_crud.get(question_id, session)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вопрос не найден!"
        )
    return question


async def check_organization_exists(org_id: int, session: AsyncSession) -> Organization:
    org = await org_crud.get(org_id, session)
    if org is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Организация не найдена!"
        )
    return org
