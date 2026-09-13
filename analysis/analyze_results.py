import pandas as pd
import numpy as np
import os

files = [
    "data/results_10.csv",
    "data/results_20.csv",
    "data/results_50.csv"
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
            "File": os.path.basename(file),
            "Metric": column,
            "Mean_ms": mean,
            "Median_ms": median,
            "StdDev_ms": std,
            "Min_ms": minimum,
            "Max_ms": maximum,
            "CV_percent": cv
        })

summary = pd.DataFrame(results)

print("\n===== STATEFUL SERVERLESS EXPERIMENT ANALYSIS =====\n")
print(summary.to_string(index=False))

summary.to_csv("analysis/summary_statistics.csv", index=False)

print("\nSaved: analysis/summary_statistics.csv")