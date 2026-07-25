# 📈 Indian Stock Market Dashboard

This project is a simple finance dashboard that tracks 20+ Indian listed companies. It fetches live stock data using **yFinance**, stores it in a **SQLite** database, provides **FastAPI** endpoints, and displays everything through an interactive **Streamlit** dashboard.

## Features

- Track 20+ Indian companies
- Live stock prices and fundamental metrics
- Historical price charts
- Company comparison
- Market summary
- Search and sort companies
- Download stock data as CSV

## Tech Stack

- Python
- FastAPI
- Streamlit
- SQLite
- SQLAlchemy
- yFinance
- Plotly
- Pandas

## Project Structure

```
finance-dashboard/
│
├── backend/
├── frontend/
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
cd backend
uvicorn main:app --reload
```

Start the frontend:

```bash
cd frontend
streamlit run app.py
```

## API Endpoints

- `/stocks` – Get all stocks
- `/stocks/{ticker}` – Get a specific stock
- `/market-summary` – Market overview
- `/history/{ticker}` – Historical stock prices

## Future Improvements

- Candlestick charts
- Portfolio tracker
- User login
- Sector-wise analysis
- AI-powered insights

