import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Financial & Forensic Dashboard", layout="wide")

st.title("📊 Financial & Forensic Analysis Dashboard")

# --------------------------------------------------
# LOAD EXCEL
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("fsafadashboard2ndtry.xlsx", header=None)

df = load_data()

# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------
def extract_table(start_row, end_row):
    """
    Extracts table safely using row numbers.
    First row is assumed to be header.
    """
    table = df.iloc[start_row:end_row].copy()
    table.columns = table.iloc[0]
    table = table[1:]
    table.reset_index(drop=True, inplace=True)
    return table


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.header("Select Company")
st.sidebar.selectbox("Company", ["Maruti Suzuki"])

# --------------------------------------------------
# DASHBOARD LAYOUT
# --------------------------------------------------

st.subheader("📌 Company Snapshot")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏢 Company Snapshot")
    snapshot = extract_table(1, 6)   # rows 2–6
    st.dataframe(snapshot, use_container_width=True)

with col2:
    st.markdown("### 🔍 DuPont Analysis")
    dupont = extract_table(7, 13)   # rows 8–14
    st.dataframe(dupont, use_container_width=True)

# --------------------------------------------------

st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 💧 Liquidity Analysis")
    liquidity = extract_table(15, 18)   # rows 16–18
    st.dataframe(liquidity, use_container_width=True)

with col4:
    st.markdown("### ⚙️ Efficiency Analysis")
    efficiency = extract_table(19, 23)  # rows 20–24
    st.dataframe(efficiency, use_container_width=True)

# --------------------------------------------------

st.markdown("---")
st.subheader("🕵️ Forensic Analysis")

col5, col6 = st.columns(2)

with col5:
    st.markdown("### Accruals")
    accruals = extract_table(25, 27)   # rows 26–27
    st.dataframe(accruals, use_container_width=True)

with col6:
    st.markdown("### Scores (M, Z, F)")
    scores = extract_table(28, 32)     # rows 29–32
    st.dataframe(scores, use_container_width=True)

# --------------------------------------------------
st.markdown("---")
st.caption("✅ Clean Excel • Stable Layout • Production Ready")
