from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import lazyload
from sqlalchemy.sql import func

from crud.base import CRUDBase
from crud.metric import metric_crud
from models import Question, User, Answer, Organization
from models.user import Gender


class CRUDQuestion(CRUDBase[Question]):
    async def create(
            self, obj_in, session: AsyncSession, org: Organization
    ):
        obj_in_data = obj_in.dict()
        obj_in_data["org_id"] = org.id
        db_obj = self.model(**obj_in_data)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def get_org_questions(
            self,
            user: User,
            session: AsyncSession,
    ) -> Sequence[Question]:
        donations = await session.execute(
            select(Question).where(Question.org_id == user.id)
        )
        return donations.scalars().all()

    async def get_questions(self, org_id, session: AsyncSession) -> Sequence[Question]:
        await metric_crud.add_opened_form(
            org_id=org_id,
            session=session
        )

        answers = (await session.execute(
            select(Question)
            .outerjoin(Answer, Answer.question_id == Question.id)
            .options(lazyload(Question.organization))
            .where(Question.org_id == org_id)
            .group_by(Question.id)
            .order_by(func.count(Answer.id))
            .limit(3)
        )).all()

        return [a.Question for a in answers]

    async def get_statistics(
            self,
            org_id: int,
            session: AsyncSession,
            gender: Gender | None = None,
            age: str | None = None
    ):
        sub_query_stmt = (
            select(
                Answer.question_id,
                Answer.answer,
                func.count().label('answers_count')
            )
            .group_by(
                Answer.question_id,
                Answer.answer
            )
        )
        if gender is not None:
            sub_query_stmt = sub_query_stmt.where(
                Answer.user.has(User.gender == gender)
            )
        if age is not None:
            if age == "child":
                sub_query_stmt = sub_query_stmt.where(
                    Answer.user.has(User.age < 18)
                )
            elif age == "adult":
                sub_query_stmt = sub_query_stmt.where(
                    Answer.user.has(User.age >= 18)
                )

        sub_query = sub_query_stmt.subquery()

        stmt = (
            select(
                self.model.description.label('question'),
                self.model.category,
                self.model.type,
                func.jsonb_object_agg(
                    sub_query.c.answer,
                    sub_query.c.answers_count
                ).label('stats')
            )
            .join(
                sub_query,
                onclause=self.model.id == sub_query.c.question_id
            )
            .group_by(
                self.model.id,
                self.model.description
            )
            .where(
                self.model.org_id == org_id
            )
        )

        result = await session.execute(stmt)

        return result.mappings().all()


question_crud = CRUDQuestion(Question)
