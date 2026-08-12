from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class DiskWidget(Widget):
    """Displays disk read and write rates."""

    def compose(self) -> ComposeResult:
        yield Label("DISK I/O", id="disk-title")
        yield Label("Read: 0.00 bytes/sec", id="disk-read")
        yield Label("Write: 0.00 bytes/sec", id="disk-write")

    def update_disk(self, disk_data):
        """Update the widget with data from stats.get_disk_io()."""

        read_rate = disk_data["read_rate"]
        write_rate = disk_data["write_rate"]

        self.query_one("#disk-read", Label).update(
            f"Read: {read_rate:.2f} bytes/sec"
        )

        self.query_one("#disk-write", Label).update(
            f"Write: {write_rate:.2f} bytes/sec"
        )