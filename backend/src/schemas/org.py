from pydantic import (
    EmailStr,
    ConfigDict,
    BaseModel,
    Field
)


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr = Field(min_length=5, max_length=150)
    password: str = Field(min_length=8, max_length=150)


class OrganizationUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
