import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Financial & Forensic Dashboard")

st.title("📊 Financial & Forensic Analysis Dashboard")

# --------------------------------------------------
# LOAD FILE
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("fsafa dashboard 2nd try.xlsx", header=None)

df = load_data()

# --------------------------------------------------
# CLEAN & EXTRACT FUNCTION
# --------------------------------------------------
def clean_extract(start_row, end_row):
    temp = df.iloc[start_row:end_row].copy()

    # Drop fully empty columns
    temp = temp.dropna(axis=1, how="all")

    # First non-null row = header
    header_row = temp.iloc[0]
    temp = temp[1:]
    temp.columns = header_row

    # Drop fully empty rows
    temp = temp.dropna(how="all")

    # Reset index
    temp.reset_index(drop=True, inplace=True)

    return temp


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
st.subheader("📌 Company Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏢 Company Snapshot")
    snapshot = clean_extract(2, 9)
    st.dataframe(snapshot, use_container_width=True)

with col2:
    st.markdown("### 🔍 DuPont Analysis")
    dupont = clean_extract(13, 20)
    st.dataframe(dupont, use_container_width=True)

#
