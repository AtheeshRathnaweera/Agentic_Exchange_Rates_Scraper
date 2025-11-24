from enum import Enum


class ScraperJobStatus(str, Enum):
    """
    Enumeration representing the status of a scraper job.

    Attributes:
        SCHEDULED: The job is scheduled and waiting to start.
        RUNNING: The job is currently in progress.
        SUCCESS: The job completed successfully.
        ERROR: The job encountered an error during execution.
    """

    SCHEDULED = "scheduled"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
