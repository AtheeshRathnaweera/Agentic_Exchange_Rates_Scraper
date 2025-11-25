from datetime import datetime

from app.api.dtos.currency_basic_dto import CurrencyBasicDTO


class CurrencyDTO(CurrencyBasicDTO):
    id: int
    country: str
    active: bool
    created_date: datetime
