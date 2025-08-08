import json
import requests
import os

# Pushgateway settings
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "http://pushgateway-prometheus-pushgateway.monitoring.svc.cluster.local:9091")
JOB_NAME = "kube_bench_detailed"

# Load kube-bench output
with open("/results/bench_output.json") as f:
    data = json.load(f)

metrics = []

controls = data.get("Controls", [])
for control in controls:
    for test_group in control.get("tests", []):
        for result in test_group.get("results", []):
            test_id = result.get("test_number", "unknown")
            status = result.get("status", "unknown")
            desc = result.get("test_desc", "no_description").replace('"', "'").replace("\n", " ")[:100]
            
            # Prometheus metric line
            metric = f'kube_bench_check{{test_id="{test_id}", status="{status}", desc="{desc}"}} 1'
            metrics.append(metric)

# Push all metrics
payload = '\n'.join(metrics) + '\n'
res = requests.post(
    f"{PUSHGATEWAY_URL}/metrics/job/{JOB_NAME}",
    data=payload,
    headers={"Content-Type": "text/plain"}
)

print("Metrics pushed:", res.status_code)

