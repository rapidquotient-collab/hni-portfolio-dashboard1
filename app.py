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
    cols[0].markdown(f"**Risk Profile:** {profile_info[selected_client]['Risk Profile']}")
    cols[1].markdown(f"**Investment Horizon:** {profile_info[selected_client]['Investment Horizon']}")
    cols[2].markdown(f"**Email:** {profile_info[selected_client]['Email']}")

# 2. Portfolio Overview & Holdings Table
st.header(f"Portfolio Overview - {selected_client}")
df = portfolio_data[selected_client].copy()
total_value = df["Value (INR Lakhs)"].sum()
df["% Allocation"] = (df["Value (INR Lakhs)"] / total_value * 100).round(2)
df["Growth (YoY %)"] = np.random.uniform(-5, 18, size=len(df)).round(2)  # Mocked growth
st.dataframe(df.style.applymap(lambda v: 'color: green' if isinstance(v, float) and v > 0 else ('color: red' if isinstance(v, float) and v < 0 else ''), subset=["Growth (YoY %)"]), use_container_width=True)
st.metric("Total Portfolio Value (INR Lakhs)", f"₹ {total_value:,.2f}")

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
