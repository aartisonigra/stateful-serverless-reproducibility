import boto3
import json
import time
import csv
import os

REGION = "eu-north-1"
FUNCTION_NAME = "stateful-serverless-experiment"

lambda_client = boto3.client("lambda", region_name=REGION)

def invoke_lambda(state_id):
    start = time.perf_counter()

    response = lambda_client.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps({
            "state_id": state_id
        })
    )

    end = time.perf_counter()

    payload = json.loads(response["Payload"].read())
    body = json.loads(payload["body"])

    return {
        "state_id": body["state_id"],
        "counter": body["counter"],
        "latency_ms": body["latency_ms"],
        "client_latency_ms": (end - start) * 1000
    }


def run_experiment(invocations):
    results = []

    print(f"\nRunning {invocations} invocations...")

    for i in range(invocations):
        result = invoke_lambda("test-state")
        result["invocation"] = i + 1
        result["total_invocations"] = invocations

        results.append(result)

        print(
            f"{i + 1}/{invocations} | "
            f"counter={result['counter']} | "
            f"lambda={result['latency_ms']:.2f} ms | "
            f"client={result['client_latency_ms']:.2f} ms"
        )

    return results


def save_results(results, invocations):
    os.makedirs("data", exist_ok=True)

    filename = f"data/results_{invocations}.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "invocation",
                "total_invocations",
                "state_id",
                "counter",
                "latency_ms",
                "client_latency_ms"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"Saved: {filename}")


def main():
    for count in [10, 20, 50]:
        results = run_experiment(count)
        save_results(results, count)

    print("\nEXPERIMENT COMPLETE!")


if __name__ == "__main__":
    main()