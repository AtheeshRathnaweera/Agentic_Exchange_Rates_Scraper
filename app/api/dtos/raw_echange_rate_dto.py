from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RawExchangeRateDTO(BaseModel):
    id: Optional[int]
    bank_name: str
    country: str
    last_updated: datetime
    source_url: Optional[str]
    currency_name: str
    currency_code: str
    tt_buying: Optional[float]
    tt_selling: Optional[float]
    draft_buying: Optional[float]
    draft_selling: Optional[float]
    cheques_buying: Optional[float]
    cheques_selling: Optional[float]
    currency_buying: Optional[float]
    currency_selling: Optional[float]
    other_buying: Optional[float]
    other_selling: Optional[float]
    notes: Optional[str]
    tag: Optional[str]
    created_date: Optional[datetime]
    correlation_id: Optional[str]

    model_config = {"from_attributes": True}  # <- allows ORM objects to be parsed
