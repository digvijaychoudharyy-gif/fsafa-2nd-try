import streamlit as st
import pandas as pd

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Financial & Forensic Dashboard", layout="wide")

st.title("📊 Financial & Forensic Analysis Dashboard")

# -------------------------------
# SAFE HELPER FUNCTIONS
# -------------------------------

def clean_table(df):
    """
    Makes dataframe safe for Streamlit:
    - Resets index
    - Removes empty columns
    - Assigns guaranteed unique column names
    """
    df = df.copy()
    df = df.dropna(axis=1, how="all")
    df.reset_index(drop=True, inplace=True)
    df.columns = [f"Col_{i+1}" for i in range(len(df.columns))]
    return df


@st.cache_data
def load_data():
    return pd.read_excel("fsafadashboard2ndtry.xlsx", sheet_name="Maruti Suzuki", header=None)


def extract_table(df, start_row, end_row, start_col=1):
    table = df.iloc[start_row:end_row, start_col:]
    table = clean_table(table)
    return table


# -------------------------------
# LOAD DATA
# -------------------------------
df = load_data()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("Select Company")
company = st.sidebar.selectbox("Company", ["Maruti Suzuki"])

# -------------------------------
# DASHBOARD LAYOUT
# -------------------------------

st.subheader("📌 Company Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏢 Company Snapshot")
    snapshot = extract_table(df, 2, 8)
    st.dataframe(snapshot, use_container_width=True)

with col2:
    st.markdown("### 🔍 DuPont Analysis")
    dupont = extract_table(df, 18, 24)
    st.dataframe(dupont, use_container_width=True)

# --------------------------------

st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.markdown("### ⚙️ Efficiency Ratios")
    efficiency = extract_table(df, 26, 32)
    st.dataframe(efficiency, use_container_width=True)

with col4:
    st.markdown("### 💧 Liquidity Analysis")
    liquidity = extract_table(df, 34, 40)
    st.dataframe(liquidity, use_container_width=True)

# --------------------------------

st.markdown("---")
st.subheader("🕵️ Forensic Analysis")

col5, col6 = st.columns(2)

with col5:
    st.markdown("### Accruals")
    accruals = extract_table(df, 42, 48)
    st.dataframe(accruals, use_container_width=True)

with col6:
    st.markdown("### M-Score | Z-Score | F-Score")
    forensic = extract_table(df, 50, 58)
    st.dataframe(forensic, use_container_width=True)

# --------------------------------
st.markdown("---")
st.caption("✔ Streamlit-safe | ✔ Arrow-safe | ✔ Production-ready")
