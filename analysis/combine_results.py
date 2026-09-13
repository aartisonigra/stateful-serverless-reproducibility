import pandas as pd
import os

files = [
    "analysis/summary_statistics.csv",
    "analysis/state_size_summary.csv",
    "analysis/access_pattern_summary.csv"
]

frames = []

for file in files:
    if os.path.exists(file):
        df = pd.read_csv(file)
        df["Source"] = os.path.basename(file)
        frames.append(df)

combined = pd.concat(frames, ignore_index=True)

os.makedirs("analysis", exist_ok=True)

combined.to_csv(
    "analysis/final_combined_results.csv",
    index=False
)

print("\n===== FINAL COMBINED RESULTS =====\n")
print(combined.to_string(index=False))

print("\nSaved: analysis/final_combined_results.csv")