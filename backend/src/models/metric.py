from sqlalchemy import Column, Integer, ForeignKey

from core.db import Base


class Metric(Base):
    org_id = Column(
        Integer,
        ForeignKey('orgs.id', ondelete='cascade'),
        nullable=False
    )
    forms_opened = Column(Integer, nullable=False, default=0)
    forms_confirmed = Column(Integer, nullable=False, default=0)
