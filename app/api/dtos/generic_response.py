from typing import Optional, Any
from pydantic import BaseModel


class GenericResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Any] = None
