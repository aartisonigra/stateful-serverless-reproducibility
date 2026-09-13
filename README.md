# Stateful Serverless Reproducibility Experiment

Comprehensive research pilot exploring state persistence, cold/warm start latency dynamics, and state-size overhead in serverless architectures using **AWS Lambda** and **Amazon DynamoDB**.

## Architecture Overview
- **Compute**: AWS Lambda (`Python 3.12`)
- **State Store**: Amazon DynamoDB (`StatefulServerlessState`)
- **Partition Key**: `state_id` (String)

## Project Structure
```text
stateful-serverless-reproducibility/
│
├── analysis/
│   ├── graphs/
│   │   ├── lambda_latency.png         # Invocation latency comparison (10, 20, 50 runs)
│   │   ├── client_latency.png         # End-to-end client latency metrics
│   │   └── coefficient_variation.png  # Variance analysis across runs
│   ├── data/
│   │   ├── results_10.csv
│   │   ├── results_20.csv
│   │   ├── results_50.csv
│   │   ├── state_size_100.csv
│   │   ├── state_size_1000.csv
│   │   └── state_size_10000.csv
│   └── *.py scripts                   # Analysis & plotting pipeline
├── experiment/
│   ├── lambda_function.py             # AWS Lambda handler querying DynamoDB state
│   ├── run_experiment.py              # Automated test invocation harness
│   └── state_size_experiment.py       # Payload scaling benchmark script
├── README.md                          # Project documentation & findings
└── requirements.txt                   # SDK dependencies (boto3)

```
Experimental Results & Analysis1. Lambda Latency Across InvocationsCold-start penalty is clearly observable on initial invocation (~288ms for 10-run baseline), stabilizing into warm-start steady state (~25–45ms) across subsequent requests.2. State Size Scaling ImpactBenchmarked payload serialization and read/write overhead across varying payload sizes:100 bytes: Minimal serialization overhead (~25-35ms steady state).1000 bytes: Stable network/storage tier behavior.10000 bytes: Linear scaling impact on transfer and JSON marshaling overhead.State SizeBehavior tierObservation100 BBaselineFast cold/warm transition1 KBNominalNegligible impact on warm invocations10 KBElevatedIncreased payload transfer & JSON parse timeSetup & ReplicationDynamoDB Table:Table Name: StatefulServerlessStatePartition Key: state_id (String)Lambda Configuration:Runtime: Python 3.12Execution Role: IAM Role with DynamoDB read/write access.Code Source: Deploy experiment/lambda_function.py.Run Experiments:
