from typing import Optional
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

    def get_by_code(self, code: str) -> Optional[Currency]:
        """
        Get an active currency by its unique code.

        Args:
            code (str): The currency code to search for

        Returns:
            Optional[Currency]: The active currency if found, None otherwise
        """
        return (
            self.db.query(self.model)
            .filter(self.model.code == code.lower(), self.model.active)
            .first()
        )
