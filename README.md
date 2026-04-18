# Robot Sensor Data Pipeline

A Python data pipeline that ingests, cleans, analyzes, and stores simulated robot sensor data.

## What it does
- Generates 200 rows of simulated sensor data (distance, speed, battery) with real-world issues: missing values, outliers, bad readings
- Cleans and validates data, removing 23 invalid rows
- Computes statistics: averages, min/max, anomaly detection
- Stores cleaned data in a SQLite database
- Runs SQL queries for anomaly detection and per-minute speed averages
- Outputs a summary report to CSV

## Results
- 177 valid rows retained from 200
- 29 high-speed anomaly events detected
- Battery drain tracked from 100% to 40.11%

## Run it
```bash
python3 generate_data.py
python3 pipeline.py
python3 database.py
```

## Skills demonstrated
Python, SQLite, SQL queries, CSV processing, data cleaning, statistical analysis, anomaly detection
