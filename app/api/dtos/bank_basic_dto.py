from pydantic import BaseModel


class BankBasicDTO(BaseModel):
    id: int
    code: str
    name: str
    logo_url: str | None
    country: str
