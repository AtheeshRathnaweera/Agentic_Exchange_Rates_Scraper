"""
This module provides factory functions for creating repository instances
without relying on FastAPI's dependency injection system.

Use these functions when you need to instantiate repositories in contexts
such as background tasks, scripts, or anywhere FastAPI DI is not available or desired.

Each factory manually initializes the required database session,
ensuring the repository is fully configured for standalone use.
"""

from db.repositories.raw_exchange_rate_repository import RawExchangeRateRepository
from db.repositories.scraper_job_repository import ScraperJobRepository
from db.session import get_db


def build_exchange_rates_repository() -> RawExchangeRateRepository:
    db = next(get_db())
    return RawExchangeRateRepository(db)


def build_scraper_job_repository() -> ScraperJobRepository:
    db = next(get_db())
    return ScraperJobRepository(db)
