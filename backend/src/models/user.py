import enum

from sqlalchemy import Column, Integer, Enum, String
from sqlalchemy.orm import relationship

from core.db import Base


class Gender(str, enum.Enum):
    Male = "Male"
    Female = "Female"


class User(Base):
    __tablename__ = "users"

    gender = Column(Enum(Gender), default=Gender.Female)
    age = Column(Integer, nullable=False)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    points = Column(Integer, nullable=False, default=0)

    answers = relationship(
        "Answer",
        back_populates="user",
        uselist=True,
        lazy="selectin",
        cascade="all, delete-orphan",
    )
