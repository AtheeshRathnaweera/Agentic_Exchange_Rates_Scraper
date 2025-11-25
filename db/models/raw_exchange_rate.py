from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Text

from db.models.base import Base


class RawExchangeRate(Base):
    """
    SQLAlchemy ORM model for the 'raw_exchange_rates' table.
    """

    __tablename__ = "raw_exchange_rates"

    id = Column(Integer, primary_key=True)
    bank_name = Column(String(100), nullable=False, index=True)
    country = Column(String(50), nullable=False, default="Sri Lanka")
    last_updated = Column(TIMESTAMP, nullable=False)
    source_url = Column(String(255))
    currency_name = Column(String(50), nullable=False, index=True)
    currency_code = Column(String(10), nullable=False, index=True)
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
    tag = Column(String(50), nullable=False, index=True)
    created_date = Column(
        TIMESTAMP,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    correlation_id = Column(String(100), nullable=False)

    def __str__(self):
        return (
            f"RawExchangeRate(id={self.id}, bank_name='{self.bank_name}', "
            f"currency_code='{self.currency_code}', tt_buying={self.tt_buying}, "
            f"tt_selling={self.tt_selling}, created_date={self.created_date})"
        )
