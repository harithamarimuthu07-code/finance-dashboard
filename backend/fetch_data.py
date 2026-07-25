import yfinance as yf

from database import SessionLocal, engine, Base
from models import Stock

Base.metadata.create_all(bind=engine)

db = SessionLocal()

tickers = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "ITC.NS",
    "LT.NS",
    "AXISBANK.NS",
    "KOTAKBANK.NS",
    "BHARTIARTL.NS",
    "HINDUNILVR.NS",
    "MARUTI.NS",
    "SUNPHARMA.NS",
    "TITAN.NS",
    "NTPC.NS",
    "WIPRO.NS",
    "BAJFINANCE.NS",
    "ASIANPAINT.NS",
    "ULTRACEMCO.NS"
]

for ticker in tickers:

    stock = yf.Ticker(ticker)
    info = stock.info

    existing = db.query(Stock).filter(
        Stock.ticker == ticker
    ).first()

    if existing:
        existing.price = info.get("currentPrice")
        existing.market_cap = info.get("marketCap")
        existing.pe_ratio = info.get("trailingPE")
        existing.eps = info.get("trailingEps")

    else:
        new_stock = Stock(
            ticker=ticker,
            company_name=info.get("longName"),
            price=info.get("currentPrice"),
            market_cap=info.get("marketCap"),
            pe_ratio=info.get("trailingPE"),
            eps=info.get("trailingEps")
        )

        db.add(new_stock)

db.commit()

print("Data saved successfully!")