from datetime import datetime
from typing import List
from agno.run.workflow import WorkflowRunOutput
from agno.utils.pprint import pprint_run_response
from agno.run.base import RunStatus

from app.api.dtos.raw_echange_rate_dto import RawExchangeRateDTO
from app.api.dtos.scraper_job_dto import ScraperJobDTO
from app.api.models.scraper_job_status import ScraperJobStatus
from db.models.scraper_job import ScraperJob
from db.repositories.raw_exchange_rate_repository import RawExchangeRateRepository
from db.repositories.scraper_job_repository import ScraperJobRepository
from utils import get_logger
from workflows import get_scrape_rates_workflow

logger = get_logger(__name__)


class ExchangeRatesService:

    def __init__(
        self,
        repo: RawExchangeRateRepository = None,
        job_repo: ScraperJobRepository = None,
        correlation_id: str | None = None,
    ):
        self._repo = repo
        self._job_repo = job_repo
        self._correlation_id = correlation_id

    @property
    def correlation_id(self) -> str:
        """Get the correlation ID for this service instance."""
        return self._correlation_id

    async def run_scraper(self) -> None:
        """
        Run the scraping workflow for exchange rates.

        Args:
            request (Request): The incoming FastAPI request object.

        Returns:
            GenericResponse: A generic response indicating success or error.
        """
        try:
            # Update scraper job status to RUNNING
            updated_job = self._job_repo.update_status_by_correlation_id(
                correlation_id=self._correlation_id, status=ScraperJobStatus.RUNNING
            )

            if updated_job is None:
                logger.warning(
                    "[%s] Failed to update job status to RUNNING - job not found",
                    self._correlation_id,
                )
            else:
                logger.info("[%s] Job status updated to RUNNING", self._correlation_id)

            response: WorkflowRunOutput = await get_scrape_rates_workflow(
                correlation_id=self._correlation_id
            ).arun()

            logger.info(
                "Scraping workflow current status:\n%s",
                response.status,
            )

            current_status = (
                ScraperJobStatus.SUCCESS
                if response.status == RunStatus.completed
                else ScraperJobStatus.ERROR
            )
            self._job_repo.update_status_by_correlation_id(
                correlation_id=self._correlation_id, status=current_status
            )

            logger.info(
                "Scraping workflow completed:\n%s",
                pprint_run_response(response, markdown=True),
            )
        except Exception as e:
            self._job_repo.update_status_by_correlation_id(
                correlation_id=self._correlation_id, status=ScraperJobStatus.ERROR
            )
            logger.exception("[%s] Error in scraper: %s", self._correlation_id, e)

    def get_all(self) -> List[RawExchangeRateDTO]:
        """
        Retrieve all exchange rates from the database and convert them to DTOs.

        Returns:
            List[RawExchangeRateDTO]: List of exchange rate DTOs.
        """
        data = self._repo.get_all()
        return [
            RawExchangeRateDTO.model_validate(item, from_attributes=True)
            for item in data
        ]

    def get_all_by_date(self, date: str) -> List[RawExchangeRateDTO]:
        """
        Retrieve all exchange rates from the database for a specific created
        date and convert them to DTOs.

        Args:
            date (str): The date to filter exchange rates (expected format 'YYYY-MM-DD').

        Returns:
            List[RawExchangeRateDTO]: List of exchange rate DTOs matching the specified date.
        """
        data = self._repo.get_by_created_date(date)
        return [
            RawExchangeRateDTO.model_validate(item, from_attributes=True)
            for item in data
        ]

    def get_all_by_year_month(self, year_month: str) -> List[RawExchangeRateDTO]:
        """
        Retrieve all exchange rates from the database for a specific year and
        month convert them to DTOs.

        Args:
            year and month (str): The date to filter exchange rates (expected format 'YYYY-MM').

        Returns:
            List[RawExchangeRateDTO]: List of exchange rate DTOs matching the specified month.
        """
        data = self._repo.get_by_created_year_month(year_month)
        return [
            RawExchangeRateDTO.model_validate(item, from_attributes=True)
            for item in data
        ]

    def add_scraper_job_status(self, status: ScraperJobStatus) -> ScraperJobDTO:
        """
        Create and save a new scraper job status entry.
        """
        logger.info("This is the correlation id: %s", self._correlation_id)
        new_status = ScraperJob(correlation_id=self._correlation_id, status=status)
        created_job = self._job_repo.create(new_status)
        return ScraperJobDTO.model_validate(created_job, from_attributes=True)

    def check_for_existing_scraper_jobs(self) -> bool:
        """
        Check if there are any non-failed scraper jobs for today.
        """
        # get the today date in 'YYYY-MM-DD'
        today_date = datetime.now().strftime("%Y-%m-%d")
        scraper_jobs: List[ScraperJob] = self._job_repo.get_by_started_date(today_date)

        # check for any with status other than error
        for scraper_job in scraper_jobs:
            if scraper_job.status != ScraperJobStatus.ERROR:
                return True
        return False
