from pydantic import BaseModel


class CurrencyBasicDTO(BaseModel):
    code: str
    symbol: str
    name: str
