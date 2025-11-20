import asyncio
from typing import List
from fastapi import APIRouter, Request, Depends

from app.api.dependencies.services import get_exchange_rates_service
from app.api.dtos.generic_response import GenericResponse
from app.api.dtos.raw_echange_rate_dto import RawExchangeRateDTO
from app.api.factories.services import get_exchange_rates_service_with_cid
from app.api.services.exchange_rates_service import ExchangeRatesService
from app.models.scraper_job_status import ScraperJobStatus
from utils import get_logger

logger = get_logger(__name__)


class ExchangeRatesController:
    router = APIRouter(prefix="/exchange-rates", tags=["Exchange Rates"])

    @router.post("/run-scraper", response_model=GenericResponse)
    # pylint: disable=no-self-argument
    async def run_scraper(
        request: Request,
        service: ExchangeRatesService = Depends(get_exchange_rates_service),
    ):
        """
        Endpoint to trigger the exchange rates scraping workflow.
        """
        correlation_id = service.correlation_id
        # pylint: disable=no-member
        body = await request.body()  # extract body before task starts

        # Create separate service instance for background task
        ex_rate_service = get_exchange_rates_service_with_cid(
            correlation_id=correlation_id
        )
        # Fire and forget safely
        scraper_task = asyncio.create_task(
            ex_rate_service.run_scraper(body), name=f"scraper-{correlation_id}"
        )

        # Record job initiation in database with SCHEDULED status for tracking
        service.add_scraper_job_status(ScraperJobStatus.SCHEDULED)

        logger.info(
            "Scraper started in background. Correlation ID: %s, Task: %s",
            correlation_id,
            scraper_task.get_name(),
        )

        return GenericResponse(
            status="accepted",
            message=f"Scraper started in background. Correlation ID: {correlation_id}",
        )

    @router.get("/", response_model=List[RawExchangeRateDTO])
    # pylint: disable=no-self-argument
    async def get_all(
        service: ExchangeRatesService = Depends(get_exchange_rates_service),
    ):
        """
        Get all exchange rates.
        """
        return service.get_all()

    @router.get("/date/{date}", response_model=List[RawExchangeRateDTO])
    # pylint: disable=no-self-argument
    async def get_all_by_date(
        date: str,
        service: ExchangeRatesService = Depends(get_exchange_rates_service),
    ):
        """
        Get all exchange rates by date.
        """
        return service.get_all_by_date(date)

    @router.get("/year-month/{date}", response_model=List[RawExchangeRateDTO])
    # pylint: disable=no-self-argument
    async def get_all_by_month(
        year_month: str,
        service: ExchangeRatesService = Depends(get_exchange_rates_service),
    ):
        """
        Get all exchange rates by year and the month.
        """
        return service.get_all_by_year_month(year_month)
