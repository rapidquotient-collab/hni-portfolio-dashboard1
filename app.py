import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO

st.set_page_config(page_title="HNI Portfolio Dashboard", layout="wide")
st.title("HNI Client Portfolio Dashboard")

# --- Excel Upload Feature ---
st.sidebar.markdown("### Upload Portfolio Excel")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls", "csv"])

# --- Data Loading ---
def load_portfolio_data():
    # Default mock data
    return {
        "Client A": pd.DataFrame({
            "Asset Class": ["Equity", "Debt", "Real Estate", "Gold"],
            "Value (INR Lakhs)": [120, 80, 50, 30],
        }),
        "Client B": pd.DataFrame({
            "Asset Class": ["Equity", "Debt", "Real Estate", "Gold"],
            "Value (INR Lakhs)": [200, 50, 40, 10],
        }),
        "Client C": pd.DataFrame({
            "Asset Class": ["Equity", "Debt", "Real Estate", "Gold"],
            "Value (INR Lakhs)": [150, 100, 60, 20],
        }),
    }

portfolio_data = load_portfolio_data()

# Always define clients and selected_client (default to first client)
clients = list(portfolio_data.keys())
selected_client = st.sidebar.selectbox("Select Client", clients)

# If Excel uploaded, override portfolio_data and update clients/selected_client
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith("csv"):
            df_uploaded = pd.read_csv(uploaded_file)
        else:
            df_uploaded = pd.read_excel(uploaded_file)
        # Assume file has columns: Client, Asset Class, Value (INR Lakhs)
        portfolio_data = {}
        for client in df_uploaded['Client'].unique():
            portfolio_data[client] = df_uploaded[df_uploaded['Client'] == client][['Asset Class', 'Value (INR Lakhs)']].reset_index(drop=True)
        clients = list(portfolio_data.keys())
        selected_client = st.sidebar.selectbox("Select Client", clients)
        st.success("Portfolio loaded from uploaded file!")
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")

# --- Financial API Integration (Stub) ---
def get_live_price(symbol):
    # Example with Alpha Vantage (add your API key)
    # api_key = 'YOUR_API_KEY'
    # url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    # response = requests.get(url)
    # data = response.json()
    # return float(data['Global Quote']['05. price'])
    return np.random.uniform(90, 110)  # Mocked price

# --- Real-Time Features (Manual Refresh) ---
if st.button("🔄 Refresh Data (Demo)"):
    st.rerun()

# --- AUM Summary for All Clients ---
aum = 0
for client_df in portfolio_data.values():
    aum += client_df["Value (INR Lakhs)"].sum()
st.markdown(f"### 💰 <span style='color:green'>Total AUM (All Clients):</span> ₹ {aum:,.2f} Lakhs", unsafe_allow_html=True)

# --- Enhanced Portfolio Dashboard ---

# 1. Client Profile Card
profile_info = {
    "Client A": {"Risk Profile": "Moderate", "Investment Horizon": "5 years", "Email": "clientA@email.com"},
    "Client B": {"Risk Profile": "Aggressive", "Investment Horizon": "10 years", "Email": "clientB@email.com"},
    "Client C": {"Risk Profile": "Conservative", "Investment Horizon": "3 years", "Email": "clientC@email.com"},
}
with st.container():
    st.subheader(f"👤 Client Profile: {selected_client}")
    cols = st.columns(3)
    cols[0].markdown(f"**Risk Profile:** {profile_info.get(selected_client, {}).get('Risk Profile', '-')}")
    cols[1].markdown(f"**Investment Horizon:** {profile_info.get(selected_client, {}).get('Investment Horizon', '-')}")
    cols[2].markdown(f"**Email:** {profile_info.get(selected_client, {}).get('Email', '-')}")

# 2. Portfolio Overview & Holdings Table
st.header(f"Portfolio Overview - {selected_client}")
df = portfolio_data[selected_client].copy()
total_value = df["Value (INR Lakhs)"].sum()
df["% Allocation"] = (df["Value (INR Lakhs)"] / total_value * 100).round(2)
df["Growth (YoY %)"] = np.random.uniform(-5, 18, size=len(df)).round(2)  # Mocked growth
st.dataframe(df.style.applymap(lambda v: 'color: green' if isinstance(v, float) and v > 0 else ('color: red' if isinstance(v, float) and v < 0 else ''), subset=["Growth (YoY %)"]), use_container_width=True)
st.metric("Total Portfolio Value (INR Lakhs)", f"₹ {total_value:,.2f}")

# --- Analytics Section ---
st.subheader("📊 Portfolio Analytics")
# Mocked monthly returns for analytics (replace with real data if available)
monthly_returns = np.random.normal(loc=1.2, scale=2.5, size=36) / 100  # 36 months
cagr = ((1 + monthly_returns).prod()) ** (12 / len(monthly_returns)) - 1
volatility = np.std(monthly_returns) * np.sqrt(12)
sharpe_ratio = (np.mean(monthly_returns) * 12) / (np.std(monthly_returns) * np.sqrt(12))
best_asset = df.loc[df["Growth (YoY %)"].idxmax(), "Asset Class"]
worst_asset = df.loc[df["Growth (YoY %)"].idxmin(), "Asset Class"]
colA, colB, colC, colD, colE = st.columns(5)
colA.metric("CAGR (3Y)", f"{cagr*100:.2f}%")
colB.metric("Volatility (Ann.)", f"{volatility*100:.2f}%")
colC.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
colD.metric("Best Asset", f"{best_asset}")
colE.metric("Worst Asset", f"{worst_asset}")

# Rolling returns chart
rolling_returns = pd.Series(monthly_returns).rolling(6).mean()
st.line_chart(rolling_returns, height=150, use_container_width=True)

# --- Real-Time Features Placeholders ---
with st.expander("Live News & Alerts (Demo)"):
    st.write("[Ticker] Nifty 50 up 0.8%, Sensex hits all-time high, RBI announces new policy...")
    st.warning("[Alert] Equity allocation exceeds 60% for Client B! Consider rebalancing.")

# 3. Asset Allocation Pie Chart
with st.expander("Asset Allocation", expanded=True):
    fig1, ax1 = plt.subplots()
    ax1.pie(df["Value (INR Lakhs)"], labels=df["Asset Class"], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

# 4. Customizable Date Range for Performance Chart
st.subheader("Portfolio Performance")
col1, col2 = st.columns(2)
def_months = 12
with col1:
    months_back = st.slider("Select months to view", 3, 36, def_months)
with col2:
    show_download = st.checkbox("Download Portfolio Report (Excel)")

months = pd.date_range(end=pd.Timestamp.today(), periods=months_back, freq='M')
performance = np.cumsum(np.random.normal(loc=1.5, scale=2, size=months_back)) + total_value - 10
performance_df = pd.DataFrame({"Month": months, "Portfolio Value": performance})
st.line_chart(performance_df.set_index("Month"))

# 5. Download Portfolio Report
if show_download:
    report_df = df.copy()
    report_df["Month"] = months[-1].strftime("%b %Y")
    st.download_button(
        label="Download Excel",
        data=report_df.to_csv(index=False),
        file_name=f"{selected_client}_portfolio_report.csv",
        mime="text/csv",
    )

# 6. Notes/Comments Section
st.markdown("---")
st.subheader("Advisor/Client Notes")
notes = st.text_area(f"Add notes for {selected_client}", "")
st.caption("(Notes are not saved in this demo. Integrate with a backend for persistence.)")

st.info("This is a demo dashboard. Replace mock data with real client data and integrate with backend systems for production use.")
