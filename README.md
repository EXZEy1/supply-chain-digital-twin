# 🏭 Supply Chain Digital Twin & Optimization Engine

![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Prophet](https://img.shields.io/badge/AI-Prophet-blue)
![PuLP](https://img.shields.io/badge/Optimization-Linear%20Programming-green)
![Supabase](https://img.shields.io/badge/Database-Supabase-emerald)
![GitHub Actions](https://img.shields.io/badge/Automation-GitHub%20Actions-black)

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

