from typing import List

from db.models import ScraperJobs
from db.repositories import BaseRepository


class ScraperJobStatusRepository(BaseRepository[ScraperJobs]):
    """
    Repository class for ScraperJobs model.
    """

    def __init__(self, db):
        """
        Initialize the repository with a database session
        """
        super().__init__(ScraperJobs, db)

    def get_by_correlation_id(self, correlation_id: str) -> List[ScraperJobs]:
        """
        Get status records by correlation id

        Args:
            correlation_id (str): The correlation id to filter records.

        Returns:
            List[ScraperJobs]: List of matching ScraperJobs records.
        """
        return (
            self.db.query(self.model)
            .filter(self.model.correlation_id == correlation_id)
            .all()
        )
