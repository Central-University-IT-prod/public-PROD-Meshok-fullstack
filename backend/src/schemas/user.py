import enum

from schemas.level import UserLevel
from utils.level import get_user_level
from pydantic import (
    PositiveInt,
    field_validator,
    EmailStr,
    ConfigDict,
    BaseModel,
    Field,
)


class Gender(str, enum.Enum):
    Male = "Male"
    Female = "Female"


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    age: PositiveInt
    gender: Gender
    points: UserLevel

    @field_validator("points", mode="before")
    @classmethod
    def get_user_points(cls, points: int | UserLevel) -> UserLevel:
        if isinstance(points, int):
            return get_user_level(points)
        return points


class UserCreate(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=150)
    password: str = Field(min_length=8, max_length=150)
    age: PositiveInt
    gender: Gender


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    age: PositiveInt | None = None
    gender: Gender | None = None
