import uuid
from fastapi import Depends

from app.api.dependencies.repositories import (
    get_exchange_rates_repository,
    get_scraper_job_repository,
)
from app.api.services import ExchangeRatesService


def get_exchange_rates_service(
    repo=Depends(get_exchange_rates_repository),
    job_repo=Depends(get_scraper_job_repository),
) -> ExchangeRatesService:
    """
    Dependency injection factory for ExchangeRatesService.

    Creates a new instance of ExchangeRatesService with a database session
    and correlation ID for request tracking.

    Args:
        repo: RawExchangeRateRepository instance (automatically injected).
        job_repo: ScraperJobRepository instance (automatically injected).

    Returns:
        ExchangeRatesService: Configured service instance for handling exchange rate operations.
    """
    correlation_id = str(uuid.uuid4())
    return ExchangeRatesService(
        repo=repo, job_repo=job_repo, correlation_id=correlation_id
    )
