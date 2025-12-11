import pandas as pd
from pulp import *
import os

def optimize_distribution(forecast_df, warehouse_stock, shipping_costs):
    """
    Use Linear Programming to calculate the optimal amount of stock to send to each store.
    Objective: Minimize Total Costs (Shipping Cost + Shortage Penalty Cost).
    
    Constraints:
    1. Cannot ship more than available warehouse stock.
    2. Ideally, shipped amount should meet predicted demand (soft constraint).
    """
    
    # 1. Setup the Problem
    # We want to minimize costs
    prob = LpProblem("Inventory_Allocation_Optimization", LpMinimize)
    
    # Get list of stores and their predicted demand
    stores = forecast_df['Store'].tolist()
    demands = forecast_df['Predicted_Demand'].tolist()
    demand_dict = dict(zip(stores, demands))
    
    # 2. Define Variables (Decision Variables)
    # 'ship_vars': How much to send to each store? (Integer, >= 0)
    ship_vars = LpVariable.dicts("Ship", stores, lowBound=0, cat='Integer')
    
    # 'shortage_vars': How much demand is unfulfilled? (Integer, >= 0)
    # We need this to calculate penalty for lost sales
    shortage_vars = LpVariable.dicts("Shortage", stores, lowBound=0, cat='Integer')
    
    # 3. Define Costs
    # Penalty for not selling an item (Lost Opportunity) -> Set high to prioritize fulfillment
    SHORTAGE_PENALTY = 1000  
    
    # 4. Objective Function: Minimize (Shipping Costs + Shortage Penalties)
    prob += lpSum([shipping_costs[s] * ship_vars[s] for s in stores]) + \
            lpSum([SHORTAGE_PENALTY * shortage_vars[s] for s in stores])
            
    # 5. Constraints
    
    # Constraint A: Total shipped amount cannot exceed Warehouse Stock
    prob += lpSum([ship_vars[s] for s in stores]) <= warehouse_stock, "Warehouse_Capacity"
    
    # Constraint B: Demand fulfillment logic
    # Amount Shipped + Shortage Amount = Predicted Demand
    # If we ship less than demand, Shortage variable will increase (and trigger penalty)
    for s in stores:
        prob += ship_vars[s] + shortage_vars[s] == demand_dict[s], f"Demand_Balance_{s}"
        
    # 6. Solve the problem
    prob.solve()
    
    # 7. Extract Results
    results = []
    print(f"\nOptimization Status: {LpStatus[prob.status]}")
    
    for s in stores:
        shipped_qty = value(ship_vars[s])
        shortage_qty = value(shortage_vars[s])
        
        results.append({
            'Store': s,
            'Predicted_Demand': demand_dict[s],
            'Allocated_Qty': int(shipped_qty),
            'Shortage_Qty': int(shortage_qty),
            'Status': 'Fulfilled' if shortage_qty == 0 else 'Stockout'
        })
        
    return pd.DataFrame(results)

if __name__ == "__main__":
    # --- Path Setup ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, 'data')
    
    # Load Forecast Data (Created in Phase 2)
    forecast_path = os.path.join(data_dir, 'forecast_results.csv')
    
    if not os.path.exists(forecast_path):
        print("Error: Forecast data not found. Run forecast.py first.")
        exit()
        
    df_forecast = pd.read_csv(forecast_path)
    
    # Let's optimize for "Tomorrow" (Pick the first date in forecast)
    target_date = df_forecast['Date'].min()
    daily_demand = df_forecast[df_forecast['Date'] == target_date].copy()
    
    print(f"Optimizing allocation for date: {target_date}")
    print(f"   Total Predicted Demand: {daily_demand['Predicted_Demand'].sum()} units")
    
    # --- Scenario Simulation ---
    # Scenario: Warehouse has LIMITED stock (Scarcity)
    # Assume we have only 80% of what is needed
    total_demand = daily_demand['Predicted_Demand'].sum()
    warehouse_stock = int(total_demand * 0.8) 
    
    print(f"   Warehouse Available Stock: {warehouse_stock} units (Scarcity Scenario!)")
    
    # Define Shipping Costs (Store A is far, Store E is close)
    shipping_costs = {
        'Store_A': 15, # Expensive to ship
        'Store_B': 10,
        'Store_C': 12,
        'Store_D': 8,
        'Store_E': 5   # Cheap to ship
    }
    
    # Run Optimization
    allocation_plan = optimize_distribution(daily_demand, warehouse_stock, shipping_costs)
    
    # Show Plan
    print("\nFinal Allocation Plan:")
    print(allocation_plan)
    
    # Save Results
    output_path = os.path.join(data_dir, 'allocation_plan.csv')
    allocation_plan.to_csv(output_path, index=False)
    print(f"\nPlan saved to: {output_path}")