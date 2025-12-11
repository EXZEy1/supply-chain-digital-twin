import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add source directory to system path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import optimization logic
from optimize import optimize_distribution

# --- 1. Page Config ---
st.set_page_config(
    page_title="Supply Chain Digital Twin",
    layout="wide"
)

st.title("Supply Chain Digital Twin & Optimization")
st.markdown("### Intelligent Inventory Management & Scenario Simulation System")

# --- 2. Load Data ---
@st.cache_data # Cache data to prevent reloading on every interaction
def load_data():
    # Automatically locate data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    forecast_path = os.path.join(data_dir, 'forecast_results.csv')
    history_path = os.path.join(data_dir, 'sales_history.csv')
    
    # Check if files exist
    if not os.path.exists(forecast_path) or not os.path.exists(history_path):
        return None, None
        
    df_forecast = pd.read_csv(forecast_path)
    df_history = pd.read_csv(history_path)
    return df_forecast, df_history

df_forecast, df_history = load_data()

if df_forecast is None:
    st.error("Data not found! Please run `src/data_gen.py` and `src/forecast.py` first.")
    st.stop()

# --- 3. Sidebar (Control Panel) ---
st.sidebar.header("Configuration")

def format_date_label(date_str):
    """Convert 'YYYY-MM-DD' string to 'YYYY-MM-DD (DayName)'"""
    try:
        dt = pd.to_datetime(date_str)
        return dt.strftime('%Y-%m-%d (%A)') # %A gives full weekday name (e.g., Monday)
    except:
        return date_str


# Select Target Date
available_dates = df_forecast['Date'].unique()
selected_date = st.sidebar.selectbox(
    "Select Target Date:", 
    available_dates,
    format_func=format_date_label 
)

# Filter data for the selected date
daily_demand = df_forecast[df_forecast['Date'] == selected_date].copy()
total_demand = daily_demand['Predicted_Demand'].sum()

st.sidebar.divider()
st.sidebar.subheader("Warehouse Constraints")

# Stock Level Simulation (Slider)
stock_level_pct = st.sidebar.slider("Warehouse Stock Level (% of Demand):", 50, 150, 80)
warehouse_stock = int(total_demand * (stock_level_pct / 100))

st.sidebar.info(f"Total Demand: {total_demand} units")
st.sidebar.warning(f"Available Stock: {warehouse_stock} units")

st.sidebar.divider()
st.sidebar.subheader("Shipping Costs (THB/Unit)")

# Adjust shipping costs dynamically
cost_a = st.sidebar.number_input("Store_A (Furthest)", value=15)
cost_e = st.sidebar.number_input("Store_E (Closest)", value=5)

# Create cost dictionary (Assumed values for others)
shipping_costs = {
    'Store_A': cost_a,
    'Store_B': 10,
    'Store_C': 12,
    'Store_D': 8,
    'Store_E': cost_e
}

# --- 4. Main Dashboard ---

# Tab Layout
tab1, tab2 = st.tabs(["Market Forecast", "Optimization Engine"])

with tab1:
    st.subheader("30-Day Sales Forecast")
    
    # Filter history for visualization context (Last 30 days)
    # (Note: In a real scenario, you would merge history and forecast here)
    
    # Visualize Forecast
    fig_line = px.line(df_forecast, x='Date', y='Predicted_Demand', color='Store', markers=True,
                       title="Predicted Demand by Store")
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.write("Forecast Data Table:")
    st.dataframe(df_forecast)

with tab2:
    st.subheader(f"Optimal Distribution Plan for: {selected_date}")
    
    # Action Button
    if st.button("Run Optimization Allocation"):
        
        # Execute Optimization Logic
        with st.spinner("Running Linear Programming Solver..."):
            allocation_plan = optimize_distribution(daily_demand, warehouse_stock, shipping_costs)
        
        # Key Metrics
        col1, col2, col3 = st.columns(3)
        
        total_allocated = allocation_plan['Allocated_Qty'].sum()
        total_shortage = allocation_plan['Shortage_Qty'].sum()
        fulfillment_rate = (total_allocated / total_demand) * 100
        
        col1.metric("Total Shipped", f"{total_allocated} Units")
        col2.metric("Lost Sales (Stockout)", f"{total_shortage} Units", delta_color="inverse")
        col3.metric("Fulfillment Rate", f"{fulfillment_rate:.1f}%")
        
        # Comparative Chart: Demand vs Allocation
        st.markdown("#### Demand vs. Real Allocation")
        
        # Melt dataframe for Plotly Grouped Bar Chart
        plot_data = allocation_plan[['Store', 'Predicted_Demand', 'Allocated_Qty']].melt(
            id_vars='Store', var_name='Type', value_name='Units'
        )
        
        fig_bar = px.bar(plot_data, x='Store', y='Units', color='Type', barmode='group',
                         color_discrete_map={'Predicted_Demand': 'lightgray', 'Allocated_Qty': 'green'},
                         title="Demand Fulfillment Analysis")
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Detailed Table
        st.markdown("#### Detailed Allocation Plan")
        # Highlight stores with shortages
        st.dataframe(allocation_plan.style.highlight_max(axis=0, subset=['Shortage_Qty'], color="#CE3D3D"))
        
        # Final Status Message
        if total_shortage > 0:
            st.warning("Alert: Stockout detected! The system prioritized stores with lower shipping costs to minimize total loss.")
        else:
            st.success("Success: All demands are fully met.")