from agno.os import AgentOS

from agents import get_scraping_agent
from app.api.controllers import ExchangeRatesController

OS_CONFIG_PATH = "configs/agent_os_config.yaml"

scraping_agent = get_scraping_agent(debug_mode=True)

# Configuration for the AgentOS
agent_os = AgentOS(
    os_id="lkexrates-os",
    agents=[scraping_agent],
    config=OS_CONFIG_PATH,
)
app = agent_os.get_app()

app.include_router(ExchangeRatesController.router)


if __name__ == "__main__":
    agent_os.serve(app="main:app", reload=True)
