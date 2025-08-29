import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="HNI Portfolio Dashboard", layout="wide")
st.title("HNI Client Portfolio Dashboard")

# Sidebar for client selection and filters
clients = ["Client A", "Client B", "Client C"]
selected_client = st.sidebar.selectbox("Select Client", clients)

# Mock portfolio data (replace with real data integration as needed)
portfolio_data = {
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

# Portfolio Overview
st.header(f"Portfolio Overview - {selected_client}")
df = portfolio_data[selected_client]
st.dataframe(df, use_container_width=True)

total_value = df["Value (INR Lakhs)"].sum()
st.metric("Total Portfolio Value (INR Lakhs)", f"₹ {total_value:,.2f}")

# Asset Allocation Pie Chart
st.subheader("Asset Allocation")
fig1, ax1 = plt.subplots()
ax1.pie(df["Value (INR Lakhs)"], labels=df["Asset Class"], autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Portfolio Performance (Mocked)
st.subheader("Portfolio Performance (Last 12 Months)")
months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='M')
performance = np.cumsum(np.random.normal(loc=1.5, scale=2, size=12)) + total_value - 10
performance_df = pd.DataFrame({"Month": months, "Portfolio Value": performance})
st.line_chart(performance_df.set_index("Month"))

st.info("This is a demo dashboard. Replace mock data with real client data and integrate with backend systems for production use.")
