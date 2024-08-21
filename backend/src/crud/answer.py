from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from crud.base import CRUDBase
from crud.metric import metric_crud
from models import Answer, User, Question
from schemas.answer import AnswerCreate


class CRUDAnswer(CRUDBase[Answer]):
    async def create(self, answer, question_id, session: AsyncSession, user: User):
        obj_dict = {"answer": answer, "question_id": question_id, "user_id": user.id}
        answer = self.model(**obj_dict)

        session.add(answer)
        await session.commit()
        await session.refresh(answer)

        return answer

    async def many_create(
            self, obj_list: list[AnswerCreate], session: AsyncSession, user: User
    ) -> list[Answer]:
        response = []
        for obj in obj_list:
            obj_dict = obj.dict()
            obj_dict["user_id"] = user.id
            answer = self.model(**obj_dict)

            session.add(answer)
            response.append(answer)
        await session.commit()
        for answer in response:
            await session.refresh(answer)

        await metric_crud.add_confirmed_form(
            org_id=response[0].question.org_id,
            session=session
        )

        return response

    async def get_user_answers(
            self, session: AsyncSession, user_id=None, question_id=None
    ) -> Sequence[Answer]:
        statement = select(Answer)
        if user_id:
            statement = statement.where(Answer.user_id == user_id)
        if question_id:
            statement = statement.where(Answer.question_id == question_id)
        answers = await session.execute(statement)
        return answers.scalars().all()

    async def get_all_answers(self, session: AsyncSession, org_id):
        stmt = select(self.model).where(
            self.model.question.has(Question.org_id == org_id)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_grouped_answers(
            self,
            org_id: int,
            session: AsyncSession
    ):
        stmt = (
            select(
                Question.description,
                Question.type,
                func.round(func.avg(self.model.answer), 2)
            )
            .join(Question)
            .where(
                self.model.question.has(Question.org_id == org_id)
            )
            .group_by(
                Question.description,
                Question.type,
            )
        )
        result = await session.execute(stmt)
        return result.all()


answer_crud = CRUDAnswer(Answer)
