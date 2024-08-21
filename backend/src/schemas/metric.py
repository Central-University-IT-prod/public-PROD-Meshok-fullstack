from pydantic import BaseModel


class MetricRead(BaseModel):
    forms_opened: int
    forms_confirmed: int
