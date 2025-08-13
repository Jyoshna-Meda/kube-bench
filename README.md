# 🌟 Kube-Bench → Prometheus → Grafana Setup

This guide explains how to:
1. Run **kube-bench** as a Kubernetes CronJob.
2. Export results to Prometheus via **node_exporter textfile collector**.
3. View compliance results in Grafana.

---

## 🛠 Prerequisites
- Kubernetes cluster (tested on v1.32)
- `kubectl` & `helm` installed
- Prometheus & Grafana deployed (e.g., via kube-prometheus-stack)

---

## 🚀 Steps

### **1️⃣ 📊 Parses the results into Prometheus metrics via node_exporter’s textfile collector.
Upgrade `prometheus-node-exporter` with the provided values file:

```bash
  helm upgrade monitoring prometheus-community/kube-prometheus-stack -n monitoring -f current-values.yaml

### **2️⃣ Create the ConfigMap from your Python script
 - The Python script reads Kube-Bench’s JSON results, extracts the test results (PASS, FAIL, WARN), and writes them as Prometheus-readable metrics
   into a file that node_exporter can pick up.

   kubectl create configmap kube-bench-parser --from-file=push-metrics.py
### **3️⃣🕒 Runs kube-bench automatically using a CronJob.
    The CronJob ensures Kube-Bench is run automatically on a schedule (e.g., daily at midnight), so you always have fresh security compliance data
     in Prometheus & Grafana.
    kubectl apply -f cron-job.yaml
### **4️⃣ Displays real-time compliance status in Grafana dashboards.
     use json which is grafana-dashboard.json
