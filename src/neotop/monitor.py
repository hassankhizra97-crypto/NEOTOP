import psutil

def monitor_cpu_usage():
    while True:
        aggregate_cpu = psutil.cpu_percent(interval=1)
        per_core_cpu = psutil.cpu_percent(interval=1, percpu=True)
        print(f"Aggregate CPU Usage: {aggregate_cpu}%")
        print(f"Per Core CPU Usage: {per_core_cpu}%")

def monitor_memory_usage():
    while True:
        memory_info = psutil.virtual_memory()
        print(f"Total Memory: {memory_info.total / (1024 ** 3):.2f} GB")
        print(f"Available Memory: {memory_info.available / (1024 ** 3):.2f} GB")
        print(f"Used Memory: {memory_info.used / (1024 ** 3):.2f} GB")
        print(f"Memory Usage: {memory_info.percent}%")

