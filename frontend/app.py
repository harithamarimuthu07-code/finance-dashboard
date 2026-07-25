import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="📈",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"


# ==========================
# API FUNCTIONS
# ==========================

@st.cache_data(ttl=300)
def load_stocks():
    response = requests.get(f"{API_URL}/stocks")
    response.raise_for_status()
    return pd.DataFrame(response.json())


@st.cache_data(ttl=300)
def load_summary():
    response = requests.get(f"{API_URL}/market-summary")
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=300)
def load_history(ticker):
    response = requests.get(f"{API_URL}/history/{ticker}")
    response.raise_for_status()
    return pd.DataFrame(response.json())


# ==========================
# LOAD DATA
# ==========================

try:
    df = load_stocks()
    summary = load_summary()

except Exception:
    st.error("Cannot connect to FastAPI backend.")
    st.stop()

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("📊 Finance Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Comparison",
        "Data Table"
    ]
)

st.sidebar.markdown("---")

st.sidebar.write("Last Updated")

st.sidebar.success(
    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)

search = st.sidebar.text_input("🔍 Search Company")

if search:
    df = df[
        df["company_name"].str.contains(
            search,
            case=False
        )
    ]

sort = st.sidebar.selectbox(
    "Sort By",
    [
        "price",
        "market_cap",
        "pe_ratio",
        "eps"
    ]
)

ascending = st.sidebar.checkbox(
    "Ascending",
    value=False
)

df = df.sort_values(sort, ascending=ascending)

# ==========================
# DASHBOARD
# ==========================

if page == "Dashboard":

    st.title("📈 Indian Stock Market Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Tracked Companies",
        summary["total_companies"]
    )

    c2.metric(
        "Average PE",
        summary["average_pe"]
    )

    c3.metric(
        "Highest Market Cap",
        summary["highest_market_cap"]
    )

    st.divider()

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Highest Price",
        f"₹{df['price'].max():,.2f}"
    )

    k2.metric(
        "Lowest Price",
        f"₹{df['price'].min():,.2f}"
    )

    k3.metric(
        "Average EPS",
        round(df["eps"].mean(), 2)
    )

    k4.metric(
        "Average Market Cap",
        f"₹{df['market_cap'].mean():,.0f}"
    )

    st.divider()

    company = st.selectbox(
        "Select Company",
        df["ticker"]
    )

    selected = df[df["ticker"] == company].iloc[0]

    st.subheader(selected["company_name"])

    col1, col2 = st.columns(2)

    col1.metric(
        "Current Price",
        f"₹{selected['price']:,.2f}"
    )

    col2.metric(
        "Market Cap",
        f"₹{selected['market_cap']:,.0f}"
    )

    col1.metric(
        "P/E Ratio",
        round(selected["pe_ratio"], 2)
    )

    col2.metric(
        "EPS",
        round(selected["eps"], 2)
    )

    st.divider()

    history = load_history(company)

    if not history.empty:

        history["Date"] = pd.to_datetime(history["Date"])

        st.subheader("📉 Candlestick Chart")

        fig = go.Figure()

        fig.add_trace(
            go.Candlestick(
                x=history["Date"],
                open=history["Open"],
                high=history["High"],
                low=history["Low"],
                close=history["Close"]
            )
        )

        fig.update_layout(
            height=600,
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("📊 Trading Volume")

        volume = px.bar(
            history,
            x="Date",
            y="Volume"
        )

        st.plotly_chart(
            volume,
            use_container_width=True
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Market Cap Distribution")

        pie = px.pie(
            df.head(10),
            names="ticker",
            values="market_cap"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    with right:

        st.subheader("PE Ratio vs EPS")

        scatter = px.scatter(
            df,
            x="pe_ratio",
            y="eps",
            size="market_cap",
            hover_name="company_name",
            color="price"
        )

        st.plotly_chart(
            scatter,
            use_container_width=True
        )

# ==========================
# COMPARISON
# ==========================

elif page == "Comparison":

    st.title("⚖ Company Comparison")

    companies = st.multiselect(
        "Select Companies",
        df["ticker"]
    )

    if companies:

        compare = df[
            df["ticker"].isin(companies)
        ]

        st.dataframe(
            compare,
            use_container_width=True
        )

        fig = px.bar(
            compare,
            x="ticker",
            y="market_cap",
            color="ticker",
            title="Market Capitalization"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig = px.bar(
            compare,
            x="ticker",
            y="price",
            color="ticker",
            title="Current Price"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig = px.bar(
            compare,
            x="ticker",
            y="pe_ratio",
            color="ticker",
            title="PE Ratio"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig = px.bar(
            compare,
            x="ticker",
            y="eps",
            color="ticker",
            title="EPS"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==========================
# DATA TABLE
# ==========================

elif page == "Data Table":

    st.title("📋 Stock Database")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top 5 Market Cap")

        st.dataframe(
            df.nlargest(
                5,
                "market_cap"
            ),
            use_container_width=True
        )

    with col2:

        st.subheader("Top 5 EPS")

        st.dataframe(
            df.nlargest(
                5,
                "eps"
            ),
            use_container_width=True
        )

    st.subheader("Lowest PE Ratio")

    st.dataframe(
        df.nsmallest(
            5,
            "pe_ratio"
        ),
        use_container_width=True
    )

    csv = df.to_csv(index=False)

    st.download_button(
        "⬇ Download CSV",
        csv,
        file_name="stocks.csv",
        mime="text/csv"
    )

    with st.expander("Raw API Response"):

        st.json(df.to_dict("records"))

st.markdown("---")

st.caption(
    "📊 Finance Dashboard | FastAPI • SQLite • Streamlit • Plotly • yFinance"
)