from typing import Annotated

from fastapi import APIRouter, Path

from api.auth_errors import FORBIDDEN
from api.dependencies import (
    CurrentOrgDep,
    CurrentSessionDep,
    CurrentUserDep,
)
from api.validators import check_question_exists, check_organization_exists
from crud.question import question_crud
from schemas.answer import AnswersResponse, AnswerCreate
from schemas.question import AllQuestions, QuestionDB
from schemas.question import QuestionCreate, QuestionsUserGetResponse
from services.add_answers import add_answers

router = APIRouter()


@router.get(
    path="",
    name="Get organization's questions",
    response_model_exclude_none=True,
    response_model=list[AllQuestions],
    response_description="List of organization's questions",
)
async def get_all_question(session: CurrentSessionDep, org: CurrentOrgDep):
    """Get organization questions."""
    return await question_crud.get_org_questions(org, session)


@router.post(
    path="/add",
    name="Add question",
    response_description="Created question",
    response_model_exclude_none=True,
    response_model=QuestionDB,
)
async def add_question(
    question: QuestionCreate,
    session: CurrentSessionDep,
    org: CurrentOrgDep,
):
    """Add question."""
    new_question = await question_crud.create(question, session, org)
    return new_question


@router.delete(
    path="/{question_id}/remove",
    name="Delete question by id",
    response_model=QuestionDB,
    response_description="Deleted question",
)
async def delete_question(
    question_id: Annotated[int, Path()],
    session: CurrentSessionDep,
    current_org: CurrentOrgDep,
):
    """Delete question by id."""
    question = await check_question_exists(question_id, session)
    if question.org_id != current_org.id:
        raise FORBIDDEN

    question_del = await question_crud.remove(question, session)
    return question_del


@router.post(
    path="",
    name="Create user`s answers",
    response_model_exclude_none=True,
    response_model=list[AnswersResponse],
    response_description="Created answers",
)
async def create_many_answers(
    answers: list[AnswerCreate], session: CurrentSessionDep, user: CurrentUserDep
):
    """Create user answers."""
    return await add_answers(answers, session, user)


@router.get(
    path="/{org_id}",
    name="Get questions which have few answers",
    response_model_exclude_none=True,
    response_model=QuestionsUserGetResponse,
    response_description="List of questions",
)
async def get_questions(org_id: Annotated[int, Path()], session: CurrentSessionDep):
    """Get questions which have few answers."""
    org = await check_organization_exists(org_id, session)
    org_name = org.name
    questions = await question_crud.get_questions(org_id, session)
    return {"org_name": org_name, "questions": questions}
