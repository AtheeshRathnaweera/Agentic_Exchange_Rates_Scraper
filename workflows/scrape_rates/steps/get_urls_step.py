from pathlib import Path
from agno.workflow import StepInput, StepOutput
import yaml

from app.models.scrape_target import ScrapeTarget
from utils import get_logger

logger = get_logger(__name__)
CONFIG_FILE_PATH = "configs/scrape_config.yaml"


def get_urls_step(step_input: StepInput) -> StepOutput:
    """
    Loads scraping target URLs from the configuration file and returns them as ScrapeTarget objects.
    """
    logger.info("Loading scraping targets from config file...")

    try:
        # Validate config file exists
        config_path = Path(CONFIG_FILE_PATH)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE_PATH}")

        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        logger.info("Loaded config: %s", CONFIG_FILE_PATH)

        # Map dicts → ScrapeTarget objects
        targets = [ScrapeTarget(**item) for item in config["scrape_targets"]]
        logger.info("Parsed %s ScrapeTarget objects.", len(targets))

        return StepOutput(content=targets)
    except FileNotFoundError:
        logger.error(
            ("Configuration file not found: %s", CONFIG_FILE_PATH),
            exc_info=True,
        )
        return StepOutput(
            content=f"Configuration file not found: {CONFIG_FILE_PATH}", stop=True
        )
    except Exception as e:
        logger.error(
            ("Failed to load scraping targets: %s", str(e)),
            exc_info=True,
        )
        return StepOutput(
            content=f"Failed to load scraping targets: {str(e)}", stop=True
        )
