from db.models.currency import Currency
from db.repositories.base_repository import BaseRepository


class CurrencyRepository(BaseRepository[Currency]):
    """
    Repository class for Currency model.
    """

    def __init__(self, db):
        """
        Initialize the repository with a database session
        """
        super().__init__(model=Currency, db=db)
