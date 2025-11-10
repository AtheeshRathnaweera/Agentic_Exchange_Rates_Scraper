from agno.workflow import Step, Workflow

from workflows.scrape_rates.steps import (
    get_urls_step,
    extract_rates_step,
    save_to_db_step,
)

MAX_RETRIES = 3
RETRY_DELAY = 2


def get_scrape_rates_workflow(correlation_id: str) -> Workflow:
    """
    Constructs and returns the Scrape Rates Pipeline workflow.
    """
    print(
        f"[get_scrape_rates_workflow] Initializing workflow with correlation_id: {correlation_id}"
    )
    return Workflow(
        name="Scrape Rates Pipeline",
        steps=[
            Step(name="Get Urls Step", executor=get_urls_step),
            Step(name="Extract Rates Step", executor=extract_rates_step),
            Step(name="Save to DB Step", executor=save_to_db_step),
        ],
        metadata={"correlation_id": correlation_id},
    )
