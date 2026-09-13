import pandas as pd
import matplotlib.pyplot as plt
import os

files = [
    ("10 Invocations", "data/results_10.csv"),
    ("20 Invocations", "data/results_20.csv"),
    ("50 Invocations", "data/results_50.csv")
]

os.makedirs("analysis/graphs", exist_ok=True)

# --------------------------------------------------
# Graph 1: Lambda latency vs invocation number
# --------------------------------------------------

plt.figure()

for label, file in files:
    df = pd.read_csv(file)
    plt.plot(
        df["invocation"],
        df["latency_ms"],
        marker="o",
        label=label
    )

plt.xlabel("Invocation Number")
plt.ylabel("Lambda Latency (ms)")
plt.title("Lambda Latency Across Invocations")
plt.legend()
plt.grid(True)

plt.savefig("analysis/graphs/lambda_latency.png", dpi=300)
plt.close()


# --------------------------------------------------
# Graph 2: Client latency vs invocation number
# --------------------------------------------------

plt.figure()

for label, file in files:
    df = pd.read_csv(file)
    plt.plot(
        df["invocation"],
        df["client_latency_ms"],
        marker="o",
        label=label
    )

plt.xlabel("Invocation Number")
plt.ylabel("Client Latency (ms)")
plt.title("Client Latency Across Invocations")
plt.legend()
plt.grid(True)

plt.savefig("analysis/graphs/client_latency.png", dpi=300)
plt.close()


# --------------------------------------------------
# Graph 3: Coefficient of Variation
# --------------------------------------------------

summary = pd.read_csv("analysis/summary_statistics.csv")

lambda_cv = summary[
    summary["Metric"] == "latency_ms"
]

client_cv = summary[
    summary["Metric"] == "client_latency_ms"
]

workloads = [10, 20, 50]

plt.figure()

plt.plot(
    workloads,
    lambda_cv["CV_percent"],
    marker="o",
    label="Lambda Latency CV"
)

plt.plot(
    workloads,
    client_cv["CV_percent"],
    marker="o",
    label="Client Latency CV"
)

plt.xlabel("Number of Invocations")
plt.ylabel("Coefficient of Variation (%)")
plt.title("Performance Variability Across Workloads")
plt.legend()
plt.grid(True)

plt.savefig("analysis/graphs/coefficient_of_variation.png", dpi=300)
plt.close()


print("\n===== GRAPHS CREATED SUCCESSFULLY =====")
print("1. analysis/graphs/lambda_latency.png")
print("2. analysis/graphs/client_latency.png")
print("3. analysis/graphs/coefficient_of_variation.png")