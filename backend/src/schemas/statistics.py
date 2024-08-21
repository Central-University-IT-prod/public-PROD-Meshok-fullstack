from pydantic import BaseModel

from schemas.question import Type


class StatisticRead(BaseModel):
    question: str
    type: Type
    stats: dict[int, int]
