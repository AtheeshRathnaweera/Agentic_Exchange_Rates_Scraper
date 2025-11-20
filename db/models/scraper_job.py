from sqlalchemy import Column, Integer, String, TIMESTAMP, Text

from app.models.scraper_job_status import ScraperJobStatus
from db.models.base import Base


class ScraperJob(Base):
    """
    SQLAlchemy ORM model for the 'scraper_jobs' table.
    """

    __tablename__ = "scraper_jobs"

    id = Column(Integer, primary_key=True)
    correlation_id = Column(String(100), nullable=False, unique=True)
    started_at = Column(TIMESTAMP, nullable=True)
    finished_at = Column(TIMESTAMP, nullable=True)
    status = Column(
        String(20), nullable=False, default=ScraperJobStatus.SCHEDULED
    )  # scheduled | running | success | error
    message = Column(Text, nullable=True)
