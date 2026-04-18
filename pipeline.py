import csv
import statistics
import datetime

def load_data(filename):
    rows = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def clean_data(rows):
    cleaned = []
    removed = 0
    for row in rows:
        try:
            row["distance_m"] = float(row["distance_m"])
            row["speed_ms"] = float(row["speed_ms"])
            row["battery_pct"] = float(row["battery_pct"])
            row["timestamp"] = datetime.datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
            if row["distance_m"] > 20:
                removed += 1
                continue
            cleaned.append(row)
        except (ValueError, KeyError):
            removed += 1
    print(f"Cleaned data: {len(cleaned)} valid rows, {removed} removed")
    return cleaned

def analyze(rows):
    distances = [r["distance_m"] for r in rows]
    speeds = [r["speed_ms"] for r in rows]
    batteries = [r["battery_pct"] for r in rows]
    stats = {
        "total_rows": len(rows),
        "avg_distance_m": round(statistics.mean(distances), 3),
        "max_distance_m": round(max(distances), 3),
        "min_distance_m": round(min(distances), 3),
        "avg_speed_ms": round(statistics.mean(speeds), 3),
        "max_speed_ms": round(max(speeds), 3),
        "avg_battery_pct": round(statistics.mean(batteries), 3),
        "min_battery_pct": round(min(batteries), 3),
    }
    anomalies = [r for r in rows if r["speed_ms"] > 2.5]
    stats["high_speed_events"] = len(anomalies)
    return stats

def save_report(stats, filename="report.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for k, v in stats.items():
            writer.writerow([k, v])
    print(f"Report saved to {filename}")

def main():
    print("--- Robot Sensor Data Pipeline ---")
    rows = load_data("sensor_data.csv")
    print(f"Loaded {len(rows)} rows")
    cleaned = clean_data(rows)
    stats = analyze(cleaned)
    print("\n--- Summary ---")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    save_report(stats)

if __name__ == "__main__":
    main()
