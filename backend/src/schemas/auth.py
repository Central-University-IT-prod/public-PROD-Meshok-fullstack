from pydantic import EmailStr, BaseModel

from schemas.org import OrganizationRead
from schemas.user import UserRead


class Auth(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    type: str = "Bearer"


class UserRegisterResponse(BaseModel):
    user: UserRead
    auth: AuthResponse


class OrgRegisterResponse(BaseModel):
    organization: OrganizationRead
    auth: AuthResponse
