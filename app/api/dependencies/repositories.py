from fastapi import Depends

from db.session import get_db
from db.repositories import RawExchangeRateRepository, ScraperJobRepository


def get_exchange_rates_repository(db=Depends(get_db)) -> RawExchangeRateRepository:
    """
    Dependency injection factory for RawExchangeRateRepository.

    Args:
        db: Database session dependency (automatically injected by FastAPI).

    Returns:
        RawExchangeRateRepository: Repository instance for exchange rate operations.
    """
    return RawExchangeRateRepository(db=db)


def get_scraper_job_repository(db=Depends(get_db)) -> ScraperJobRepository:
    """
    Dependency injection factory for ScraperJobRepository.

    Args:
        db: Database session dependency (automatically injected by FastAPI).

    Returns:
        ScraperJobRepository: Repository instance for job status operations.
    """
    return ScraperJobRepository(db=db)
