import pandas as pd
from sqlalchemy import create_engine
import os
import streamlit as st

# Function to get DB connection URL
def get_db_connection_url():
    # 1. ลองดึงจาก st.secrets (สำหรับรันในเครื่อง Local)
    try:
        return st.secrets["connections"]["supabase"]["url"]
    except (FileNotFoundError, KeyError):
        pass # Maybe run in GitHub Actions?

    # 2. try to get from Environment Variables (GitHub Actions)
    url = os.environ.get("SUPABASE_URL")
    if url:
        return url
    
    raise ValueError("Database connection URL not found in st.secrets or Environment Variables.")

# 1. Load local CSV files
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
data_dir = os.path.join(project_root, 'data')

try:
    df_history = pd.read_csv(os.path.join(data_dir, 'sales_history.csv'))
    df_forecast = pd.read_csv(os.path.join(data_dir, 'forecast_results.csv'))
    print("Downloaded local CSV files successfully.")
except FileNotFoundError:
    print("Data files not found locally. Please run data_gen.py and forecast.py first.")
    exit()

# 2. connect to Cloud Database
conn_str = get_db_connection_url()
engine = create_engine(
    conn_str,
    connect_args={'prepare_threshold': None} 
)

print("Connected to Cloud Database successfully.")

# 3. pass data to Cloud Database
try:
    df_history.to_sql('sales_history', engine, if_exists='replace', index=False)
    print("   - Table 'sales_history': Uploaded")
    
    df_forecast.to_sql('forecast_results', engine, if_exists='replace', index=False)
    print("   - Table 'forecast_results': Uploaded")
    
    print("\n Migration completed successfully!")
except Exception as e:
    print(f"\n Error: {e}")