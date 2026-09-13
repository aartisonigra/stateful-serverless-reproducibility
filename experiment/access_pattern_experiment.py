import boto3
import json
import time
import csv
import os

REGION = "eu-north-1"
FUNCTION_NAME = "stateful-serverless-experiment"

lambda_client = boto3.client("lambda", region_name=REGION)


def invoke_lambda(state_id, access_pattern):

    payload = {
        "state_id": state_id,
        "access_pattern": access_pattern
    }

    start = time.perf_counter()

    response = lambda_client.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload)
    )

    client_latency = (time.perf_counter() - start) * 1000

    raw = response["Payload"].read().decode("utf-8")
    result = json.loads(raw)

    # Lambda proxy response
    if "body" in result:
        body = result["body"]

        if isinstance(body, str):
            body = json.loads(body)

        result = body

    return result, client_latency


def run_experiment(access_pattern, count=20):

    results = []

    state_id = f"pattern-{access_pattern}"

    print(f"\nRunning access-pattern experiment: {access_pattern}")
    print(f"Invocations: {count}")

    for i in range(1, count + 1):

        result, client_latency = invoke_lambda(
            state_id,
            access_pattern
        )

        latency = result.get(
            "execution_time_ms",
            result.get("latency_ms", 0)
        )

        counter = result.get("counter", 0)

        print(
            f"{i}/{count} | "
            f"pattern={access_pattern} | "
            f"counter={counter} | "
            f"lambda={latency:.2f} ms | "
            f"client={client_latency:.2f} ms"
        )

        results.append({
            "invocation": i,
            "access_pattern": access_pattern,
            "counter": counter,
            "latency_ms": latency,
            "client_latency_ms": client_latency
        })

    return results


def save_results(results, access_pattern):

    os.makedirs("data", exist_ok=True)

    filename = f"data/access_pattern_{access_pattern}.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "invocation",
                "access_pattern",
                "counter",
                "latency_ms",
                "client_latency_ms"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"Saved: {filename}")


def main():

    patterns = [
        "read-heavy",
        "write-heavy",
        "mixed"
    ]

    for pattern in patterns:

        results = run_experiment(
            access_pattern=pattern,
            count=20
        )

        save_results(results, pattern)


if __name__ == "__main__":
    main()