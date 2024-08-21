from typing import TypeVar

import bcrypt
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models import User
from models.org import Organization
from schemas.org import OrganizationCreate
from schemas.user import UserCreate

Model = TypeVar("Model", Organization, User)


class CRUDAuth(CRUDBase[Model]):
    async def get_by_email(self, email: str, session: AsyncSession) -> Model | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await session.execute(stmt)
        return result.scalar()


class CRUDUser(CRUDAuth[User]):
    async def create_entity(self, schema: UserCreate, session: AsyncSession) -> User:
        entity = self.model(
            gender=schema.gender,
            age=schema.age,
            email=schema.email,
            hashed_password=bcrypt.hashpw(
                password=schema.password.encode(), salt=bcrypt.gensalt()
            ).decode(),
        )
        session.add(entity)
        await session.commit()
        await session.refresh(entity)

        return entity

    async def add_points(self, user: User, session: AsyncSession) -> User:
        user.points += 70
        await session.commit()
        return user


class CRUDOrg(CRUDAuth[Organization]):
    async def create_entity(
        self, schema: OrganizationCreate, session: AsyncSession
    ) -> Organization:
        entity = self.model(
            name=schema.name,
            email=schema.email,
            hashed_password=bcrypt.hashpw(
                password=schema.password.encode(), salt=bcrypt.gensalt()
            ).decode(),
        )
        session.add(entity)
        await session.commit()
        await session.refresh(entity)

        return entity


user_crud = CRUDUser(User)
org_crud = CRUDOrg(Organization)
