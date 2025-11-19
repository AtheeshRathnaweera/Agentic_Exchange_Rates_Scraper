from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ScraperJobDTO(BaseModel):
    id: Optional[int]
    correlation_id: str
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    status: str
    message: Optional[str]
