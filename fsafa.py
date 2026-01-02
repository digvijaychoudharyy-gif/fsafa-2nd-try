import streamlit as st
import pandas as pd

st.set_page_config(page_title="Financial & Forensic Dashboard", layout="wide")
st.title("📊 Financial & Forensic Analysis Dashboard")

# -------------------------------
# LOAD EXCEL
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("fsafadashboard2ndtry.xlsx", sheet_name="Maruti Suzuki", header=None)

df = load_data()

# -------------------------------
# SAFE TABLE EXTRACTOR
# -------------------------------
def extract_table(df, start_row, end_row, start_col=1):
    table = df.iloc[start_row:end_row, start_col:]
    table = table.reset_index(drop=True)
    table.columns = [f"Col_{i+1}" for i in range(len(table.columns))]
    return table.astype(str)  # force safe rendering

def show_table(df):
    st.markdown(df.to_html(index=False), unsafe_allow_html=True)

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("Select Company")
st.sidebar.selectbox("Company", ["Maruti Suzuki"])

# -------------------------------
# DASHBOARD LAYOUT
# -------------------------------
st.subheader("📌 Company Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏢 Company Snapshot")
    show_table(extract_table(df, 2, 8))

with col2:
    st.markdown("### 🔍 DuPont Analysis")
    show_table(extract_table(df, 18, 24))

# -------------------------------
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.markdown("### ⚙️ Efficiency Ratios")
    show_table(extract_table(df, 26, 32))

with col4:
    st.markdown("### 💧 Liquidity Analysis")
    show_table(extract_table(df, 34, 40))

# -------------------------------
st.markdown("---")
st.subheader("🕵️ Forensic Analysis")

col5, col6 = st.columns(2)

with col5:
    st.markdown("### Accruals")
    show_table(extract_table(df, 42, 48))

with col6:
    st.markdown("### M-Score | Z-Score | F-Score")
    show_table(extract_table(df, 50, 58))

st.markdown("---")
st.caption("✅ Stable • No Arrow Errors • Production Safe")
