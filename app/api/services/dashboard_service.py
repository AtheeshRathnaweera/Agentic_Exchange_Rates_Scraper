from datetime import datetime
from typing import Dict, List, Optional, Tuple

from app.api.constants.rate_types import RATE_TYPES
from app.api.dtos.bank_basic_dto import BankBasicDTO
from app.api.dtos.currency_basic_dto import CurrencyBasicDTO
from app.api.dtos.currency_dto import CurrencyDTO
from app.api.dtos.dashboard_meta_dto import DashboardMetaDTO
from app.api.dtos.dashboard_rate_dto import DashboardRateDTO
from app.api.dtos.dashboard_today_rates_dto import DashboardTodayRateDTO
from app.api.dtos.rate_types_dto import RateTypesDTO
from db.models.currency import Currency
from db.models.raw_exchange_rate import RawExchangeRate
from db.repositories.dashboard_repository import DashboardRepository
from db.repositories.raw_exchange_rate_repository import RawExchangeRateRepository
from db.repositories.scraper_job_repository import ScraperJobRepository
from db.repositories.bank_repository import BankRepository
from db.repositories.currency_repository import CurrencyRepository
from utils import get_logger

logger = get_logger(__name__)


class DashboardService:

    def __init__(
        self,
        dashboard_repo: DashboardRepository = None,
        raw_exhange_repo: RawExchangeRateRepository = None,
        scraper_job_repo: ScraperJobRepository = None,
        currency_repo: CurrencyRepository = None,
        bank_repo: BankRepository = None,
        correlation_id: str | None = None,
    ):
        self._dashboard_repo = dashboard_repo
        self._raw_exchange_repo = raw_exhange_repo
        self._scraper_job_repo = scraper_job_repo
        self._currency_repo = currency_repo
        self._bank_repo = bank_repo
        self._correlation_id = correlation_id

    def get_dashboard_data(self) -> DashboardMetaDTO:
        # all currencies
        all_currencies = self._currency_repo.get_all()
        # all banks
        all_banks = self._bank_repo.get_all()
        # all rate types
        all_rate_types = RATE_TYPES
        # last updated time
        last_updated_time = self._raw_exchange_repo.get_last_updated_time()

        # prepare metadata
        meta_data: DashboardMetaDTO = DashboardMetaDTO(
            currencies=[
                CurrencyDTO.model_validate(currency, from_attributes=True)
                for currency in all_currencies
            ],
            banks=[
                BankBasicDTO.model_validate(bank, from_attributes=True)
                for bank in all_banks
            ],
            rate_types=[
                RateTypesDTO(id=key, name=value)
                for key, value in all_rate_types.items()
            ],
            last_updated_time=last_updated_time,
        )

        return meta_data

    def get_today_rates(
        self,
        search: Optional[str] = None,
        currency: Optional[str] = None,
        bank_code: Optional[str] = None,
        rate_type: Optional[str] = None,
    ) -> List[DashboardTodayRateDTO]:
        # Get today's date in YYYY-MM-DD format
        today = datetime.now().date().isoformat()
        rate_type_name = None

        if rate_type and rate_type in RATE_TYPES:
            rate_type_name = RATE_TYPES[rate_type]
        else:
            rate_type_name = "All Rate Types"

        today_rates: List[Tuple[RawExchangeRate, Currency]] = (
            self._dashboard_repo.get_by_created_date_with_filters(
                created_date=today,
                search=search,
                currency_code=currency,
                bank_code=bank_code,
            )
        )

        if not today_rates:
            logger.info("No rates found for today (%s) with given filters", today)
            return []

        processed_rates = []

        for rate, currency_info in today_rates:
            rates: List[Dict[str, float]] = []

            rate_mappings = {
                "tt": [
                    ("tt_buying", rate.tt_buying),
                    ("tt_selling", rate.tt_selling),
                ],
                "draft": [
                    ("draft_buying", rate.draft_buying),
                    ("draft_selling", rate.draft_selling),
                ],
                "cheques": [
                    ("cheques_buying", rate.cheques_buying),
                    ("cheques_selling", rate.cheques_selling),
                ],
                "currency": [
                    ("currency_buying", rate.currency_buying),
                    ("currency_selling", rate.currency_selling),
                ],
                "other": [
                    ("other_buying", rate.other_buying),
                    ("other_selling", rate.other_selling),
                ],
            }

            if rate_type and (rate_type in rate_mappings):
                for rate_name, rate_value in rate_mappings[rate_type]:
                    if rate_value is not None:
                        rates.append({"type": rate_name, "value": rate_value})
            else:
                # return all if rate type is null
                for rt_category in rate_mappings.values():
                    for rate_name, rate_value in rt_category:
                        if rate_value is not None:
                            rates.append({"type": rate_name, "value": rate_value})

            if len(rates) > 0:
                processed_rates.append(
                    DashboardTodayRateDTO(
                        id=rate.id,
                        bank_name=rate.bank_name,
                        last_updated=rate.last_updated,
                        currency=CurrencyBasicDTO.model_validate(
                            currency_info, from_attributes=True
                        ),
                        rates=DashboardRateDTO(name=rate_type_name, values=rates),
                        tag=rate.tag,
                        created_date=rate.created_date,
                    )
                )

        return processed_rates
