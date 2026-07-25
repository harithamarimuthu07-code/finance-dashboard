from sqlalchemy import Column, Integer, String, Float
from database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    ticker = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    company_name = Column(
        String,
        nullable=False
    )

    sector = Column(
        String,
        nullable=True
    )

    price = Column(
        Float,
        nullable=False
    )

    market_cap = Column(
        Float,
        nullable=True
    )

    pe_ratio = Column(
        Float,
        nullable=True
    )

    eps = Column(
        Float,
        nullable=True
    )

    volume = Column(
        Float,
        nullable=True
    )

    high = Column(
        Float,
        nullable=True
    )

    low = Column(
        Float,
        nullable=True
    )

    open = Column(
        Float,
        nullable=True
    )

    close = Column(
        Float,
        nullable=True
    )

    def __repr__(self):
        return (
            f"<Stock("
            f"{self.ticker}, "
            f"{self.company_name}, "
            f"₹{self.price}"
            f")>"
        )