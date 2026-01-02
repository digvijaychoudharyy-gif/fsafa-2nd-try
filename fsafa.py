import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration for a wide layout
st.set_page_config(page_title="Financial Analysis Dashboard", layout="wide")

# Function to load data from specific row ranges
def load_data(file_path):
    # Read the CSV (adjusting for the 1-row offset often found in Excel-to-CSV exports)
    # We use skiprows and nrows to target your specific sections
    try:
        data = {}
        # 1. Company Snapshot (Rows 2-6) -> Python index 1 to 5
        data['snapshot'] = pd.read_csv(file_path, skiprows=1, nrows=5).dropna(how='all', axis=1)
        
        # 2. DuPont Analysis (Rows 8-14) -> Python index 7 to 13
        data['dupont'] = pd.read_csv(file_path, skiprows=7, nrows=7).dropna(how='all', axis=1)
        
        # 3. Liquidity Analysis (Rows 16-18) -> Python index 15 to 17
        data['liquidity'] = pd.read_csv(file_path, skiprows=15, nrows=3).dropna(how='all', axis=1)
        
        # 4. Efficiency Analysis (Rows 20-24) -> Python index 19 to 23
        data['efficiency'] = pd.read_csv(file_path, skiprows=19, nrows=5).dropna(how='all', axis=1)
        
        # 5. Accruals Info (Rows 26-27) -> Python index 25 to 26
        data['accruals'] = pd.read_csv(file_path, skiprows=25, nrows=2).dropna(how='all', axis=1)
        
        # 6. Scores (Rows 29-32) -> Python index 28 to 31
        data['scores'] = pd.read_csv(file_path, skiprows=28, nrows=4).dropna(how='all', axis=1)
        
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Sidebar - Company Selection
st.sidebar.header("Navigation")
company_options = ["Maruti Suzuki"] # You can add more companies here later
selected_company = st.sidebar.selectbox("Choose Company", company_options)

if selected_company:
    st.title(f"Financial & Forensic Analysis: {selected_company}")
    
    # Load the specific file for Maruti Suzuki
    # Make sure the filename matches your uploaded file
    file_name = "fsafa dashboard 2nd try.xlsx - Maruti Suzuki.csv"
    data = load_data(file_name)

    if data:
        # --- FINANCIAL ANALYSIS SECTION ---
        st.header("Financial Analysis")
        
        # Top Row: Snapshot (Left) and DuPont (Right)
        top_col1, top_col2 = st.columns(2)
        
        with top_col1:
            st.subheader("📊 Company Snapshot")
            st.dataframe(data['snapshot'], use_container_width=True)
            
        with top_col2:
            st.subheader("📈 DuPont Analysis")
            st.dataframe(data['dupont'], use_container_width=True)
            
        # Bottom Row: Efficiency (Left) and Liquidity (Right)
        mid_col1, mid_col2 = st.columns(2)
        
        with mid_col1:
            st.subheader("⚙️ Efficiency Ratios")
            st.dataframe(data['efficiency'], use_container_width=True)
            
        with mid_col2:
            st.subheader("💧 Liquidity Analysis")
            st.dataframe(data['liquidity'], use_container_width=True)

        st.divider()

        # --- FORENSIC ANALYSIS SECTION ---
        st.header("Forensic Analysis")
        
        # Accruals on top, then Scores
        st.subheader("🔍 Accruals Information")
        st.dataframe(data['accruals'], use_container_width=True)
        
        st.subheader("🎯 Forensic Scores (M-Score, Z-Score, F-Score)")
        st.table(data['scores']) # Using table for a cleaner look for scores

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed for GitHub & Streamlit")
