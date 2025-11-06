from pathlib import Path
from fastapi import Request

from agno.os import AgentOS
from agno.run.workflow import (
    WorkflowRunOutput,
)
from agno.utils.pprint import pprint_run_response
from agents.core_agent import get_core_agent

from workflows import get_scrape_rates_workflow

OS_CONFIG_PATH = str(Path(__file__).parent.joinpath("config.yaml"))

# web_agent = get_web_agent(model_id="gpt-5")
# agno_assist = get_agno_assist(model_id="gpt-5")
core_agent = get_core_agent(model_id="llama-3.1-8b-instant")
# scrape_rates_workflow = scrape_rates.workflow.get_scrape_rates_workflow()

# Create the AgentOS
agent_os = AgentOS(
    os_id="agentos-demo",
    # agents=[web_agent, agno_assist],
    agents=[core_agent],
    # Configuration for the AgentOS
    config=OS_CONFIG_PATH,
)
app = agent_os.get_app()


@app.post("/run-scraper")
async def run_scraper(request: Request):
    body = await request.body()
    print(f"Main: run scraper started: {body.decode('utf-8')}")
    try:
        response: WorkflowRunOutput = await get_scrape_rates_workflow().arun(
            input="Test Input",
        )
        pprint_run_response(response, markdown=True)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("Main: run scraper completed")


if __name__ == "__main__":
    # Add knowledge to Agno Assist agent
    # asyncio.run(
    #     agno_assist.knowledge.add_content_async(  # type: ignore
    #         name="Agno Docs",
    #         url="https://docs.agno.com/llms-full.txt",
    #     )
    # )
    # Simple run to generate and record a session
    agent_os.serve(app="main:app", reload=True)
