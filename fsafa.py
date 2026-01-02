import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Financial Dashboard", layout="wide")

def get_table_by_keyword(df, start_keyword, row_count):
    """Finds a keyword in the first two columns and returns the next N rows."""
    try:
        # Search for the keyword in the first two columns (where labels usually sit)
        mask = df.iloc[:, :2].apply(lambda x: x.str.contains(start_keyword, na=False, case=False)).any(axis=1)
        if mask.any():
            start_idx = df[mask].index[0]
            # Extract the rows. We include the header row + data rows
            table = df.iloc[start_idx : start_idx + row_count].copy()
            # Clean up: Drop completely empty columns
            table = table.dropna(how='all', axis=1)
            # Use the first row as the header (years)
            table.columns = table.iloc[0]
            table = table[1:].reset_index(drop=True)
            return table
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

# Load the raw data once
@st.cache_data
def load_raw_data(file_path):
    # Read the whole file without a header first to handle irregular rows
    return pd.read_csv(file_path, header=None)

# --- APP START ---
st.sidebar.header("Configuration")
selected_company = st.sidebar.selectbox("Select Company", ["Maruti Suzuki"])

# 1. Load the file
file_path = "fsafa dashboard 2nd try.xlsx - Maruti Suzuki.csv"
raw_df = load_raw_data(file_path)

if not raw_df.empty:
    # 2. Extract sections based on keywords and your specific counts
    # Company Snapshot: Starts with "Year", take 5 rows (Year + 4 metrics)
    snapshot_df = get_table_by_keyword(raw_df, "Sales", 5) 
    
    # DuPont: Starts with "Tax burden", take 7 rows
    dupont_df = get_table_by_keyword(raw_df, "Tax burden", 7)
    
    # Liquidity: Starts with "Current Ratio", take 3 rows
    liquidity_df = get_table_by_keyword(raw_df, "Current Ratio", 3)
    
    # Efficiency: Starts with "Inventory TO", take 5 rows
    efficiency_df = get_table_by_keyword(raw_df, "Inventory TO", 5)
    
    # Accruals: Starts with "Accruals", take 2 rows
    accruals_df = get_table_by_keyword(raw_df, "Accruals", 2)
    
    # Scores: Starts with "M - Score", take 4 rows
    scores_df = get_table_by_keyword(raw_df, "M - Score", 4)

    # --- DASHBOARD LAYOUT ---
    st.title(f"Financial & Forensic Analysis: {selected_company}")

    # Section 1: Financial Analysis
    st.header("Financial Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Company Snapshot")
        st.dataframe(snapshot_df, hide_index=True)
        
        st.subheader("⚙️ Efficiency Analysis")
        st.dataframe(efficiency_df, hide_index=True)

    with col2:
        st.subheader("📈 DuPont Analysis")
        st.dataframe(dupont_df, hide_index=True)
        
        st.subheader("💧 Liquidity Analysis")
        st.dataframe(liquidity_df, hide_index=True)

    st.markdown("---")

    # Section 2: Forensic Analysis
    st.header("Forensic Analysis")
    f_col1, f_col2 = st.columns([1, 1])
    
    with f_col1:
        st.subheader("🔍 Accruals Information")
        st.dataframe(accruals_df, hide_index=True)
        
    with f_col2:
        st.subheader("🎯 Forensic Scores")
        st.table(scores_df)

else:
    st.error("Could not read the file. Please check the file path.")

st.sidebar.info("Upload this to GitHub and connect to Streamlit Cloud to publish.")
