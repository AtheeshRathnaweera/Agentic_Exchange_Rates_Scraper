from pydantic import BaseModel


class DashboardRateDTO(BaseModel):
    type: str
    value: float
