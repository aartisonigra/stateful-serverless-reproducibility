import pandas as pd
import os

files = [
    "data/state_size_100.csv",
    "data/state_size_1000.csv",
    "data/state_size_10000.csv"
]

results = []

for file in files:

    df = pd.read_csv(file)

    for column in ["latency_ms", "client_latency_ms"]:

        mean = df[column].mean()
        median = df[column].median()
        std = df[column].std()
        minimum = df[column].min()
        maximum = df[column].max()
        cv = (std / mean) * 100

        results.append({
            "State_Size": df["state_size"].iloc[0],
            "Metric": column,
            "Mean_ms": mean,
            "Median_ms": median,
            "StdDev_ms": std,
            "Min_ms": minimum,
            "Max_ms": maximum,
            "CV_percent": cv
        })

summary = pd.DataFrame(results)

print("\n===== STATE SIZE EXPERIMENT ANALYSIS =====\n")

print(summary.to_string(index=False))

summary.to_csv(
    "analysis/state_size_summary.csv",
    index=False
)

print("\nSaved: analysis/state_size_summary.csv")