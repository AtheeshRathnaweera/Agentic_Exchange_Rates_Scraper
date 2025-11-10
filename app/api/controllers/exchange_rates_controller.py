import uuid
from typing import List
from fastapi import APIRouter, Request, Depends

from app.api.dtos import GenericResponse, RawExchangeRateDTO
from app.api.services import ExchangeRatesService
from db.session import get_db
from utils import get_logger

logger = get_logger(__name__)


class ExchangeRatesController:
    router = APIRouter(prefix="/exchange-rates", tags=["Exchange Rates"])

    @router.post("/run-scraper", response_model=GenericResponse)
    # pylint: disable=no-self-argument
    async def run_scraper(
        request: Request,
    ):
        """
        Endpoint to trigger the exchange rates scraping workflow.
        """
        return await ExchangeRatesService(correlation_id=str(uuid.uuid4())).run_scraper(
            request
        )

    @router.get("/", response_model=List[RawExchangeRateDTO])
    # pylint: disable=no-self-argument
    async def get_all(db=Depends(get_db)):
        """
        Get all exchange rates.
        """
        return ExchangeRatesService(db=db, correlation_id=str(uuid.uuid4())).get_all()
