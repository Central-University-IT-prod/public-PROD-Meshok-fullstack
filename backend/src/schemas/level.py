from pydantic import BaseModel


class UserLevel(BaseModel):
    current_level: str
    next_level: str | None = None
    min_xp: int
    max_xp: int | None = None
    current_xp: int
