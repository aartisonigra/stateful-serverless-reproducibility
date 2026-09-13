import json
import boto3
import time

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("StatefulServerlessState")


def lambda_handler(event, context):

    start_time = time.perf_counter()

    state_id = event.get("state_id", "test-state")
    state_size = int(event.get("state_size", 100))

    # READ state
    response = table.get_item(
        Key={
            "state_id": state_id
        }
    )

    state = response.get(
        "Item",
        {
            "state_id": state_id,
            "counter": 0,
            "state_data": "x" * state_size
        }
    )

    # Make sure state size is applied
    state["state_data"] = "x" * state_size

    # Update counter
    state["counter"] += 1

    # WRITE state
    table.put_item(
        Item=state
    )

    end_time = time.perf_counter()

    execution_time_ms = (end_time - start_time) * 1000

    return {
        "statusCode": 200,
        "body": json.dumps({
            "state_id": state_id,
            "counter": state["counter"],
            "state_size": state_size,
            "execution_time_ms": execution_time_ms
        })
    }