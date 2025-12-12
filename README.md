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



## Dashboard Preview
- **Historical Data Tab:** Multi-store filtering, rolling date window, and exportable table for the days of sales.
- **Market Forecast Tab:** Prophet predictions with store toggles, confidence plotting, and CSV download for planners.
- **Optimization Engine Tab:** Scenario sliders, LP-based baseline plan, editable allocation grid, and real-time KPI updates.

## Key Features
* **AI-Powered Forecasting:** Automatically detects Thai holidays and special shopping events.
* **Cost Optimization:** Uses Linear Programming (PuLP) to solve logistics problems.
* **Cloud-Native:** Data is stored in a centralized Cloud Database (Supabase).
* **Zero-Touch Automation:** The entire data pipeline runs automatically via CI/CD workflows.



## Live Demo
Experience the deployed app on Streamlit Cloud: [Supply Chain Digital Twin](https://supply-chain-digital-twin.streamlit.app)

## Quick Start
Pick the path that fits your setup.

### Option A) Docker
```bash
git clone https://github.com/<your-org>/supply-chain-digital-twin.git
cd supply-chain-digital-twin
docker build -t scdt .
```
with Supabase secrets mapped in
```bash
docker run --rm -p 8501:8501 -v "$PWD/.streamlit:/app/.streamlit" scdt
```
(generate sample data if missing)
```bash
    python src/data_gen.py
    python src/forecast.py
```
offline mode (no Supabase): ensure data/*.csv exists or generate it, then
```bash
docker run --rm -p 8501:8501 -e OFFLINE_MODE=1 \
  -v "$PWD/data:/app/data" scdt
```


### Option B) Local environment
1. **Clone & Install**
   ```bash
   git clone https://github.com/<your-org>/supply-chain-digital-twin.git
   cd supply-chain-digital-twin
   pip install -r requirements.txt
   ```
2. **Configure Secrets**
   * Create `.streamlit/secrets.toml` and set Supabase credentials (URL + service role key) plus any API keys referenced in `app.py`.
3. **Generate Data (Optional / for OFFLINE_MODE)**
   ```bash
   python src/data_gen.py
   python src/forecast.py
   ```
   > Skip if you rely entirely on Supabase tables populated via the daily ETL.
4. **Seed Your Own Supabase (Optional)**
   ```bash
   # requires SUPABASE_URL env (or .streamlit/secrets.toml) to be set
   python src/migrate_db.py
   ```
   > Run this only if you want to upload the generated CSVs to your own Supabase instance. Will fail if `data/sales_history.csv` or `data/forecast_results.csv` are missing, or if `SUPABASE_URL`/`.streamlit/secrets.toml` is not configured; not meant to run from the Streamlit UI.
5. **Run the Dashboard**
   ```bash
   streamlit run app.py
   ```
6. **(Optional) Trigger ETL Workflow**
   * Update `.github/workflows/daily_etl.yml` secrets (`SUPABASE_URL`) and push to run the scheduled GitHub Actions pipeline.

## Project Structure
```
supply-chain-digital-twin/
├── app.py                  # Streamlit dashboard (analytics + optimizer UI)
├── data/                   # Local CSV outputs (when running offline)
├── src/
│   ├── data_gen.py         # Synthetic sales generator with event factors
│   ├── forecast.py         # Prophet training + inference pipeline
│   ├── optimize.py         # PuLP linear program for allocation
│   └── migrate_db.py       # Helper to seed Supabase tables
├── .github/workflows/
│   └── daily_etl.yml       # CI job that regenerates data/forecast + uploads to Supabase
├── .streamlit/secrets.toml # Local secrets (not committed)
└── README.md
```

## Data Flow
1. **Simulate:** `src/data_gen.py` emits historical sales with event-driven spikes and pushes CSVs.
2. **Forecast:** `src/forecast.py` feeds history into Prophet, outputting 30-day forecasts per store.
3. **Sync:** GitHub Actions (`daily_etl.yml`) regenerates data/forecasts nightly and loads both tables into Supabase.
4. **Analyze:** `app.py` pulls Supabase tables via `st.connection`, powering the dashboard tabs.
5. **Optimize & Override:** `src/optimize.py` minimizes shipping + stockout cost; planners adjust allocations interactively and can export the final plan.

## APIs & Integrations
- **Supabase PostgreSQL:** Primary data store accessed securely through `.streamlit/secrets.toml`.
- **GitHub Actions:** Schedules ETL + forecasting so Supabase stays fresh without manual intervention.
- **Streamlit Cloud:** Hosts the live dashboard with the same secrets for consistent prod parity.

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
