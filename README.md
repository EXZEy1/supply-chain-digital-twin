# Supply Chain Digital Twin & Optimization Engine



## Overview
**Supply Chain Digital Twin** is an end-to-end data product designed to simulate, forecast, and optimize inventory distribution for a retail chain. It moves beyond static analysis by integrating **Automated ETL Pipelines** and **Cloud-based decision support systems**.

## System Architecture
The system operates on a fully automated daily cycle:

1.  **Data Simulation (Python):** Generates realistic daily sales transactions, accounting for seasonality (Paydays, Double Days, Holidays).
2.  **Demand Forecasting (Meta Prophet):** Predicts sales for the next 30 days based on historical patterns.
3.  **Optimization Engine (Linear Programming):** Calculates the optimal stock allocation to minimize shipping costs and lost sales under scarcity constraints.
4.  **Automated ETL (GitHub Actions):** Runs every day at 00:00 UTC to update the **Supabase (PostgreSQL)** database.
5.  **Dashboard (Streamlit):** Visualizes trends and allows managers to simulate "What-if" scenarios (e.g., Stock shortages, Cost changes).

## Key Features
* **AI-Powered Forecasting:** Automatically detects Thai holidays and special shopping events.
* **Cost Optimization:** Uses Linear Programming (PuLP) to solve logistics problems.
* **Cloud-Native:** Data is stored in a centralized Cloud Database (Supabase).
* **Zero-Touch Automation:** The entire data pipeline runs automatically via CI/CD workflows.


## Live Demo
Experience the deployed app on Streamlit Cloud: [Supply Chain Digital Twin](https://supply-chain-digital-twin.streamlit.app)

## Quick Start
Reproduce the project locally in a few steps:

1. **Clone & Install**
   ```bash
   git clone https://github.com/<your-org>/supply-chain-digital-twin.git
   cd supply-chain-digital-twin
   pip install -r requirements.txt
   ```
2. **Configure Secrets**
   * Create `.streamlit/secrets.toml` and set Supabase credentials (URL + service role key) plus any API keys referenced in `app.py`.
3. **Generate Data (Optional)**
   ```bash
   python src/data_gen.py
   python src/forecast.py
   ```
   > Skip if you rely entirely on Supabase tables populated via the daily ETL.
4. **Run the Dashboard**
   ```bash
   streamlit run app.py
   ```
5. **(Optional) Trigger ETL Workflow**
   * Update `.github/workflows/daily_etl.yml` secrets (`SUPABASE_URL`) and push to run the scheduled GitHub Actions pipeline.

## How to Use the Dashboard
1.  **Historical Analysis:** View past sales trends and event impacts.
2.  **Market Forecast:** Check the AI predictions for the next 30 days.
3.  **Optimization Engine:**
    * Adjust **Warehouse Stock** to simulate scarcity.
    * Change **Shipping Costs** to see how the algorithm prioritizes stores.
    * Click **Run Optimization** to see the recommended plan.

## Tech Stack
* **Language:** Python 3.11
* **Libraries:** Pandas, Prophet, PuLP, Streamlit, Plotly, SQLAlchemy
* **Database:** PostgreSQL (Supabase)
* **DevOps:** GitHub Actions, Docker (Optional)
