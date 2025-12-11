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
@st.cache_data(ttl=600) # cache data for 10 minutes
def load_data():
    try:
        # Setup connection to Supabase
        conn = st.connection("supabase", type="sql")
        
        # Query data from tables
        df_forecast = conn.query("SELECT * FROM forecast_results;", ttl=0)
        df_history = conn.query("SELECT * FROM sales_history;", ttl=0)
        
        # Ensure Date columns are in datetime format
        df_forecast['Date'] = pd.to_datetime(df_forecast['Date'])
        df_history['Date'] = pd.to_datetime(df_history['Date'])
        
        return df_forecast, df_history
        
    except Exception as e:
        st.error(f" Error loading data from database: {e}")
        return None, None

df_forecast, df_history = load_data()

if df_forecast is None:
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
cost_b = st.sidebar.number_input("Store_B", value=10)
cost_c = st.sidebar.number_input("Store_C", value=12)
cost_d = st.sidebar.number_input("Store_D", value=8)
cost_e = st.sidebar.number_input("Store_E (Closest)", value=5)

# Create cost dictionary
shipping_costs = {
    'Store_A': cost_a,
    'Store_B': cost_b,
    'Store_C': cost_c,
    'Store_D': cost_d,
    'Store_E': cost_e
}

# --- 4. Main Dashboard ---

# Tab Layout
tab1, tab2, tab3 = st.tabs(["Historical Data", "Market Forecast", "Optimization Engine"])
with tab1:
    st.subheader("Last 30-Day Historical Sales Data")
    
    all_stores_history = df_history['Store'].unique()
    
    # Multi-select for Stores
    selected_stores_hist = st.multiselect(
        "Filter by Store(s):",
        options=all_stores_history,
        default=all_stores_history,
        key="history_filter"
    )
    
    # Filter historical data based on selected stores
    filtered_history = df_history[df_history['Store'].isin(selected_stores_hist)]

    filtered_history['Date'] = pd.to_datetime(filtered_history['Date'])
    latest_date = filtered_history['Date'].max()
    start_date_30d = latest_date - pd.Timedelta(days=30)

    # Filter to last 30 days
    filtered_history = filtered_history[filtered_history['Date'] > start_date_30d]
    
    # If no stores selected, show warning
    if filtered_history.empty:
        st.warning("Please select at least one store to view the historical data.")
    else:
        # Visualization: Line Chart of Historical Sales
        fig_hist = px.line(
            filtered_history, 
            x='Date', 
            y='Sales', 
            color='Store', 
            markers=True,
            title="Historical Sales Trends"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        st.divider()
        
        col_hist_view, col_hist_download = st.columns([4, 1])
        
        with col_hist_view:
            st.markdown("### Detailed Data Table")            
            st.dataframe(
                filtered_history,
                column_config={
                    "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                    "Sales": st.column_config.NumberColumn("Sales (Units)")
                },
                use_container_width=True,
                hide_index=True 
            )
            
        with col_hist_download:
            # Download to CSV
            csv_hist = filtered_history.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv_hist,
                file_name="historical_sales_data.csv",
                mime="text/csv"
            )


with tab2:
    st.subheader("30-Day Sales Forecast")
    
    all_stores_forcast = df_forecast['Store'].unique()
    
    # Multi-select for Stores
    selected_stores_view = st.multiselect(
        "Filter by Store(s):",
        options=all_stores_forcast,
        default=all_stores_forcast,
        key = "forecast_filter"
    )
    
    # Filter forecast data based on selected stores
    filtered_forecast = df_forecast[df_forecast['Store'].isin(selected_stores_view)]
    
    
    # If no stores selected, show warning
    if filtered_forecast.empty:
        st.warning("Please select at least one store to view the forecast data.")
    else:
        # Visualization: Line Chart of Predicted Demand
        fig_line = px.line(
            filtered_forecast, 
            x='Date', 
            y='Predicted_Demand', 
            color='Store', 
            markers=True,
            title="Predicted Demand Trends"
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        st.divider()
        
        
        col_view, col_download = st.columns([4, 1])
        
        with col_view:
            st.markdown("### Detailed Data Table")            
            st.dataframe(
                filtered_forecast,
                column_config={
                    "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                    "Predicted_Demand": st.column_config.NumberColumn("Demand (Units)")
                },
                use_container_width=True,
                hide_index=True 
            )
            
        with col_download:
            # Download to CSV
            csv = filtered_forecast.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="forecast_data.csv",
                mime="text/csv"
            )


with tab3:
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
                         color_discrete_map={'Predicted_Demand': 'lightgray', 'Allocated_Qty': '#CE3D3D'},
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