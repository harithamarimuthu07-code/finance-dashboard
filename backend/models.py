from sqlalchemy import Column, Integer, String, Float
from database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    company_name = Column(String)
    price = Column(Float)
    market_cap = Column(Float)
    pe_ratio = Column(Float)
    eps = Column(Float)