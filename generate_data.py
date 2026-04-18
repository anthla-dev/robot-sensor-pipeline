import csv
import random
from datetime import datetime, timedelta

random.seed(42)

start_time = datetime(2026, 4, 18, 9, 0, 0)
rows = []

for i in range(200):
    timestamp = start_time + timedelta(seconds=i)
    distance = round(random.uniform(0.5, 10.0), 2)
    speed = round(random.uniform(0.0, 3.0), 2)
    battery = round(100 - (i * 0.3) + random.uniform(-1, 1), 2)

    if random.random() < 0.05:
        distance = round(random.uniform(50, 100), 2)
    if random.random() < 0.05:
        distance = ""
    if random.random() < 0.03:
        speed = ""
    if random.random() < 0.03:
        battery = ""

    rows.append([timestamp.strftime("%Y-%m-%d %H:%M:%S"), distance, speed, battery])

with open("sensor_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "distance_m", "speed_ms", "battery_pct"])
    writer.writerows(rows)

print("Generated sensor_data.csv with 200 rows")