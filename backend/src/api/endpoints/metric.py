from fastapi import APIRouter

from api.dependencies import CurrentOrgDep, CurrentSessionDep
from crud.metric import metric_crud
from schemas.metric import MetricRead

router = APIRouter(
    prefix="/metric",
    tags=["Metric"]
)


@router.get(
    path="",
    response_description="Organization metric",
    response_model=MetricRead
)
async def get_metric(
        current_org: CurrentOrgDep,
        session: CurrentSessionDep
):
    """Get organization metric"""
    return await metric_crud.get_metric(
        org_id=current_org.id,
        session=session
    )
