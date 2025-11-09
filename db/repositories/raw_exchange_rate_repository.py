from typing import List
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
