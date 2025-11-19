from agno.workflow import Step, Workflow

from workflows.scrape_rates.steps import (
    get_urls_step,
    extract_rates_step,
    save_to_db_step,
)
from workflows.utils import wrap_executor


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
            Step(
                name="Get Urls Step",
                executor=wrap_executor(get_urls_step),
                max_retries=3,
                skip_on_failure=False,
            ),
            Step(
                name="Extract Rates Step",
                executor=wrap_executor(extract_rates_step),
                max_retries=0,
                skip_on_failure=False,
            ),
            Step(
                name="Save to DB Step",
                executor=wrap_executor(save_to_db_step),
                max_retries=0,
                skip_on_failure=False,
            ),
        ],
        metadata={"correlation_id": correlation_id},
    )
