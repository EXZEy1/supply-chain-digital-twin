import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sales_data(days=730):
    """
    Simulate sales data for 5 stores over a period of 2 year.
    Each store will have different demand patterns.
    """
    np.random.seed(42)  # Ensure reproducibility
    stores = ['Store_A', 'Store_B', 'Store_C', 'Store_D', 'Store_E']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Create a list of dates from (Today - 365) to Yesterday
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    
    data = []
    
    for store in stores:
        # Define base demand (varies by store location)
        base_demand = np.random.randint(50, 200) 
        
        for date in dates:
            # Apply seasonality: Sales fluctuate based on the day of the week
            # Example: Weekend sales (Fri, Sat, Sun) receive a 20% boost
            weekday_factor = 1.2 if date.weekday() >= 5 else 0.9 
            # Payday
            factor = 1.0
            if 25 <= date.day <= 31:
                factor *= 1.3  
            
            # Double Days (1.1, 2.2, ... 12.12)
            if date.day == date.month:
                factor *= 2.5  
                
            # Black Friday
            if date.month == 11 and 24 <= date.day <= 30 and date.weekday() == 4:
                factor *= 3.0  

            noise = np.random.normal(0, 10)  # Add random fluctuation
            
            # Calculate daily demand and ensure it's non-negative
            demand = int((base_demand * weekday_factor * factor) + noise)
            demand = max(0, demand) 
            
            data.append([date, store, demand])
            
    # Create DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Store', 'Sales'])
    return df

# Main execution block
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # create sales data
    df = generate_sales_data()
    
    # Save to CSV
    output_path = os.path.join(data_dir, 'sales_history.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Sales data generated successfully: {output_path}")
    print(df.head())