import sqlite3
import csv
import datetime

def create_database():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            distance_m REAL,
            speed_ms REAL,
            battery_pct REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            speed_ms REAL,
            distance_m REAL
        )
    """)

    conn.commit()
    return conn

def load_clean_data(filename):
    rows = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                distance = float(row["distance_m"])
                speed = float(row["speed_ms"])
                battery = float(row["battery_pct"])
                if distance > 20:
                    continue
                rows.append((row["timestamp"], distance, speed, battery))
            except (ValueError, KeyError):
                continue
    return rows

def insert_data(conn, rows):
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO sensor_readings (timestamp, distance_m, speed_ms, battery_pct)
        VALUES (?, ?, ?, ?)
    """, rows)
    conn.commit()
    print(f"Inserted {len(rows)} rows into database")

def query_anomalies(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, speed_ms, distance_m
        FROM sensor_readings
        WHERE speed_ms > 2.5
        ORDER BY speed_ms DESC
    """)
    results = cursor.fetchall()
    print(f"\nHigh-speed anomalies (speed > 2.5 m/s): {len(results)} events")
    for row in results[:5]:
        print(f"  {row[0]} | speed: {row[1]} m/s | distance: {row[2]} m")
    return results

def query_avg_speed_per_minute(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT substr(timestamp, 1, 16) as minute,
               ROUND(AVG(speed_ms), 3) as avg_speed
        FROM sensor_readings
        GROUP BY minute
        ORDER BY minute
    """)
    results = cursor.fetchall()
    print(f"\nAverage speed per minute:")
    for row in results:
        print(f"  {row[0]} | avg speed: {row[1]} m/s")
    return results

def main():
    print("--- Sensor Database ---")
    conn = create_database()
    rows = load_clean_data("sensor_data.csv")
    insert_data(conn, rows)
    query_anomalies(conn)
    query_avg_speed_per_minute(conn)
    conn.close()

if __name__ == "__main__":
    main()
