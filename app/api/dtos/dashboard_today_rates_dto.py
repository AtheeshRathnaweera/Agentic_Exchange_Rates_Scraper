from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.api.dtos.currency_basic_dto import CurrencyBasicDTO
from app.api.dtos.dashboard_rate_dto import DashboardRateDTO


class DashboardTodayRateDTO(BaseModel):
    id: int
    bank_name: str
    last_updated: datetime
    currency: CurrencyBasicDTO
    rates: List[DashboardRateDTO]
    tag: str
    created_date: datetime
