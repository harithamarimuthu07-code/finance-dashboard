import yfinance as yf

from database import SessionLocal, engine, Base
from models import Stock


# Create tables if not created
Base.metadata.create_all(bind=engine)


# ==========================
# INDIAN STOCK LIST
# ==========================

companies = {

    "RELIANCE.NS": "Reliance Industries",

    "TCS.NS": "Tata Consultancy Services",

    "INFY.NS": "Infosys",

    "HDFCBANK.NS": "HDFC Bank",

    "ICICIBANK.NS": "ICICI Bank",

    "SBIN.NS": "State Bank of India",

    "BHARTIARTL.NS": "Bharti Airtel",

    "ITC.NS": "ITC Limited",

    "LT.NS": "Larsen & Toubro",

    "HINDUNILVR.NS": "Hindustan Unilever",

    "AXISBANK.NS": "Axis Bank",

    "KOTAKBANK.NS": "Kotak Mahindra Bank",

    "WIPRO.NS": "Wipro",

    "HCLTECH.NS": "HCL Technologies",

    "MARUTI.NS": "Maruti Suzuki",

    "TITAN.NS": "Titan Company",

    "SUNPHARMA.NS": "Sun Pharmaceutical",

    "ASIANPAINT.NS": "Asian Paints",

    "BAJFINANCE.NS": "Bajaj Finance",

    "NTPC.NS": "NTPC"

}


# ==========================
# FETCH DATA
# ==========================


def fetch_stock_data():

    db = SessionLocal()

    try:

        for ticker, company_name in companies.items():

            print(f"Fetching {ticker}")

            try:

                stock = yf.Ticker(ticker)

                info = stock.info


                # Current price

                price = (
                    info.get("currentPrice")
                    or info.get("regularMarketPrice")
                    or 0
                )


                market_cap = (
                    info.get("marketCap")
                    or 0
                )


                pe_ratio = (
                    info.get("trailingPE")
                    or 0
                )


                eps = (
                    info.get("trailingEps")
                    or 0
                )


                sector = (
                    info.get("sector")
                    or "Unknown"
                )


                # Recent history

                history = stock.history(
                    period="5d"
                )


                if not history.empty:

                    latest = history.iloc[-1]

                    open_price = float(
                        latest["Open"]
                    )

                    high = float(
                        latest["High"]
                    )

                    low = float(
                        latest["Low"]
                    )

                    close = float(
                        latest["Close"]
                    )

                    volume = float(
                        latest["Volume"]
                    )

                else:

                    open_price = 0
                    high = 0
                    low = 0
                    close = 0
                    volume = 0



                ticker_name = ticker.replace(
                    ".NS",
                    ""
                )


                # Check existing stock

                existing = (
                    db.query(Stock)
                    .filter(
                        Stock.ticker == ticker_name
                    )
                    .first()
                )


                if existing:


                    existing.price = price
                    existing.market_cap = market_cap
                    existing.pe_ratio = pe_ratio
                    existing.eps = eps
                    existing.sector = sector
                    existing.volume = volume
                    existing.open = open_price
                    existing.high = high
                    existing.low = low
                    existing.close = close


                else:


                    new_stock = Stock(

                        ticker=ticker_name,

                        company_name=company_name,

                        sector=sector,

                        price=price,

                        market_cap=market_cap,

                        pe_ratio=pe_ratio,

                        eps=eps,

                        volume=volume,

                        open=open_price,

                        high=high,

                        low=low,

                        close=close

                    )


                    db.add(new_stock)


                db.commit()

                print(
                    f"{ticker} saved successfully"
                )


            except Exception as e:

                print(
                    f"Error fetching {ticker}: {e}"
                )


    finally:

        db.close()



# ==========================
# RUN SCRIPT
# ==========================

if __name__ == "__main__":

    fetch_stock_data()

    print(
        "Stock database updated successfully"
    )