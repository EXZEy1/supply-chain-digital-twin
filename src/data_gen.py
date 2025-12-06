import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sales_data(days=365):
    """
    Simulate sales data for 5 stores over a period of 1 year.
    Each store will have different demand patterns.
    """
    np.random.seed(42)  # Ensure reproducibility
    stores = ['Store_A', 'Store_B', 'Store_C', 'Store_D', 'Store_E']
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(days)]
    
    data = []
    
    for store in stores:
        # Define base demand (varies by store location)
        base_demand = np.random.randint(50, 200) 
        
        for date in dates:
            # Apply seasonality: Sales fluctuate based on the day of the week
            # Example: Weekend sales (Fri, Sat, Sun) receive a 20% boost
            weekday_factor = 1.2 if date.weekday() >= 5 else 0.9 
            noise = np.random.normal(0, 10)  # Add random fluctuation
            
            # Calculate daily demand and ensure it's non-negative
            demand = int((base_demand * weekday_factor) + noise)
            demand = max(0, demand) 
            
            data.append([date, store, demand])
            
    # Create DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Store', 'Sales'])
    return df

# Main execution block
if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs('../data', exist_ok=True)
    
    df = generate_sales_data()
    
    # Save generated data to CSV
    output_path = '../data/sales_history.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Sales data generated successfully: {output_path}")
    print(df.head())