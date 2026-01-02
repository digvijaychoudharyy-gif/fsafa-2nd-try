import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Financial Dashboard", layout="wide")

# --- DATA LOADING FUNCTIONS ---
@st.cache_data
def load_and_slice_data(file_path):
    """
    Reads the raw CSV with no header, then strictly slices rows based on 
    Excel row numbers provided by the user.
    """
    try:
        # Read the full file without assuming headers
        df_raw = pd.read_csv(file_path, header=None)
        
        data = {}
        
        # Helper function to process a slice
        def process_slice(start_row, end_row):
            # Convert Excel Row Number (1-based) to Python Index (0-based)
            # e.g., Excel Row 2 is Index 1. 
            # Slice is [start-1 : end] because Python stop index is exclusive.
            subset = df_raw.iloc[start_row-1 : end_row].copy()
            
            # Reset index to make processing easier
            subset = subset.reset_index(drop=True)
            
            # The first row of the subset is the header
            subset.columns = subset.iloc[0]
            subset = subset[1:] # Drop the header row from data
            
            # Clean up: Drop columns that are completely empty/NaN
            subset = subset.dropna(how='all', axis=1)
            
            # Set 'Year' or 'Ratio \ Year' as index for easier transposing later
            # We look for a column that contains "Year"
            year_col = [c for c in subset.columns if 'Year' in str(c)]
            if year_col:
                subset = subset.set_index(year_col[0])
            
            return subset

        # --- STRICT ROW SLICING (Based on your inputs) ---
        # 1. Company Snapshot: R2 to R6
        data['snapshot'] = process_slice(2, 6)
        
        # 2. DuPont Analysis: R8 to R14
        data['dupont'] = process_slice(8, 14)
        
        # 3. Liquidity Analysis: R16 to R18
        data['liquidity'] = process_slice(16, 18)
        
        # 4. Efficiency Analysis: R20 to R24
        data['efficiency'] = process_slice(20, 24)
        
        # 5. Accruals Info: R26 to R27
        data['accruals'] = process_slice(26, 27)
        
        # 6. Scores: R29 to R32
        data['scores'] = process_slice(29, 32)
        
        return data

    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None

def plot_line_chart(df, title, y_label="Value"):
    """Helper to create consistent line charts from row-based data"""
    # Transpose: Switch rows and columns so 'Years' are on the X-axis
    df_t = df.transpose()
    
    # Convert data to numeric (coercing errors)
    df_t = df_t.apply(pd.to_numeric, errors='coerce')
    
    # Reset index so 'Year' becomes a column we can plot
    df_t = df_t.reset_index()
    df_t.rename(columns={'index': 'Year'}, inplace=True)
    
    # Create Plotly Chart
    fig = px.line(df_t, x='Year', y=df_t.columns[1:], 
                  title=title, markers=True, 
                  labels={"value": y_label, "variable": "Metric"})
    return fig

def plot_bar_chart(df, title):
    """Helper for bar charts (good for Snapshot/Accruals)"""
    df_t = df.transpose().apply(pd.to_numeric, errors='coerce').reset_index()
    df_t.rename(columns={'index': 'Year'}, inplace=True)
    
    fig = px.bar(df_t, x='Year', y=df_t.columns[1:], 
                 title=title, barmode='group',
                 labels={"value": "Amount", "variable": "Metric"})
    return fig

# --- DASHBOARD LAYOUT ---

st.sidebar.title("Configuration")
company = st.sidebar.selectbox("Select Company", ["Maruti Suzuki"])

# Load Data
file_name = "fsafa dashboard 2nd try.xlsx - Maruti Suzuki.csv"
data = load_and_slice_data(file_name)

if data:
    st.title(f"Financial Dashboard: {company}")
    st.markdown("---")

    # === SECTION 1: FINANCIAL ANALYSIS ===
    st.header("1. Financial Analysis")
    
    # Row 1: Snapshot (Left) | DuPont (Right)
    col1, col2 = st.columns([1.2, 1]) # Left column slightly wider for the graph
    
    with col1:
        st.subheader("📸 Company Snapshot")
        # Visual: Bar chart for Sales/Expenses vs Profit
        fig_snap = plot_bar_chart(data['snapshot'], "Sales, Expenses & Net Profit Trend")
        st.plotly_chart(fig_snap, use_container_width=True)
        # Optional: Show dataframe below toggle
        with st.expander("View Snapshot Data"):
            st.dataframe(data['snapshot'])

    with col2:
        st.subheader("📊 DuPont Analysis")
        st.info("Breakdown of Return on Equity (ROE)")
        # REQUEST: Table ONLY for DuPont
        st.dataframe(data['dupont'], use_container_width=True)

    # Row 2: Efficiency (Left) | Liquidity (Right)
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("⚙️ Efficiency Analysis")
        # Visual: Line chart for Days (DSO, DIO, DPO)
        fig_eff = plot_line_chart(data['efficiency'], "Efficiency Cycles (Days)", "Days")
        st.plotly_chart(fig_eff, use_container_width=True)

    with col4:
        st.subheader("💧 Liquidity Analysis")
        # Visual: Line chart for Ratios
        fig_liq = plot_line_chart(data['liquidity'], "Liquidity Ratios", "Ratio")
        st.plotly_chart(fig_liq, use_container_width=True)

    st.markdown("---")

    # === SECTION 2: FORENSIC ANALYSIS ===
    st.header("2. Forensic Analysis")
    
    # Row 3: Accruals (Left) | Scores (Right)
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader("🔍 Accruals")
        # Visual: Bar chart for Accruals (Positive vs Negative is important)
        fig_acc = plot_bar_chart(data['accruals'], "Accruals Over Time")
        st.plotly_chart(fig_acc, use_container_width=True)
        
    with col6:
        st.subheader("🎯 Forensic Scores")
        # Visual: Multi-line chart for M-Score, Z-Score, F-Score
        fig_score = plot_line_chart(data['scores'], "Risk Scores (M, Z, F)", "Score Value")
        
        # Add reference lines (Optional but helpful for analysis)
        # Z-Score safe zone > 2.99, Distress < 1.81
        fig_score.add_hline(y=1.81, line_dash="dash", line_color="red", annotation_text="Z-Score Distress")
        
        st.plotly_chart(fig_score, use_container_width=True)

else:
    st.warning("Please upload the CSV file to the root folder.")
