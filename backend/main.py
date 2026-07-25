from fastapi import FastAPI
from database import SessionLocal, engine, Base
from models import Stock

app = FastAPI(title="Finance Dashboard API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Finance Dashboard API Running"}

@app.get("/stocks")
def get_stocks():
    db = SessionLocal()

    stocks = db.query(Stock).all()

    result = []

    for stock in stocks:
        result.append({
            "ticker": stock.ticker,
            "company_name": stock.company_name,
            "price": stock.price,
            "market_cap": stock.market_cap,
            "pe_ratio": stock.pe_ratio,
            "eps": stock.eps
        })

    return result
@app.get("/stocks/{ticker}")
def get_stock(ticker: str):
    db = SessionLocal()

    stock = db.query(Stock).filter(Stock.ticker == ticker).first()

    if stock is None:
        return {"error": "Stock not found"}

    return {
        "ticker": stock.ticker,
        "company_name": stock.company_name,
        "price": stock.price,
        "market_cap": stock.market_cap,
        "pe_ratio": stock.pe_ratio,
        "eps": stock.eps
    }
@app.get("/market-summary")
def market_summary():
    db = SessionLocal()

    stocks = db.query(Stock).all()

    if not stocks:
        return {"message": "No data available"}

    total_companies = len(stocks)

    average_pe = sum(stock.pe_ratio or 0 for stock in stocks) / total_companies

    highest_market_cap = max(stocks, key=lambda s: s.market_cap or 0)

    lowest_price = min(stocks, key=lambda s: s.price or 0)

    return {
        "total_companies": total_companies,
        "average_pe": round(average_pe, 2),
        "highest_market_cap": highest_market_cap.company_name,
        "lowest_price": lowest_price.company_name
    }
@app.get("/history/{ticker}")
def get_history(ticker: str):
    import yfinance as yf

    stock = yf.Ticker(ticker)

    history = stock.history(period="1y")

    history.reset_index(inplace=True)

    return history.to_dict(orient="records")