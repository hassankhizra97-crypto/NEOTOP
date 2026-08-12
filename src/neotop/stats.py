import psutil
import time

import sys
import time


def initialize_processes():
    for process in psutil.process_iter(["pid", "name"]):
        try:
            process.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
# ============================================================
# Previous samples for disk and network rate calculations
# ============================================================

_previous_disk = psutil.disk_io_counters()
_previous_disk_time = time.monotonic()

_previous_net = psutil.net_io_counters()
_previous_net_time = time.monotonic()


# ============================================================
# CPU
# ============================================================

def get_cpu():
    aggregate_cpu = psutil.cpu_percent(interval=None)
    per_core_cpu = psutil.cpu_percent(interval=None, percpu=True)

    return {
        "aggregate": aggregate_cpu,
        "per_core": per_core_cpu
    }


# ============================================================
# Memory
# ============================================================

def get_memory():
    memory_info = psutil.virtual_memory()

    return {
        "total": memory_info.total,
        "available": memory_info.available,
        "used": memory_info.used,
        "percent": memory_info.percent
    }


# ============================================================
# Processes
# ============================================================

def get_top_processes(n):
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_percent"]
    ):
        try:
            cpu_percent = process.cpu_percent(None)

            processes.append({
                "pid": process.info["pid"],
                "name": process.info["name"],
                "cpu_percent": cpu_percent,
                "memory_percent": process.info["memory_percent"],
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    processes.sort(
        key=lambda x: x["cpu_percent"],
        reverse=True
    )

    return processes[:n]
# ============================================================
# Disk I/O
# ============================================================

def get_disk_io():
    global _previous_disk
    global _previous_disk_time

    current_disk = psutil.disk_io_counters()
    current_time = time.monotonic()

    # Make sure psutil returned valid counters
    if current_disk is None:
        return {
            "read_rate": 0.0,
            "write_rate": 0.0
        }

    elapsed = current_time - _previous_disk_time

    # Avoid division by zero
    if elapsed <= 0:
        return {
            "read_rate": 0.0,
            "write_rate": 0.0
        }

    # Calculate how many bytes were transferred
    read_bytes = (
        current_disk.read_bytes -
        _previous_disk.read_bytes
    )

    write_bytes = (
        current_disk.write_bytes -
        _previous_disk.write_bytes
    )

    # Convert amount transferred into a rate
    read_rate = read_bytes / elapsed
    write_rate = write_bytes / elapsed

    # IMPORTANT:
    # Save current reading for the NEXT function call
    _previous_disk = current_disk
    _previous_disk_time = current_time

    return {
        "read_rate": read_rate,
        "write_rate": write_rate
    }


# ============================================================
# Network I/O
# ============================================================

def get_network_io():
    global _previous_net
    global _previous_net_time

    current_net = psutil.net_io_counters()
    current_time = time.monotonic()

    if current_net is None:
        return {
            "sent_rate": 0.0,
            "received_rate": 0.0
        }

    elapsed = current_time - _previous_net_time

    if elapsed <= 0:
        return {
            "sent_rate": 0.0,
            "received_rate": 0.0
        }

    # Calculate bytes transferred since previous sample
    bytes_sent = (
        current_net.bytes_sent -
        _previous_net.bytes_sent
    )

    bytes_received = (
        current_net.bytes_recv -
        _previous_net.bytes_recv
    )

    # Convert to bytes/second
    sent_rate = bytes_sent / elapsed
    received_rate = bytes_received / elapsed

    # Save current reading for NEXT call
    _previous_net = current_net
    _previous_net_time = current_time

    return {
        "sent_rate": sent_rate,
        "received_rate": received_rate
    }

