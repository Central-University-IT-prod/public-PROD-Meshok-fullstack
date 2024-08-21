from pydantic import BaseModel, ConfigDict

from schemas.question import QuestionWithOrg, QuestionDB
from schemas.user import UserRead


class AnswersResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: UserRead
    question: QuestionDB
    answer: int


class UserAnswersResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question: QuestionWithOrg
    answer: int


class AnswerCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_id: int
    answer: int
