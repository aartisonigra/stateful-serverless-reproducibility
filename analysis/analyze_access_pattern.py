import pandas as pd
import os

files = [
    "data/access_pattern_read-heavy.csv",
    "data/access_pattern_write-heavy.csv",
    "data/access_pattern_mixed.csv"
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

        if mean != 0:
            cv = (std / mean) * 100
        else:
            cv = 0

        results.append({
            "Access_Pattern": df["access_pattern"].iloc[0],
            "Metric": column,
            "Mean_ms": mean,
            "Median_ms": median,
            "StdDev_ms": std,
            "Min_ms": minimum,
            "Max_ms": maximum,
            "CV_percent": cv
        })

summary = pd.DataFrame(results)

print("\n===== ACCESS PATTERN EXPERIMENT ANALYSIS =====\n")

print(summary.to_string(index=False))

os.makedirs("analysis", exist_ok=True)

summary.to_csv(
    "analysis/access_pattern_summary.csv",
    index=False
)

print("\nSaved: analysis/access_pattern_summary.csv")