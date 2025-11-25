from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.api.dependencies.services import get_dashboard_service
from app.api.dtos.dashboard_today_rates_dto import DashboardTodayRateDTO
from app.api.services.dashboard_service import DashboardService

templates = Jinja2Templates(directory="app/ui/templates")


class DashboardController:
    router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

    @router.get("/")
    # pylint: disable=no-self-argument
    async def get_dashboard(
        request: Request,
        service: DashboardService = Depends(get_dashboard_service),
    ):
        dashboard_meta = service.get_dashboard_data()

        # Convert Pydantic models to dictionaries for template
        context = {
            "request": request,
            "data": {
                "currencies": [
                    {"id": currency.code, "value": f"{currency.code} - {currency.name}"}
                    for currency in dashboard_meta.currencies
                ],
                "rate_types": [
                    {
                        "id": rate_type.id,
                        "value": rate_type.name,
                    }
                    for rate_type in dashboard_meta.rate_types
                ],
                "banks": [
                    {"id": bank.code, "value": f"{bank.name}"}
                    for bank in dashboard_meta.banks
                ],
                "last_updated_time": dashboard_meta.last_updated_time.strftime(
                    "%b %d, %Y %I:%M %p"
                ),
            },
        }
        return templates.TemplateResponse("dashboard.html", context)

    @router.get("/rates/today")
    # pylint: disable=no-self-argument
    async def get_dashboard_rates(
        request: Request,
        search: Optional[str] = None,
        currency: Optional[str] = None,
        bank: Optional[str] = None,
        rate_type: Optional[str] = None,
        service: DashboardService = Depends(get_dashboard_service),
    ) -> List[DashboardTodayRateDTO]:
        """
        Get today's exchange rates with optional filtering
        """
        print(
            f"dashboard rates called: search: {search} currency: {currency} bank: {bank} rate_type: {rate_type}"
        )
        return service.get_today_rates(
            search=search, currency=currency, bank_code=bank, rate_type=rate_type
        )
