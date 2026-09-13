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
# Experimental Results & Analysis

## 1. Lambda Latency Across Invocations
Cold-start penalty is clearly observable on initial invocation (~288ms for 10-run baseline), stabilizing into warm-start steady state (~25–45ms) across subsequent requests.

<img width="959" height="439" alt="Screenshot 2026-09-13 122737" src="https://github.com/user-attachments/assets/9409c0a6-ce0f-45cf-ab3c-7ae5e1bccf01" />
<img width="959" height="446" alt="Screenshot 2026-09-13 122925" src="https://github.com/user-attachments/assets/7f2a03b8-7b07-4a15-90fa-f545c3c84573" />
<img width="959" height="442" alt="Screenshot 2026-09-13 122942" src="https://github.com/user-attachments/assets/8392e80c-a80a-4b7c-b591-6f1f7d8707ff" />
<img width="959" height="440" alt="Screenshot 2026-09-13 123344" src="https://github.com/user-attachments/assets/c0a65e1e-2734-45ae-bb1e-8f3ff1192ffe" />
<img width="959" height="426" alt="Screenshot 2026-09-13 123435" src="https://github.com/user-attachments/assets/9075597a-82d4-475d-b462-cde2a85597d8" />
<img width="959" height="440" alt="Screenshot 2026-09-13 123800" src="https://github.com/user-attachments/assets/0151c2f7-0846-4e89-8b1a-970470fa913d" />
<img width="959" height="430" alt="Screenshot 2026-09-13 123925" src="https://github.com/user-attachments/assets/7f90f337-8d6a-417b-affd-600743d4f800" />
<img width="959" height="434" alt="Screenshot 2026-09-13 124159" src="https://github.com/user-attachments/assets/11753cb4-8664-4757-a877-c8236be14ad7" />
<img width="956" height="434" alt="Screenshot 2026-09-13 124309" src="https://github.com/user-attachments/assets/7f964d8b-f8fa-4efc-9df0-c213705d7065" />
<img width="959" height="428" alt="Screenshot 2026-09-13 124833" src="https://github.com/user-attachments/assets/24286da3-087d-4db0-ab04-41d7968b7997" />
<img width="959" height="428" alt="Screenshot 2026-09-13 125132" src="https://github.com/user-attachments/assets/1f58cbd4-03ad-4387-b9a6-bd509fcf2a90" />
<img width="959" height="437" alt="Screenshot 2026-09-13 125206" src="https://github.com/user-attachments/assets/dbea82bc-23f8-4dce-9562-18a9fcd522be" />
<img width="531" height="325" alt="Screenshot 2026-09-13 125355" src="https://github.com/user-attachments/assets/e0a9f6d1-c8f7-4d9c-a89d-6c56cbaefe30" />
<img width="959" height="427" alt="Screenshot 2026-09-13 125527" src="https://github.com/user-attachments/assets/e2c55bfa-9ab4-4e90-b8ec-b341ac28daa6" />
<img width="957" height="539" alt="Screenshot 2026-09-13 130059" src="https://github.com/user-attachments/assets/0be3c68e-8ceb-480e-8775-c4ad3dc9c38f" />
<img width="959" height="442" alt="Screenshot 2026-09-13 133920" src="https://github.com/user-attachments/assets/8ae3fdb5-f321-484b-ab35-257ce355201f" />
<img width="959" height="440" alt="Screenshot 2026-09-13 134208" src="https://github.com/user-attachments/assets/e6a85500-a81b-439d-8ff6-4b08d9fcfc98" />
<img width="959" height="437" alt="Screenshot 2026-09-13 135349" src="https://github.com/user-attachments/assets/3056d397-76b0-479d-b398-e05f9b27cc7f" />
<img width="911" height="535" alt="Screenshot 2026-09-13 170403" src="https://github.com/user-attachments/assets/e169f2de-2dfa-4307-8524-2abe6ddccfff" />
<img width="497" height="377" alt="image" src="https://github.com/user-attachments/assets/a5aba8a7-63a7-413c-af64-38edaf3ef8a9" />
<img width="501" height="372" alt="image" src="https://github.com/user-attachments/assets/f7d88550-7be3-468a-987a-51520987e088" />


## 2. State Size Scaling Impact
Benchmarked payload serialization and read/write overhead across varying payload sizes:
- **100 bytes**: Minimal serialization overhead (~25-35ms steady state).
- **1000 bytes**: Stable network/storage tier behavior.
- **10000 bytes**: Linear scaling impact on transfer and JSON marshaling overhead.

| State Size | Behavior tier | Observation |
| :--- | :--- | :--- |
| **100 B** | Baseline | Fast cold/warm transition |
| **1 KB** | Nominal | Negligible impact on warm invocations |
| **10 KB** | Elevated | Increased payload transfer & JSON parse time |

## Setup & Replication
- **DynamoDB Table**:
  - Table Name: `StatefulServerlessState`
  - Partition Key: `state_id` (String)
- **Lambda Configuration**:
  - Runtime: Python 3.12
  - Execution Role: IAM Role with DynamoDB read/write access.
  - Code Source: Deploy `experiment/lambda_function.py`.
- **Run Experiments**:
  ```bash
  pip install -r requirements.txt
  python experiment/run_experiment.py
  python experiment/state_size_experiment.py
