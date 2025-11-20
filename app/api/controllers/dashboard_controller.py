from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")


class DashboardController:
    router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

    @router.get("/")
    # pylint: disable=no-self-argument
    async def run_scraper(request: Request, type: str = None):
        # data = await get_scraped_data(filter_type=type)
        data = {}
        return templates.TemplateResponse(
            "dashboard.html", {"request": request, "data": data}
        )
