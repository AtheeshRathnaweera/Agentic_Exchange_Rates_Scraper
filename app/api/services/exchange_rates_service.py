from agno.run.workflow import WorkflowRunOutput
from agno.utils.pprint import pprint_run_response

from db.repositories import RawExchangeRateRepository
from app.api.dtos import RawExchangeRateDTO
from utils import get_logger
from workflows import get_scrape_rates_workflow

logger = get_logger(__name__)


class ExchangeRatesService:

    def __init__(self, db=None, correlation_id: str | None = None):
        self.db = db
        self.correlation_id = correlation_id
        self.repo = RawExchangeRateRepository(db=db) if db is not None else None

    async def run_scraper(self, body: bytes):
        """
        Run the scraping workflow for exchange rates.

        Args:
            request (Request): The incoming FastAPI request object.

        Returns:
            GenericResponse: A generic response indicating success or error.
        """
        logger.info(
            "Received request body: %s Using correlation_id: %s",
            body.decode("utf-8"),
            self.correlation_id,
        )
        try:
            response: WorkflowRunOutput = await get_scrape_rates_workflow(
                correlation_id=self.correlation_id
            ).arun()
            logger.info(
                "Scraping workflow completed:\n%s",
                pprint_run_response(response, markdown=True),
            )
        except Exception as e:
            logger.exception("[%s] Error in scraper: %s", self.correlation_id, e)
        finally:
            logger.info("[%s] Scraper run finished.", self.correlation_id)

    def get_all(self):
        """
        Retrieve all exchange rates from the database and convert them to DTOs.

        Args:
            db: Database session instance.

        Returns:
            List[RawExchangeRateDTO]: List of exchange rate DTOs.
        """
        data = self.repo.get_all()
        return [RawExchangeRateDTO.model_validate(item) for item in data]

    def get_all_by_date(self, date: str):
        """
        Retrieve all exchange rates from the database for a specific created date and convert them to DTOs.

        Args:
            date (str): The date to filter exchange rates (expected format 'YYYY-MM-DD').

        Returns:
            List[RawExchangeRateDTO]: List of exchange rate DTOs matching the specified date.
        """
        data = self.repo.get_by_created_date(date)
        return [RawExchangeRateDTO.model_validate(item) for item in data]

    def get_all_by_year_month(self, year_month: str):
        """
        Retrieve all exchange rates from the database for a specific year and month convert them to DTOs.

        Args:
            year and month (str): The date to filter exchange rates (expected format 'YYYY-MM').

        Returns:
            List[RawExchangeRateDTO]: List of exchange rate DTOs matching the specified month.
        """
        data = self.repo.get_by_created_year_month(year_month)
        return [RawExchangeRateDTO.model_validate(item) for item in data]
