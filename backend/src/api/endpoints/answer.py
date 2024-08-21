from typing import Annotated

from fastapi import APIRouter, Path

from api.auth_errors import FORBIDDEN
from api.dependencies import CurrentSessionDep, CurrentOrgDep
from api.validators import check_question_exists
from crud.answer import answer_crud
from schemas.answer import AnswersResponse

router = APIRouter()


@router.get(
    path='/{question_id}',
    response_model_exclude_none=True,
    response_model=list[AnswersResponse],
    response_description="List of answers"
)
async def get_question_answers(
        question_id: Annotated[int, Path()],
        current_org: CurrentOrgDep,
        session: CurrentSessionDep
):
    """Get answers of organization questions."""
    question = await check_question_exists(question_id, session)
    if question.org_id != current_org.id:
        raise FORBIDDEN

    return await answer_crud.get_user_answers(
        session=session,
        question_id=question_id
    )
