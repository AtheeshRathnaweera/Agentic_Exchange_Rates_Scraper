from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Text

from db.models import Base


class RawExchangeRate(Base):
    """
    SQLAlchemy ORM model for the 'raw_exchange_rates' table.
    """

    __tablename__ = "raw_exchange_rates"

    id = Column(Integer, primary_key=True)
    bank_name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False, default="Sri Lanka")
    last_updated = Column(TIMESTAMP, nullable=False)
    source_url = Column(String(255))
    currency_name = Column(String(50), nullable=False)
    currency_code = Column(String(10), nullable=False)
    tt_buying = Column(Float)
    tt_selling = Column(Float)
    draft_buying = Column(Float)
    draft_selling = Column(Float)
    cheques_buying = Column(Float)
    cheques_selling = Column(Float)
    currency_buying = Column(Float)
    currency_selling = Column(Float)
    other_buying = Column(Float)
    other_selling = Column(Float)
    notes = Column(Text)
    tag = Column(String(50))
    created_date = Column(
        TIMESTAMP, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    correlation_id = Column(String(100))
