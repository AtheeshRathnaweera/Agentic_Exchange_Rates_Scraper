import uuid
from fastapi import Request

from agno.os import AgentOS
from agno.run.workflow import (
    WorkflowRunOutput,
)
from agno.utils.pprint import pprint_run_response

from agents import get_scraping_agent
from workflows import get_scrape_rates_workflow

OS_CONFIG_PATH = "configs/agent_os_config.yaml"

scraping_agent = get_scraping_agent(debug_mode=True)

# Configuration for the AgentOS
agent_os = AgentOS(
    os_id="lkexrates-os",
    agents=[scraping_agent],
    config=OS_CONFIG_PATH,
)
app = agent_os.get_app()


@app.post("/run-scraper")
async def run_scraper(request: Request):
    """
    Endpoint to trigger the exchange rates scraping workflow.
    """
    correlation_id = str(uuid.uuid4())
    body = await request.body()
    print(
        f"[run_scraper] Received request body: {body.decode('utf-8')} Using correlation_id: {correlation_id}"
    )
    try:
        response: WorkflowRunOutput = await get_scrape_rates_workflow(
            correlation_id=correlation_id
        ).arun()
        print("[run_scraper] Scraping workflow completed. Printing response:")
        pprint_run_response(response, markdown=True)
    except Exception as e:
        print(f"[run_scraper] ❌ Error occurred: {e}")
    finally:
        print("[run_scraper] Scraper run finished.")


if __name__ == "__main__":
    agent_os.serve(app="main:app", reload=True)
