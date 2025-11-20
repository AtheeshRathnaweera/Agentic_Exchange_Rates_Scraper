from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from agno.os import AgentOS

from agents import get_scraping_agent
from app.api.controllers import ExchangeRatesController, DashboardController
from utils import build_openapi

OS_CONFIG_PATH = "configs/agent_os_config.yaml"

scraping_agent = get_scraping_agent(debug_mode=True)

# Configuration for the AgentOS
agent_os = AgentOS(
    os_id="lkexrates-os",
    agents=[scraping_agent],
    config=OS_CONFIG_PATH,
)

# Public-facing API
app = FastAPI(
    title="Exchange API",
    version="1.0.0",
    description="Handles exchange rate scraping and retrieval",
)

# Public routes
app.include_router(ExchangeRatesController.router)
app.include_router(DashboardController.router)

# Mount Agno’s internal OS separately
app.mount("/agentOS", agent_os.get_app())
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# API docs -> http://localhost:8000/docs#
# AgentOS docs -> http://localhost:8000/agentOS/docs#
build_openapi(app, allowed_prefixes="*")
