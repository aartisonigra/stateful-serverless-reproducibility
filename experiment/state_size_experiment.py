import boto3
import json
import time
import csv
import os

REGION = "eu-north-1"
FUNCTION_NAME = "stateful-serverless-experiment"

lambda_client = boto3.client("lambda", region_name=REGION)


def invoke_lambda(state_size):

    payload = {
        "state_id": f"state-size-{state_size}",
        "state_size": state_size
    }

    start = time.perf_counter()

    response = lambda_client.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload)
    )

    client_latency = (time.perf_counter() - start) * 1000

    response_payload = json.loads(
        response["Payload"].read().decode("utf-8")
    )

    # Lambda returns API Gateway-style body
    body = response_payload.get("body", "{}")

    if isinstance(body, str):
        body = json.loads(body)

    return body, client_latency


def run_experiment(state_size, count=20):

    results = []

    print(f"\nRunning state-size experiment: {state_size} bytes")
    print(f"Invocations: {count}")

    for i in range(1, count + 1):

        result, client_latency = invoke_lambda(state_size)

        latency = result.get("execution_time_ms", 0)
        counter = result.get("counter", 0)

        print(
            f"{i}/{count} | "
            f"state_size={state_size} | "
            f"counter={counter} | "
            f"lambda={latency:.2f} ms | "
            f"client={client_latency:.2f} ms"
        )

        results.append({
            "invocation": i,
            "state_size": state_size,
            "counter": counter,
            "latency_ms": latency,
            "client_latency_ms": client_latency
        })

    return results


def save_results(results, state_size):

    os.makedirs("data", exist_ok=True)

    filename = f"data/state_size_{state_size}.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "invocation",
                "state_size",
                "counter",
                "latency_ms",
                "client_latency_ms"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"Saved: {filename}")


def main():

    state_sizes = [
        100,
        1000,
        10000
    ]

    for size in state_sizes:

        results = run_experiment(
            state_size=size,
            count=20
        )

        save_results(results, size)


if __name__ == "__main__":
    main()