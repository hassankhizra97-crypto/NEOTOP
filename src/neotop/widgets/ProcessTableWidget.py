from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, Label


class ProcessTableWidget(Widget):
    """Displays the top processes by CPU usage."""

    def compose(self) -> ComposeResult:
        yield Label("TOP PROCESSES BY CPU", id="process-title")
        yield DataTable(id="process-table")

    def on_mount(self) -> None:
        """Set up the process table columns."""

        table = self.query_one("#process-table", DataTable)

        table.add_columns(
            "PID",
            "Name",
            "CPU %",
            "Memory %",
        )

    def update_processes(self, processes):
        """Update the table with data from stats.get_top_processes()."""

        table = self.query_one("#process-table", DataTable)

        # Remove the old rows
        table.clear()

        # Add the newest processes
        for process in processes:
            table.add_row(
                str(process["pid"]),
                process["name"],
                f"{process['cpu_percent']:.1f}",
                f"{process['memory_percent']:.1f}",
            )