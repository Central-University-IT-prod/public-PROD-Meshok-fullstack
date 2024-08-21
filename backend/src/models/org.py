from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.db import Base


class Organization(Base):
    __tablename__ = 'orgs'

    name = Column(String, nullable=False)
    email = Column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password = Column(
        String(length=1024), nullable=False
    )

    questions = relationship(
        "Question",
        back_populates="organization",
        uselist=True,
        lazy="selectin",
        cascade="all, delete-orphan",
    )
