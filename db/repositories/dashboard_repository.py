from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import Date, or_, asc

from db.models.currency import Currency
from db.models.raw_exchange_rate import RawExchangeRate
from utils import get_logger

logger = get_logger(__name__)


class DashboardRepository:
    """
    Repository for dashboard-specific queries that span multiple tables
    and provide optimized data access for dashboard views.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_created_date_with_filters(
        self,
        created_date: str,
        search: Optional[str] = None,
        currency_code: Optional[str] = None,
        bank_code: Optional[str] = None,
    ) -> List[Tuple[RawExchangeRate, Currency]]:
        """
        Get today's exchange rates with currency details in a single optimized query.

        Returns:
            List[Tuple[RawExchangeRate, Currency]]: List of tuples containing rate and currency data
        """
        logger.info(
            "dashboard rates called: search: %s currency: %s bank: %s created_date: %s",
            search,
            currency_code,
            bank_code,
            created_date,
        )
        try:
            date_obj = datetime.strptime(created_date, "%Y-%m-%d").date()
        except ValueError as e:
            logger.error("Invalid date format: %s", created_date)
            raise ValueError(
                f"Invalid date format. Expected 'YYYY-MM-DD', got '{created_date}'"
            ) from e

        # Start with base date query
        query = (
            self.db.query(RawExchangeRate, Currency)
            .join(Currency, RawExchangeRate.currency_code == Currency.code)
            .filter(
                RawExchangeRate.created_date.cast(Date) == date_obj,
                Currency.active,
            )
        )

        # Apply search filter (assuming currency relationship exists)
        if search and search.strip():
            clean_search = search.strip().replace("%", r"\%").replace("_", r"\_")
            search_term = f"%{clean_search}%"

            query = query.filter(
                or_(
                    RawExchangeRate.currency_code.ilike(search_term),
                    RawExchangeRate.currency_name.ilike(search_term),
                    RawExchangeRate.bank_name.ilike(search_term),
                )
            )

        # Apply currency filter
        if currency_code and currency_code.strip():
            query = query.filter(RawExchangeRate.currency_code == currency_code.strip())

        # Apply bank filter
        if bank_code and bank_code.strip():
            query = query.filter(RawExchangeRate.tag == bank_code.strip())

        # Order by currency code and bank name for consistent results
        query = query.order_by(
            asc(RawExchangeRate.currency_code), asc(RawExchangeRate.bank_name)
        )

        results = query.all()
        logger.info(
            "Found %s rates for %s with applied filters", len(results), created_date
        )

        return results
