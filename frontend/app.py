import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Indian Stock Dashboard", layout="wide")

API_URL = "http://127.0.0.1:8000"

# ---------------- Sidebar ---------------- #

st.sidebar.title("📊 Finance Dashboard")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Comparison", "Data Table"]
)

st.sidebar.markdown("---")
st.sidebar.write("Last Updated")
st.sidebar.info(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

# ---------------- Fetch Data ---------------- #

response = requests.get(f"{API_URL}/stocks")

if response.status_code != 200:
    st.error("Unable to connect to backend.")
    st.stop()

data = response.json()
df = pd.DataFrame(data)

# ---------------- Search ---------------- #

search = st.sidebar.text_input("🔍 Search Company")

if search:
    df = df[df["company_name"].str.contains(search, case=False)]

# ---------------- Sorting ---------------- #

sort_option = st.sidebar.selectbox(
    "Sort By",
    ["price", "market_cap", "pe_ratio", "eps"]
)

ascending = st.sidebar.checkbox("Ascending Order")

df = df.sort_values(sort_option, ascending=ascending)

# ================= DASHBOARD ================= #

if page == "Dashboard":

    st.title("📈 Indian Stock Market Dashboard")

    summary = requests.get(f"{API_URL}/market-summary").json()

    c1, c2, c3 = st.columns(3)

    c1.metric("Companies", summary["total_companies"])
    c2.metric("Average PE", round(summary["average_pe"],2))
    c3.metric("Highest Market Cap", summary["highest_market_cap"])

    st.divider()

    # ---------------- KPI Cards ---------------- #

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Highest Price", f"₹{df['price'].max():,.2f}")
    k2.metric("Lowest Price", f"₹{df['price'].min():,.2f}")
    k3.metric("Average EPS", round(df["eps"].mean(),2))
    k4.metric("Average PE", round(df["pe_ratio"].mean(),2))

    st.divider()

    company = st.selectbox(
        "Select Company",
        df["ticker"]
    )

    selected = df[df["ticker"] == company]

    st.subheader("🏢 Company Details")

    col1, col2 = st.columns(2)

    col1.metric(
        "Current Price",
        f"₹{selected.iloc[0]['price']:.2f}"
    )

    col2.metric(
        "P/E Ratio",
        f"{selected.iloc[0]['pe_ratio']:.2f}"
    )

    col1.metric(
        "EPS",
        f"{selected.iloc[0]['eps']:.2f}"
    )

    col2.metric(
        "Market Cap",
        f"₹{selected.iloc[0]['market_cap']:,}"
    )

    st.divider()

    st.subheader("📈 Historical Price")

    history = requests.get(
        f"{API_URL}/history/{company}"
    ).json()

    history_df = pd.DataFrame(history)

    fig = px.line(
        history_df,
        x="Date",
        y="Close",
        title=f"{company} Price History"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🥧 Market Cap Distribution")

    pie = px.pie(
        df.head(10),
        names="ticker",
        values="market_cap"
    )

    st.plotly_chart(pie, use_container_width=True)

    st.divider()

    st.subheader("📊 PE Ratio vs EPS")

    scatter = px.scatter(
        df,
        x="pe_ratio",
        y="eps",
        size="market_cap",
        hover_name="company_name"
    )

    st.plotly_chart(scatter, use_container_width=True)

# ================= COMPARISON ================= #

elif page == "Comparison":

    st.title("⚖ Company Comparison")

    companies = st.multiselect(
        "Choose Companies",
        df["ticker"]
    )

    if companies:

        compare_df = df[df["ticker"].isin(companies)]

        st.dataframe(compare_df)

        fig = px.bar(
            compare_df,
            x="ticker",
            y="market_cap",
            color="ticker",
            title="Market Capitalization"
        )

        st.plotly_chart(fig, use_container_width=True)

        fig = px.bar(
            compare_df,
            x="ticker",
            y="pe_ratio",
            color="ticker",
            title="P/E Ratio Comparison"
        )

        st.plotly_chart(fig, use_container_width=True)

        fig = px.bar(
            compare_df,
            x="ticker",
            y="eps",
            color="ticker",
            title="EPS Comparison"
        )

        st.plotly_chart(fig, use_container_width=True)

# ================= DATA TABLE ================= #

elif page == "Data Table":

    st.title("📋 Complete Stock Data")

    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("🏆 Top 5 Companies by Market Cap")

    top5 = df.nlargest(5, "market_cap")

    st.dataframe(top5)

    st.subheader("📉 Lowest PE Stocks")

    lowest = df.nsmallest(5, "pe_ratio")

    st.dataframe(lowest)

    st.subheader("💰 Highest EPS Stocks")

    highest = df.nlargest(5, "eps")

    st.dataframe(highest)

    st.divider()

    csv = df.to_csv(index=False)

    st.download_button(
        "⬇ Download CSV",
        csv,
        "stocks.csv",
        "text/csv"
    )

    with st.expander("View API Response"):
        st.json(data)

st.markdown("---")
st.caption(
    "📊 Finance Dashboard | Built with FastAPI • SQLite • Streamlit • Plotly • yFinance"
)