import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Financial & Forensic Dashboard", layout="wide")

st.title("📊 Financial & Forensic Analysis Dashboard")

# --------------------------------------------------
# LOAD EXCEL FILE
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("fsafa dashboard 2nd try.xlsx", header=None)

df = load_data()

# --------------------------------------------------
# FUNCTION TO EXTRACT CLEAN TABLE
# --------------------------------------------------
def extract_table(header_row, start_row, end_row):
    """
    header_row : row number containing column names
    start_row  : first data row
    end_row    : last data row (exclusive)
    """
    temp = df.iloc[header_row:end_row].copy()
    temp.columns = temp.iloc[0]          # set header
    temp = temp[1:]                      # remove header row
    temp = temp.loc[:, temp.columns.notna()]  # drop empty columns
    temp.reset_index(drop=True, inplace=True)
    return temp

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
    snapshot =
