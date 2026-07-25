from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import yfinance as yf

from database import engine, Base, get_db
from models import Stock
from schemas import StockResponse

app = FastAPI(
    title="Finance Dashboard API",
    version="1.0.0",
    description="Stock Market Dashboard API built with FastAPI"
)

# Create tables
Base.metadata.create_all(bind=engine)


# ==========================
# HOME
# ==========================

@app.get("/")
def home():
    return {
        "message": "Finance Dashboard API Running",
        "status": "success"
    }


# ==========================
# GET ALL STOCKS
# ==========================

@app.get("/stocks", response_model=list[StockResponse])
def get_stocks(db: Session = Depends(get_db)):

    stocks = db.query(Stock).all()

    return stocks


# ==========================
# GET SINGLE STOCK
# ==========================

@app.get("/stocks/{ticker}", response_model=StockResponse)
def get_stock(
    ticker: str,
    db: Session = Depends(get_db)
):

    stock = (
        db.query(Stock)
        .filter(Stock.ticker == ticker.upper())
        .first()
    )

    if stock is None:
        raise HTTPException(
            status_code=404,
            detail="Stock not found"
        )

    return stock


# ==========================
# MARKET SUMMARY
# ==========================

@app.get("/market-summary")
def market_summary(db: Session = Depends(get_db)):

    stocks = db.query(Stock).all()

    if len(stocks) == 0:
        raise HTTPException(
            status_code=404,
            detail="No stock data available"
        )

    total_companies = len(stocks)

    average_pe = round(
        sum(stock.pe_ratio or 0 for stock in stocks)
        / total_companies,
        2
    )

    average_eps = round(
        sum(stock.eps or 0 for stock in stocks)
        / total_companies,
        2
    )

    highest_market_cap = max(
        stocks,
        key=lambda x: x.market_cap or 0
    )

    highest_price = max(
        stocks,
        key=lambda x: x.price or 0
    )

    lowest_price = min(
        stocks,
        key=lambda x: x.price or 0
    )

    return {

        "total_companies": total_companies,

        "average_pe": average_pe,

        "average_eps": average_eps,

        "highest_market_cap":
            highest_market_cap.company_name,

        "highest_market_cap_value":
            highest_market_cap.market_cap,

        "highest_price":
            highest_price.company_name,

        "highest_price_value":
            highest_price.price,

        "lowest_price":
            lowest_price.company_name,

        "lowest_price_value":
            lowest_price.price
    }


# ==========================
# HISTORICAL DATA
# ==========================

@app.get("/history/{ticker}")
def get_history(ticker: str):

    try:

        stock = yf.Ticker(f"{ticker.upper()}.NS")

        history = stock.history(period="1y")

        if history.empty:

            raise HTTPException(
                status_code=404,
                detail="Historical data not found"
            )

        history.reset_index(inplace=True)

        history["Date"] = (
            history["Date"]
            .dt.strftime("%Y-%m-%d")
        )

        return history[
            [
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ]
        ].to_dict(orient="records")

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================
# HEALTH CHECK
# ==========================

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "service": "Finance Dashboard API"

    }