import bcrypt
from fastapi import APIRouter

from api.auth_errors import BAD_CREDENTIALS, ENTITY_EXISTS
from api.dependencies import CurrentSessionDep, CurrentUserDep
from core.auth import generate_jwt
from crud.answer import answer_crud
from crud.auth import user_crud
from schemas.answer import UserAnswersResponse
from schemas.auth import Auth, AuthResponse, UserRegisterResponse
from schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    path="/register",
    name="Register user",
    response_model=UserRegisterResponse,
    response_description="Registered user",
    status_code=201,
)
async def register(create_schema: UserCreate, session: CurrentSessionDep):
    """Register user."""
    db_user = await user_crud.get_by_email(email=create_schema.email, session=session)
    if db_user is not None:
        raise ENTITY_EXISTS

    new_user = await user_crud.create_entity(schema=create_schema, session=session)

    token = generate_jwt(email=new_user.email, issuer="user")
    return UserRegisterResponse(user=new_user, auth=AuthResponse(token=token))


@router.post(
    path="/login",
    name="Login user",
    response_model=AuthResponse,
    response_description="Credentials",
)
async def login(auth_data: Auth, session: CurrentSessionDep):
    """Login user."""
    user = await user_crud.get_by_email(email=auth_data.email, session=session)
    if user is None:
        raise BAD_CREDENTIALS
    if not bcrypt.checkpw(
            hashed_password=user.hashed_password.encode(),
            password=auth_data.password.encode(),
    ):
        raise BAD_CREDENTIALS

    token = generate_jwt(email=auth_data.email, issuer="user")

    return AuthResponse(token=token)


@router.get(
    path="/me",
    name="Get info about logged user",
    response_model_exclude_none=True,
    response_model=UserRead,
    response_description="Info about logged user",
)
async def show_user(current_user: CurrentUserDep):
    """Get info about logged user."""
    return current_user


@router.get(
    path="/answers",
    name="Get user answers",
    response_model_exclude_none=True,
    response_model_exclude={"user"},
    response_model=list[UserAnswersResponse],
    response_description="List of user answers",
)
async def get_user_answers(session: CurrentSessionDep, user: CurrentUserDep):
    """Get user answers."""
    return await answer_crud.get_user_answers(session, user.id)
