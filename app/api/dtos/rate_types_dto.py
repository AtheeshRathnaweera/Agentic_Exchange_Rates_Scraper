from pydantic import BaseModel


class RateTypesDTO(BaseModel):
    id: str
    name: str
