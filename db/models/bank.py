from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP

from db.models.base import Base


class Bank(Base):
    """
    SQLAlchemy ORM model for the 'bank' table.
    """

    __tablename__ = "bank"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False, default="Sri Lanka")
    rates_url = Column(String(255), nullable=False)
    logo_url = Column(String(255), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    scraper_type = Column(
        String(20), nullable=False
    )  # html | api | pdf
    created_date = Column(
        TIMESTAMP,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
