from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.api.dependencies.services import get_dashboard_service
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
