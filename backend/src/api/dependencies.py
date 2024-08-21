from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth_errors import BAD_CREDENTIALS
from core.auth import decode_jwt
from core.db import get_async_session
from crud.auth import user_crud, org_crud
from models import User
from models.org import Organization

CurrentSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def get_current_user(
        token: Annotated[
            HTTPAuthorizationCredentials,
            Depends(HTTPBearer(scheme_name="User"))
        ],
        session: CurrentSessionDep
) -> User:
    try:
        jwt_data = decode_jwt(
            token=token.credentials
        )
    except PyJWTError:
        raise BAD_CREDENTIALS
    if jwt_data.issuer != "user":
        raise BAD_CREDENTIALS
    user = await user_crud.get_by_email(
        email=jwt_data.email,
        session=session
    )
    if user is None:
        raise BAD_CREDENTIALS
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_org(
        token: Annotated[
            HTTPAuthorizationCredentials,
            Depends(HTTPBearer(scheme_name="Organization"))
        ],
        session: CurrentSessionDep
) -> Organization:
    try:
        jwt_data = decode_jwt(
            token=token.credentials
        )
    except PyJWTError:
        raise BAD_CREDENTIALS
    org = await org_crud.get_by_email(
        email=jwt_data.email,
        session=session
    )
    if jwt_data.issuer != "org":
        raise BAD_CREDENTIALS
    if org is None:
        raise BAD_CREDENTIALS
    return org


CurrentOrgDep = Annotated[Organization, Depends(get_current_org)]
