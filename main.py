import json
import requests
import os

PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "http://pushgateway-prometheus-pushgateway.monitoring.svc.cluster.local:9091")
JOB_NAME = "kube_bench"
LABELS = 'instance="kube-node"'

with open("/results/bench_output.json") as f:
    report = json.load(f)

total_fail = 0
total_pass = 0
total_warn = 0
total_info = 0

for section in report.get("Controls", []):
    for test in section.get("tests", []):
        total_fail += test.get("fail", 0)
        total_pass += test.get("pass", 0)
        total_warn += test.get("warn", 0)
        total_info += test.get("info", 0)

metrics = f"""
# HELP kube_bench_fail Number of failed checks
# TYPE kube_bench_fail gauge
kube_bench_fail{{{LABELS}}} {total_fail}

# HELP kube_bench_pass Number of passed checks
# TYPE kube_bench_pass gauge
kube_bench_pass{{{LABELS}}} {total_pass}

# HELP kube_bench_warn Number of warning checks
# TYPE kube_bench_warn gauge
kube_bench_warn{{{LABELS}}} {total_warn}
"""

res = requests.post(f"{PUSHGATEWAY_URL}/metrics/job/{JOB_NAME}", data=metrics)
print("Metrics pushed:", res.status_code)

