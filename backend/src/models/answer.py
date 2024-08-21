from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class Answer(Base):
    question_id = Column(
        Integer,
        ForeignKey('question.id', ondelete="cascade")
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete="cascade"))
    answer = Column(Integer)

    user = relationship(
        "User",
        back_populates="answers",
        uselist=False,
        lazy="joined"
    )
    question = relationship(
        "Question",
        back_populates="answers",
        uselist=False,
        lazy="joined"
    )
