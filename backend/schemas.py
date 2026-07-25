from pydantic import BaseModel
from typing import Optional


class StockResponse(BaseModel):
    ticker: str
    company_name: str
    sector: Optional[str] = None
    price: float
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    eps: Optional[float] = None
    volume: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    close: Optional[float] = None

    class Config:
        from_attributes = True


class MarketSummary(BaseModel):
    total_companies: int
    average_pe: float
    average_eps: float
    highest_market_cap: str
    highest_market_cap_value: float
    highest_price: str
    highest_price_value: float
    lowest_price: str
    lowest_price_value: float