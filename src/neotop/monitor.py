import psutil
import time



print("===============")
print("System Monitor")
print("===============")
print("\n")


def monitor_cpu_usage():
        aggregate_cpu = psutil.cpu_percent(interval=1)
        per_core_cpu = psutil.cpu_percent(interval=1, percpu=True)
        print(f"CPU: {aggregate_cpu}%")
        print("Per Core CPU Usage:")
        for i, x in enumerate(per_core_cpu):
            print(f"Core {i}: {x}%")
        

def monitor_memory_usage():
        memory_info = psutil.virtual_memory()
        print(f"Total Memory: {memory_info.total / (1024 ** 3):.2f} GB")
        print(f"Available Memory: {memory_info.available / (1024 ** 3):.2f} GB")
        print(f"Used Memory: {memory_info.used / (1024 ** 3):.2f} GB")
        print(f"Memory Usage: {memory_info.percent}%")

def monitor_processes():
    processes = []

    for process in psutil.process_iter(["pid", "name", "memory_percent"]):
        process.cpu_percent(None)

    time.sleep(1)

    processes = []

    for process in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            process.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    time.sleep(1)

    # 3. Collect CPU measurements
    for process in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            processes.append({
                "pid": process.info["pid"],
                "name": process.info["name"],
                "cpu_percent": process.cpu_percent(None)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # 4. Highest CPU first
    processes.sort(key=lambda x: x["cpu_percent"], reverse=True)

    print("Top 5 Processes by CPU:")
    print()
    print(f"{'PID':<10}{'Name':<20}{'CPU'}")
    for process in processes[:5]:
         print(
        f"{process['pid']:<10}"
        f"{process['name']:<20}"
        f"{process['cpu_percent']:.1f}%"
    )

         
def start_monitoring():
    while True:
        print("\n")
        monitor_cpu_usage()
        print("\n")
        monitor_memory_usage()
        print("\n")
        monitor_processes()
        print("\n")
        print("==============================")
        time.sleep(5)  # Monitor every 5 seconds

start_monitoring()
if __name__ == "__monitor__":
    start_monitoring()




_previous_disk = psutil.disk_io_counters()
_previous_time = time.time()


def get_disk_io():
    global _previous_disk, _previous_time

    current_disk = psutil.disk_io_counters()
    current_time = time.time()

    elapsed = current_time - _previous_time

    read_bytes = current_disk.read_bytes - _previous_disk.read_bytes
    write_bytes = current_disk.write_bytes - _previous_disk.write_bytes

    read_rate = read_bytes / elapsed
    write_rate = write_bytes / elapsed

    _previous_disk = current_disk
    _previous_time = current_time

    return {
        "read_bytes_per_sec": read_rate,
        "write_bytes_per_sec": write_rate,
    }