import pandas as pd

def analyze_log(timestamp_range):
    df = pd.read_csv("data/sample_log.csv", parse_dates=["timestamp"])

    if timestamp_range:
        start, end = pd.to_datetime(timestamp_range[0]), pd.to_datetime(timestamp_range[1])
        df = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]

    return {
        "average_throughput": round(df["throughput"].mean(), 2),
        "average_rsrp": round(df["rsrp"].mean(), 2),
        "average_snr": round(df["snr"].mean(), 2),
        "sample_count": len(df)
    }
