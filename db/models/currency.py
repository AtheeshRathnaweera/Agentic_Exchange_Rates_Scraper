from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP

from db.models.base import Base


class Currency(Base):
    """
    SQLAlchemy ORM model for the 'currency' table.
    """

    __tablename__ = "currency"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    symbol = Column(
        String(10),
        nullable=False,
    )
    name = Column(String(100), nullable=False)
    country = Column(
        String(50),
        nullable=False,
    )
    active = Column(Boolean, nullable=False, default=True)
    created_date = Column(
        TIMESTAMP,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
