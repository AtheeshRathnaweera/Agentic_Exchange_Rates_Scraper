from typing import List
from datetime import datetime
from pydantic import BaseModel

from app.api.dtos.currency_dto import CurrencyDTO
from app.api.dtos.rate_types_dto import RateTypesDTO
from app.api.dtos.bank_basic_dto import BankBasicDTO


class DashboardMetaDTO(BaseModel):
    currencies: List[CurrencyDTO]
    rate_types: List[RateTypesDTO]
    banks: List[BankBasicDTO]
    last_updated_time: datetime
