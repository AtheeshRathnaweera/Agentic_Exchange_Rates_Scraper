from app.api.constants.rate_types import RATE_TYPES
from app.api.dtos.bank_basic_dto import BankBasicDTO
from app.api.dtos.currency_dto import CurrencyDTO
from app.api.dtos.dashboard_meta_dto import DashboardMetaDTO
from app.api.dtos.rate_types_dto import RateTypesDTO
from db.repositories.raw_exchange_rate_repository import RawExchangeRateRepository
from db.repositories.scraper_job_repository import ScraperJobRepository
from db.repositories.bank_repository import BankRepository
from db.repositories.currency_repository import CurrencyRepository


class DashboardService:

    def __init__(
        self,
        raw_exhange_repo: RawExchangeRateRepository = None,
        scraper_job_repo: ScraperJobRepository = None,
        currency_repo: CurrencyRepository = None,
        bank_repo: BankRepository = None,
        correlation_id: str | None = None,
    ):
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
