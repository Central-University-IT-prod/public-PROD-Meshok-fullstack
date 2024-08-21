import bcrypt
from fastapi import APIRouter

from api.auth_errors import BAD_CREDENTIALS, ENTITY_EXISTS
from api.dependencies import CurrentSessionDep, CurrentOrgDep
from core.auth import generate_jwt
from crud.answer import answer_crud
from crud.auth import org_crud
from schemas.answer import AnswersResponse
from schemas.auth import Auth, AuthResponse, OrgRegisterResponse
from schemas.org import OrganizationCreate, OrganizationRead
from services.default_questions import add_default_questions
from services.gpt import org_hints

router = APIRouter(
    tags=["Organizations"]
)

@router.post(
    path="/register",
    name="Register organization",
    response_model=OrgRegisterResponse,
    response_description="Registered organization",
    status_code=201
)
async def register(
        create_schema: OrganizationCreate,
        session: CurrentSessionDep
):
    """Register organization."""
    db_org = await org_crud.get_by_email(
        email=create_schema.email,
        session=session
    )
    if db_org is not None:
        raise ENTITY_EXISTS

    new_org = await org_crud.create_entity(
        schema=create_schema,
        session=session
    )

    await add_default_questions(new_org, session)

    token = generate_jwt(
        email=new_org.email,
        issuer="org"
    )
    return OrgRegisterResponse(
        organization=new_org,
        auth=AuthResponse(
            token=token
        )
    )


@router.post(
    path="/login",
    name="Login organization",
    response_model=AuthResponse,
    response_description="Credentials"
)
async def login(
        auth_data: Auth,
        session: CurrentSessionDep
):
    """Login organization."""
    org = await org_crud.get_by_email(
        email=auth_data.email,
        session=session
    )
    if org is None:
        raise BAD_CREDENTIALS
    if not bcrypt.checkpw(
            hashed_password=org.hashed_password.encode(),
            password=auth_data.password.encode()
    ):
        raise BAD_CREDENTIALS

    token = generate_jwt(
        email=auth_data.email,
        issuer="org"
    )

    return AuthResponse(
        token=token
    )


@router.get(
    path="/me",
    name="Get info about logged organization",
    response_model=OrganizationRead,
    response_description="Info about logged organization"
)
async def show_org(
        current_org: CurrentOrgDep
):
    """Get info about logged organization."""
    return current_org


@router.get(
    path='/answers',
    name='Get answers for organization questions',
    response_model_exclude_none=True,
    response_model=list[AnswersResponse],
    response_description="List of answers"
)
async def get_org_answers(
        session: CurrentSessionDep,
        org: CurrentOrgDep
):
    """Get answers for organization questions."""
    return await answer_crud.get_all_answers(session, org.id)


@router.get(
    path='/hints',
    name='Get hints for organization',
    response_model_exclude_none=True,
    response_description="List of answers"
)
async def get_org_hints(
        session: CurrentSessionDep,
        org: CurrentOrgDep
):
    """Get hints for organization."""
    return await org_hints(org, session)
