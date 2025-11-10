from fastapi import Request
from agno.run.workflow import WorkflowRunOutput
from agno.utils.pprint import pprint_run_response

from db.repositories import RawExchangeRateRepository
from app.api.dtos import GenericResponse, RawExchangeRateDTO
from utils import get_logger
from workflows import get_scrape_rates_workflow

logger = get_logger(__name__)


class ExchangeRatesService:

    def __init__(self, db=None, correlation_id: str | None = None):
        self.db = db
        self.correlation_id = correlation_id
        self.repo = RawExchangeRateRepository(db=db) if db is not None else None

    async def run_scraper(self, request: Request):
        """
        Run the scraping workflow for exchange rates.

        Args:
            request (Request): The incoming FastAPI request object.

        Returns:
            GenericResponse: A generic response indicating success or error.
        """
        # pylint: disable=no-member
        body = await request.body()
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
                "Scraping workflow completed. Printing response:\n%s",
                pprint_run_response(response, markdown=True),
            )
            return GenericResponse(status="success", data=None)
        except Exception as e:
            logger.error("❌ Error occurred: %s", e)
            return GenericResponse(status="error", message=str(e))
        finally:
            logger.info("Scraper run finished.")

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
