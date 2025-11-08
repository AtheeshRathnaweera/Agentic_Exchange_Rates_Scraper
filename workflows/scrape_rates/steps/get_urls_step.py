from agno.workflow import StepOutput
import yaml

from app.models.scrape_target import ScrapeTarget

CONFIG_FILE_PATH = "configs/scrape_config.yaml"


def get_urls_step() -> StepOutput:
    """
    Loads scraping target URLs from the configuration file and returns them as ScrapeTarget objects.
    """

    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Map dicts → ScrapeTarget objects
    targets = [ScrapeTarget(**item) for item in config["scrape_targets"]]

    print(f"Scrape Rates: loaded {len(targets)} targets")
    return StepOutput(content=targets)
