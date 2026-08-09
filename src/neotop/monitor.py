import psutil

def monitor_cpu_usage():
    while True:
        aggregate_cpu = psutil.cpu_percent(interval=1)
        per_core_cpu = psutil.cpu_percent(interval=1, percpu=True)
        print(f"Aggregate CPU Usage: {aggregate_cpu}%")
        print(f"Per Core CPU Usage: {per_core_cpu}%")



