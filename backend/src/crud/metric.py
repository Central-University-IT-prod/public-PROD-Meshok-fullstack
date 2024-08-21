from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.metric import Metric


class CRUDMetric(CRUDBase[Metric]):
    async def get_metric(
            self,
            org_id: int,
            session: AsyncSession
    ) -> Metric:
        stmt = (
            select(self.model)
            .where(self.model.org_id == org_id)
        )
        result = await session.execute(stmt)
        metric = result.scalar()

        if metric is None:
            metric = Metric(org_id=org_id)
            session.add(metric)
            await session.commit()
            await session.refresh(metric)
        return metric

    async def add_opened_form(
            self,
            org_id: int,
            session: AsyncSession
    ) -> Metric:
        metric = await self.get_metric(org_id, session)
        metric.forms_opened += 1
        await session.commit()
        await session.refresh(metric)
        return metric

    async def add_confirmed_form(
            self,
            org_id: int,
            session: AsyncSession
    ) -> Metric:
        metric = await self.get_metric(org_id, session)
        metric.forms_confirmed += 1
        await session.commit()
        await session.refresh(metric)
        return metric


metric_crud = CRUDMetric(Metric)
