import psutil
import time

# def monitor_cpu_usage():
#     while True:
#         aggregate_cpu = psutil.cpu_percent(interval=1)
#         per_core_cpu = psutil.cpu_percent(interval=1, percpu=True)
#         print(f"Aggregate CPU Usage: {aggregate_cpu}%")
#         print(f"Per Core CPU Usage: {per_core_cpu}%")

# def monitor_memory_usage():
#     while True:
#         memory_info = psutil.virtual_memory()
#         print(f"Total Memory: {memory_info.total / (1024 ** 3):.2f} GB")
#         print(f"Available Memory: {memory_info.available / (1024 ** 3):.2f} GB")
#         print(f"Used Memory: {memory_info.used / (1024 ** 3):.2f} GB")
#         print(f"Memory Usage: {memory_info.percent}%")


processes = []

# Start measuring
for process in psutil.process_iter(["pid", "name", "memory_percent"]):
    process.cpu_percent(None)

# One-second measurement window
time.sleep(1)

# Get the measurements
for process in psutil.process_iter(["pid", "name", "memory_percent"]):

    processes.append({
        "pid": process.info["pid"],
        "name": process.info["name"],
        "cpu_percent": process.cpu_percent(None),
        "memory_percent": process.info["memory_percent"]
    })

# Highest CPU first
processes.sort(key=lambda x: x["cpu_percent"], reverse=True)

print(f"Top 5 Processes by CPU Usage:\n{processes[:5]}")