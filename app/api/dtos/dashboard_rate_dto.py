from pydantic import BaseModel
from typing import List


class RatesDTO(BaseModel):
    type: str
    value: float


class DashboardRateDTO(BaseModel):
    name: str
    values: List[RatesDTO]
