import streamlit as st
import pandas as pd

# ------------------------------------
# PAGE CONFIG
# ------------------------------------
st.set_page_config(
    page_title="Financial & Forensic Dashboard",
    layout="wide"
)

st.title("📊 Financial & Forensic Analysis Dashboard")

# ------------------------------------
# HELPER FUNCTIONS
# ------------------------------------

def make_columns_unique(df):
    """Ensure dataframe column names are unique"""
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        idxs = cols[cols == dup].index.tolist()
        for i, idx in enumerate(idxs):
            cols[idx] = f"{dup}_{i}" if i != 0 else dup
    df.columns = cols
    return df


@st.cache_data
def load_data():
    file_path = "fsafadashboard2ndtry.xlsx"
    return pd.read_excel(file_path, sheet_name="Maruti Suzuki", header=None)


def extract_table(df, start_row, end_row, start_col=1):
    table = df.iloc[start_row:end_row, start_col:]
    table.columns = df.iloc[start_row - 1, start_col:]
    table = table.reset_index(drop=True)
    table = make_columns_unique(table)
    return table


# ------------------------------------
# LOAD DATA
# ------------------------------------
df = load_data()

# ------------------------------------
# SIDEBAR
# ------------------------------------
st.sidebar.header("Select Company")
company = st.sidebar.selectbox("Company", ["Maruti Suzuki"])
st.sidebar.markdown("---")
st.sidebar.write("📁 Data Source: Excel File")

# ------------------------------------
# TOP SECTION – SNAPSHOT & DUPONT
# ------------------------------------
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

# ------------------------------------
# MIDDLE SECTION – EFFICIENCY & LIQUIDITY
# ------------------------------------
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

# ------------------------------------
# BOTTOM SECTION – FORENSIC ANALYSIS
# ------------------------------------
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

# ------------------------------------
# FOOTER
# ------------------------------------
st.markdown("---")
st.caption("📘 Financial & Forensic Analysis Dashboard | Built using Streamlit & Python")
