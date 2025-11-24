from datetime import datetime
from pydantic import BaseModel


class CurrencyDTO(BaseModel):
    id: int
    code: str
    symbol: str
    name: str
    country: str
    active: bool
    created_date: datetime
