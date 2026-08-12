# import psutil
# import time
# from colors import PURPLE, CYAN, MAGENTA, LIME, PINK, YELLOW, GREEN, RED, WHITE, GRAY, RESET
# import sys
# import time

# # ============================================================
# # Previous samples for disk and network rate calculations
# # ============================================================

# _previous_disk = psutil.disk_io_counters()
# _previous_disk_time = time.monotonic()

# _previous_net = psutil.net_io_counters()
# _previous_net_time = time.monotonic()


# # ============================================================
# # CPU
# # ============================================================

# def get_cpu():
#     aggregate_cpu = psutil.cpu_percent(interval=1)
#     per_core_cpu = psutil.cpu_percent(interval=1, percpu=True)
#     return {
#         f"aggregate": aggregate_cpu,
#         "per_core": per_core_cpu
#     }


# # ============================================================
# # Memory
# # ============================================================

# def get_memory():
#     memory_info = psutil.virtual_memory()

#     return {
#         "total": memory_info.total,
#         "available": memory_info.available,
#         "used": memory_info.used,
#         "percent": memory_info.percent
#     }


# # ============================================================
# # Processes
# # ============================================================

# def get_top_processes(n):
#     processes = []

#     # First measurement
#     for process in psutil.process_iter(
#         ["pid", "name", "memory_percent"]
#     ):
#         try:
#             process.cpu_percent(None)
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             pass

#     # Wait so CPU usage can be measured
#     time.sleep(1)

#     # Second measurement
#     for process in psutil.process_iter(
#         ["pid", "name", "memory_percent"]
#     ):
#         try:
#             cpu_percent = process.cpu_percent(None)

#             processes.append({
#                 "pid": process.info["pid"],
#                 "name": process.info["name"],
#                 "cpu_percent": cpu_percent,
#                 "memory_percent": process.info["memory_percent"]
#             })

#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             pass

#     # Highest CPU first
#     processes.sort(
#         key=lambda x: x["cpu_percent"],
#         reverse=True
#     )

#     return processes[:n]


# # ============================================================
# # Disk I/O
# # ============================================================

# def get_disk_io():
#     global _previous_disk
#     global _previous_disk_time

#     current_disk = psutil.disk_io_counters()
#     current_time = time.monotonic()

#     # Make sure psutil returned valid counters
#     if current_disk is None:
#         return {
#             "read_rate": 0.0,
#             "write_rate": 0.0
#         }

#     elapsed = current_time - _previous_disk_time

#     # Avoid division by zero
#     if elapsed <= 0:
#         return {
#             "read_rate": 0.0,
#             "write_rate": 0.0
#         }

#     # Calculate how many bytes were transferred
#     read_bytes = (
#         current_disk.read_bytes -
#         _previous_disk.read_bytes
#     )

#     write_bytes = (
#         current_disk.write_bytes -
#         _previous_disk.write_bytes
#     )

#     # Convert amount transferred into a rate
#     read_rate = read_bytes / elapsed
#     write_rate = write_bytes / elapsed

#     # IMPORTANT:
#     # Save current reading for the NEXT function call
#     _previous_disk = current_disk
#     _previous_disk_time = current_time

#     return {
#         "read_rate": read_rate,
#         "write_rate": write_rate
#     }


# # ============================================================
# # Network I/O
# # ============================================================

# def get_network_io():
#     global _previous_net
#     global _previous_net_time

#     current_net = psutil.net_io_counters()
#     current_time = time.monotonic()

#     if current_net is None:
#         return {
#             "sent_rate": 0.0,
#             "received_rate": 0.0
#         }

#     elapsed = current_time - _previous_net_time

#     if elapsed <= 0:
#         return {
#             "sent_rate": 0.0,
#             "received_rate": 0.0
#         }

#     # Calculate bytes transferred since previous sample
#     bytes_sent = (
#         current_net.bytes_sent -
#         _previous_net.bytes_sent
#     )

#     bytes_received = (
#         current_net.bytes_recv -
#         _previous_net.bytes_recv
#     )

#     # Convert to bytes/second
#     sent_rate = bytes_sent / elapsed
#     received_rate = bytes_received / elapsed

#     # Save current reading for NEXT call
#     _previous_net = current_net
#     _previous_net_time = current_time

#     return {
#         "sent_rate": sent_rate,
#         "received_rate": received_rate
#     }


# # ============================================================
# # Display / monitoring
# # ============================================================

# import sys
# import time

# # --- ANSI control sequences -------------------------------------------------
# ALT_SCREEN_ON  = "\x1b[?1049h"   # switch to the alternate screen buffer
# ALT_SCREEN_OFF = "\x1b[?1049l"   # switch back to the normal buffer (restores scrollback)
# HIDE_CURSOR    = "\x1b[?25l"
# SHOW_CURSOR    = "\x1b[?25h"
# CURSOR_HOME    = "\x1b[H"        # move cursor to row 1, col 1
# CLEAR_TO_END   = "\x1b[J"        # erase from cursor to end of screen (\x1b[0J)


# def start_monitoring():
#     # Enter the alt-screen buffer once, hide the cursor. This is the same
#     # trick htop/vim/less use so their UI paints in place and never leaks
#     # into (or gets pushed off by) your shell's scrollback history.
#     sys.stdout.write(ALT_SCREEN_ON + HIDE_CURSOR)
#     sys.stdout.flush()

#     try:
#         print(f"{MAGENTA}==========={RESET}")
#         print(f"{PINK}System Monitor{RESET}")
#         print(f"{MAGENTA}==========={RESET}")
#         print()

#         while True:
#             frame = []  # build the entire frame first, write it in ONE shot

#             # ---------------- CPU ----------------
#             cpu = get_cpu()
#             frame.append(f"{PURPLE}CPU{RESET}: {CYAN}{cpu['aggregate']}%{RESET}")
#             frame.append(f"{PURPLE}Per Core CPU Usage:{RESET}")
#             for i, usage in enumerate(cpu["per_core"]):
#                 frame.append(f"{GREEN}Core {i}{RESET}: {CYAN}{usage}%{RESET}")
#             frame.append("")

#             # ---------------- Memory ----------------
#             memory = get_memory()
#             frame.append(
#                 f"{PINK}Total Memory{RESET}: "
#                 f"{CYAN}{memory['total'] / (1024 ** 3):.2f} GB{RESET}"
#             )
#             frame.append(
#                 f"{MAGENTA}Available Memory:{RESET} "
#                 f"{CYAN}{memory['available'] / (1024 ** 3):.2f} GB{RESET}"
#             )
#             frame.append(
#                 f"{YELLOW}Used Memory:{RESET} "
#                 f"{CYAN}{memory['used'] / (1024 ** 3):.2f} GB{RESET}"
#             )
#             frame.append(
#                 f"{GREEN}Memory Usage:{RESET} "
#                 f"{CYAN}{memory['percent']}%{RESET}"
#             )
#             frame.append("")

#             # ---------------- Processes ----------------
#             processes = get_top_processes(5)
#             frame.append(f"{RED}Top 5 Processes by CPU:{RESET}")
#             frame.append("")
#             frame.append(
#                 f"{LIME}{'PID':<10}{RESET}"
#                 f"{PINK}{'Name':<20}{RESET}"
#                 f"{RED}{'CPU':<10}{RESET}"
#                 f"{LIME}{'Memory'}{RESET}"
#             )
#             for process in processes:
#                 frame.append(
#                     f"{PINK}{process['pid']:<10}{RESET}"
#                     f"{YELLOW}{process['name']:<20}{RESET}"
#                     f"{LIME}{process['cpu_percent']:<10.1f}{RESET}"
#                     f"{PURPLE}{process['memory_percent']:.1f}{RESET}"
#                     f"{GRAY}%{RESET}"
#                 )
#             frame.append("")

#             # ---------------- Disk ----------------
#             disk = get_disk_io()
#             frame.append(
#                 f"{MAGENTA}Read rate: {RESET} "
#                 f"{MAGENTA}{disk['read_rate']:.2f}{RESET} "
#                 f"{CYAN}bytes/sec{RESET}"
#             )
#             frame.append(
#                 f"{CYAN}Write rate:{RESET} "
#                 f"{PINK}{disk['write_rate']:.2f}{RESET} "
#                 f"{CYAN}bytes/sec{RESET}"
#             )
#             frame.append("")

#             # ---------------- Network ----------------
#             network = get_network_io()
#             frame.append(
#                 f"{YELLOW}Sent rate: {RESET}    "
#                 f"{GREEN}{network['sent_rate']:.2f} {RESET}"
#                 f"{CYAN}bytes/sec{RESET}"
#             )
#             frame.append(
#                 f"{RED}Received rate: {RESET} "
#                 f"{PINK}{network['received_rate']:.2f} {RESET}"
#                 f"{CYAN}bytes/sec{RESET}"
#             )
#             frame.append("")
#             frame.append(f"{LIME}=============================={RESET}")

#             # Home the cursor, erase everything below it, then paint the
#             # whole new frame in a single write+flush.
#             sys.stdout.write(CURSOR_HOME + CLEAR_TO_END + "\n".join(frame) + "\n")
#             sys.stdout.flush()

#             time.sleep(1)

#     except KeyboardInterrupt:
#         pass
#     finally:
#         # ALWAYS restore the terminal, even on Ctrl+C or an exception,
#         # or the user's shell will be left in the alt-screen state.
#         sys.stdout.write(SHOW_CURSOR + ALT_SCREEN_OFF)
#         sys.stdout.flush()


# if __name__ == "__main__":
#     start_monitoring()