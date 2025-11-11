from datetime import datetime
from typing import List

from sqlalchemy import Date, extract
from db.models.raw_exchange_rate import RawExchangeRate
from db.repositories import BaseRepository


class RawExchangeRateRepository(BaseRepository[RawExchangeRate]):
    """
    Repository class for RawExchangeRate model.
    """

    def __init__(self, db):
        """
        Initialize the repository with a database session
        """
        super().__init__(RawExchangeRate, db)

    def get_by_created_date(self, created_date: str) -> List[RawExchangeRate]:
        """
        Get all RawExchangeRate records by created date.

        Args:
            created_date (str): The date to filter records (in 'YYYY-MM-DD' format).

        Returns:
            List[RawExchangeRate]: List of matching RawExchangeRate records.
        """
        date_obj = datetime.strptime(created_date, "%Y-%m-%d").date()
        return (
            self.db.query(self.model)
            .filter(self.model.created_date.cast(Date) == date_obj)
            .all()
        )

    def get_by_created_year_month(
        self, created_year_month: str
    ) -> List[RawExchangeRate]:
        """
        Get all RawExchangeRate records by created month.

        Args:
            created_month (str): The month to filter records (in 'YYYY-MM' format).

        Returns:
            List[RawExchangeRate]: List of matching RawExchangeRate records.
        """
        # Extract year and month from the string
        year, month = created_year_month.split("-")
        return (
            self.db.query(self.model)
            .filter(
                extract("year", self.model.created_date) == int(year),
                extract("month", self.model.created_date) == int(month),
            )
            .all()
        )

    def save(self, new_obj: RawExchangeRate):
        """
        Save a single RawExchangeRate object to the database.
        """
        return self.create(new_obj)

    def save_bulk(self, new_objs: List[RawExchangeRate]):
        """
        Save multiple RawExchangeRate objects to the database in bulk.
        """
        return self.bulk_create(new_objs)
