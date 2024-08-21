import enum

from pydantic import BaseModel, Field, ConfigDict

from schemas.org import OrganizationRead


class Type(str, enum.Enum):
    Smile = 'Smile'
    Range = "Range"


class QuestionBase(BaseModel):
    id: int
    description: str
    type: Type
    category: str


class QuestionCreate(BaseModel):
    description: str = Field(min_length=3, max_length=200)
    type: Type = Field(min_length=3, max_length=50)
    category: str = Field(min_length=2, max_length=30)


class QuestionDB(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    org_id: int


class QuestionWithOrg(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    organization: OrganizationRead


class AllQuestions(QuestionDB):
    pass


class QuestionsUserGetResponse(BaseModel):
    org_name: str
    questions: list[QuestionDB]
