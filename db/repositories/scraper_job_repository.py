from typing import List
from datetime import datetime, timezone

from app.models.scraper_job_status import ScraperJobStatus
from db.models.scraper_job import ScraperJob
from db.repositories.base_repository import BaseRepository


class ScraperJobRepository(BaseRepository[ScraperJob]):
    """
    Repository class for ScraperJob model.
    """

    def __init__(self, db):
        """
        Initialize the repository with a database session
        """
        super().__init__(model=ScraperJob, db=db)

    def get_by_correlation_id(self, correlation_id: str) -> List[ScraperJob]:
        """
        Get status records by correlation id

        Args:
            correlation_id (str): The correlation id to filter records.

        Returns:
            List[ScraperJob]: List of matching ScraperJob records.
        """
        return (
            self.db.query(self.model)
            .filter(self.model.correlation_id == correlation_id)
            .all()
        )

    def update_status_by_correlation_id(
        self, correlation_id: str, status: ScraperJobStatus
    ) -> ScraperJob | None:
        """
        Update the status for a scraper job by correlation ID.
        Automatically sets started_at timestamp when status is RUNNING.

        Args:
            correlation_id: The correlation ID to identify the job.
            status: The new status to set for the job.

        Returns:
            ScraperJob | None: The updated job record or None if not found.
        """
        status_entry = (
            self.db.query(self.model)
            .filter(self.model.correlation_id == correlation_id)
            .first()
        )

        if status_entry is None:
            return None

        # Build update data based on status
        update_data = {"status": status}

        # Set started_at only when status changes to RUNNING
        if status == ScraperJobStatus.RUNNING:
            update_data["started_at"] = datetime.now(timezone.utc)
        # Set finished_at only when status changes to SUCCESS
        if status in {ScraperJobStatus.SUCCESS, ScraperJobStatus.ERROR}:
            update_data["finished_at"] = datetime.now(timezone.utc)

        return self.update(obj_id=status_entry.id, update_data=update_data)
