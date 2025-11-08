from agno.workflow import Step, Workflow

from workflows.scrape_rates.steps import get_urls_step, extract_rates_step

MAX_RETRIES = 3
RETRY_DELAY = 2


def get_scrape_rates_workflow() -> Workflow:
    return Workflow(
        name="Scrape Rates Pipeline",
        steps=[
            Step(name="Get Urls Step", executor=get_urls_step),
            Step(name="Main Step", executor=extract_rates_step),
        ],
    )
