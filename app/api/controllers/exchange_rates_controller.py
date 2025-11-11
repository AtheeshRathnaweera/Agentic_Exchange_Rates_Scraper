import asyncio
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
    async def run_scraper(request: Request):
        """
        Endpoint to trigger the exchange rates scraping workflow.
        """
        correlation_id = str(uuid.uuid4())
        # pylint: disable=no-member
        body = await request.body()  # extract body before task starts

        service = ExchangeRatesService(correlation_id=correlation_id)
        # Fire and forget safely
        asyncio.create_task(service.run_scraper(body))

        logger.info(
            "Scraper started in background. Correlation ID: %s",
            correlation_id,
        )

        # background_tasks.add_task(service.run_scraper_background, body)
        return GenericResponse(
            status="accepted",
            message=f"Scraper started in background. Correlation ID: {correlation_id}",
        )

    @router.get("/", response_model=List[RawExchangeRateDTO])
    # pylint: disable=no-self-argument
    async def get_all(db=Depends(get_db)):
        """
        Get all exchange rates.
        """
        return ExchangeRatesService(db=db, correlation_id=str(uuid.uuid4())).get_all()

    @router.get("/date/{date}", response_model=List[RawExchangeRateDTO])
    # pylint: disable=no-self-argument
    async def get_all_by_date(date: str, db=Depends(get_db)):
        """
        Get all exchange rates by date.
        """
        return ExchangeRatesService(db=db).get_all_by_date(date)

    @router.get("/year-month/{date}", response_model=List[RawExchangeRateDTO])
    # pylint: disable=no-self-argument
    async def get_all_by_month(year_month: str, db=Depends(get_db)):
        """
        Get all exchange rates by year and the month.
        """
        return ExchangeRatesService(db=db).get_all_by_year_month(year_month)
