import streamlit as st
import pandas as pd

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Financial & Forensic Dashboard",
    layout="wide"
)

st.title("📊 Financial & Forensic Analysis Dashboard")

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    file_path = "fsafadashboard2ndtry.xlsx"
    df = pd.read_excel(file_path, sheet_name="Maruti Suzuki", header=None)
    return df

df = load_data()

# ---------------------------
# HELPER FUNCTION
# ---------------------------
def extract_table(start_row, end_row, start_col=1):
    table = df.iloc[start_row:end_row, start_col:]
    table.columns = df.iloc[start_row - 1, start_col:]
    table = table.reset_index(drop=True)
    return table

# ---------------------------
# SIDEBAR – COMPANY SELECTION
# ---------------------------
st.sidebar.header("Select Company")
company = st.sidebar.selectbox(
    "Company",
    ["Maruti Suzuki"]  # extendable later
)

st.sidebar.markdown("---")
st.sidebar.write("📌 Data Source: Financial Statements Excel")

# ===========================
# TOP SECTION – SNAPSHOT + DUPONT
# ===========================
st.subheader("📌 Company Overview")

col1, col2 = st.columns(2)

# ---- Company Snapshot ----
with col1:
    st.markdown("### 🏢 Company Snapshot")
    snapshot = extract_table(2, 8)
    st.dataframe(snapshot, use_container_width=True)

# ---- DuPont Analysis ----
with col2:
    st.markdown("### 🔍 DuPont Analysis")
    dupont = extract_table(18, 24)
    st.dataframe(dupont, use_container_width=True)

# ===========================
# MIDDLE SECTION – EFFICIENCY & LIQUIDITY
# ===========================
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.markdown("### ⚙️ Efficiency Ratios")
    efficiency = extract_table(26, 32)
    st.dataframe(efficiency, use_container_width=True)

with col4:
    st.markdown("### 💧 Liquidity Analysis")
    liquidity = extract_table(34, 40)
    st.dataframe(liquidity, use_container_width=True)

# ===========================
# FORENSIC ANALYSIS
# ===========================
st.markdown("---")
st.subheader("🕵️ Forensic Analysis")

col5, col6 = st.columns(2)

with col5:
    st.markdown("### Accrual Analysis")
    accruals = extract_table(42, 48)
    st.dataframe(accruals, use_container_width=True)

with col6:
    st.markdown("### M-Score, Z-Score & F-Score")
    forensic = extract_table(50, 58)
    st.dataframe(forensic, use_container_width=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("📘 Built using Python, Streamlit & Excel | Financial Statement Forensic Analysis")
