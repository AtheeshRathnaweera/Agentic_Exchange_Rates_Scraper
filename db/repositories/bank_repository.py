from db.models.bank import Bank
from db.repositories.base_repository import BaseRepository


class BankRepository(BaseRepository[Bank]):
    """
    Repository class for Bank model.
    """

    def __init__(self, db):
        """
        Initialize the repository with a database session
        """
        super().__init__(model=Bank, db=db)
