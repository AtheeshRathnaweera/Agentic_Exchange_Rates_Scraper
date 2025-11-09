from agno.workflow import StepInput, StepOutput
import yaml

from app.models.scrape_target import ScrapeTarget

CONFIG_FILE_PATH = "configs/scrape_config.yaml"


def get_urls_step(step_input: StepInput) -> StepOutput:
    """
    Loads scraping target URLs from the configuration file and returns them as ScrapeTarget objects.
    """
    print("[get_urls_step] Loading scraping targets from config file...")
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    print(f"[get_urls_step] Loaded config: {CONFIG_FILE_PATH}")

    # Map dicts → ScrapeTarget objects
    targets = [ScrapeTarget(**item) for item in config["scrape_targets"]]
    print(f"[get_urls_step] Parsed {len(targets)} ScrapeTarget objects.")

    print(f"[get_urls_step] Scrape Rates: loaded {len(targets)} targets")
    return StepOutput(content=targets)
