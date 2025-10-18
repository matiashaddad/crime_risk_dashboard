# Global Crime Risk Visualization Dashboard

This project is an interactive web dashboard built with Python Dash/Plotly and SQLite (SQL) that analyzes and visualizes global crime risk levels based on the "World Crime Index 2023" dataset.

It shows a global map and a city-level scatterplot, allowing users to filter data and analyze the relationship between the Crime and the Safety Index.

## Set up and launch dashboard locally:

### 1. Prerequisites
Make sure you have Python 3.x installed.

### 2. Setup and Dependencies:
Go to the main folder, and install all required libraries.
on bash:
cd crime_risk_dashboard
pip install -r requirements.txt

### 3. Data Setup
Download the World Crime Index 2023 dataset and place the CSV file in the data/ directory (exact name: world_crime_index_2023.csv).

### 4. Run the ETL Process (Database Creation)
Run the ETL script to read the CSV, clean, and load the data into the SQLite database (db/risk_database.db).
python src/etl_process.py

### 5. Run the App
python src/dashboard.py

To view the interactive dashboard:
http://127.0.0.1:8050/
