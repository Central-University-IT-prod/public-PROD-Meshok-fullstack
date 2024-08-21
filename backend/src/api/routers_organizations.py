from fastapi import APIRouter

from api.endpoints import (
    organization_router,
    statistics_router,
    metric_router
)

organizations_router = APIRouter(
    prefix="/orgs"
)

organizations_router.include_router(organization_router)
organizations_router.include_router(statistics_router)
organizations_router.include_router(metric_router)
