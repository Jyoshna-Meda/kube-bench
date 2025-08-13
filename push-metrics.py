import json
import os
from datetime import datetime

RESULTS_FILE = "/results/bench_output.json"
TEXTFILE_COLLECTOR_DIR = "/var/lib/node_exporter/textfile_collector"
OUTPUT_FILE = os.path.join(TEXTFILE_COLLECTOR_DIR, "kube_bench.prom")

def sanitize_label_value(value):
    # Replace newlines with space, double quotes with single quotes, escape backslashes
    value = value.replace('\n', ' ').replace('"', "'").replace('\\', '\\\\')
    return value

with open(RESULTS_FILE) as f:
    data = json.load(f)

metrics = []
controls = data.get("Controls", [])

for control in controls:
    for test_group in control.get("tests", []):
        for result in test_group.get("results", []):
            test_id = result.get("test_number", "unknown")
            status = result.get("status", "unknown")
            desc = sanitize_label_value(result.get("test_desc", "no_description"))
            remediation = sanitize_label_value(result.get("remediation", "no_remediation"))
            value = 1 if status.lower() == "pass" else 0

            metrics.append(
                f'kube_bench_check{{test_id="{test_id}", status="{status}", desc="{desc}", remediation="{remediation}"}} {value}'
            )

metrics.append(f'# Generated at {datetime.utcnow().isoformat()}Z')

os.makedirs(TEXTFILE_COLLECTOR_DIR, exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(metrics) + "\n")

print(f"Metrics written to {OUTPUT_FILE}")
