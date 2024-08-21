import enum
from sqlalchemy import Column, String, Text, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class Type(str, enum.Enum):
    Smile = 'Smile'
    Range = "Range"


class Question(Base):
    org_id = Column(Integer, ForeignKey('orgs.id', ondelete="cascade"))
    type = Column(Enum(Type), default=Type.Smile)
    description = Column(Text, nullable=False)
    category = Column(String(100))

    answers = relationship(
        "Answer",
        back_populates="question",
        uselist=True,
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    organization = relationship(
        "Organization",
        back_populates="questions",
        uselist=False,
        lazy="joined"
    )
