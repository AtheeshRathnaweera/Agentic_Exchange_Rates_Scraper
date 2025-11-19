"""
This module provides factory functions for creating service instances
without relying on FastAPI's dependency injection system.

Use these functions when you need to instantiate services in contexts
such as background tasks, scripts, or anywhere FastAPI DI is not available or desired.

Each factory manually initializes the required database session and repositories,
ensuring the service is fully configured for standalone use.
"""

from app.api.factories.repositories import (
    build_exchange_rates_repository,
    build_scraper_job_repository,
)
from app.api.services import ExchangeRatesService


def get_exchange_rates_service_with_cid(correlation_id: str) -> ExchangeRatesService:
    """
    Factory function to create an ExchangeRatesService instance with the provided correlation ID.

    This function initializes the required database session and repositories,
    then constructs and returns an ExchangeRatesService configured for the given correlation ID.

    Args:
        correlation_id (str): Unique identifier for tracking the request or workflow.

    Returns:
        ExchangeRatesService: A fully configured service instance for exchange rate operations.
    """
    repo = build_exchange_rates_repository()
    scraper_repo = build_scraper_job_repository()

    return ExchangeRatesService(
        repo=repo,
        job_repo=scraper_repo,
        correlation_id=correlation_id,
    )
