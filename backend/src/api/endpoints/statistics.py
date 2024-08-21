from typing import Annotated, Literal

from fastapi import APIRouter, Query

from api.dependencies import CurrentOrgDep, CurrentSessionDep
from crud.question import question_crud
from schemas.statistics import StatisticRead
from schemas.user import Gender

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


@router.get(
    path="",
    response_model=list[StatisticRead],
    response_description="Organization statistics"
)
async def get_statistics(
        current_org: CurrentOrgDep,
        session: CurrentSessionDep,
        gender: Annotated[Gender, Query()] = None,
        age: Annotated[Literal["child", "adult"], Query()] = None,
):
    """Get organization statistics."""
    statistics = await question_crud.get_statistics(
        org_id=current_org.id,
        gender=gender,
        age=age,
        session=session
    )
    return statistics
