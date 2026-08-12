from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, ProgressBar


class MemoryWidget(Widget):
    """Displays system memory usage."""

    def compose(self) -> ComposeResult:
        yield Label("MEMORY", id="memory-title")

        yield Label("Total: 0.00 GB", id="memory-total")
        yield Label("Used: 0.00 GB", id="memory-used")
        yield Label("Available: 0.00 GB", id="memory-available")
        yield Label("Usage: 0.0%", id="memory-percent")

        yield ProgressBar(
            total=100,
            show_eta=False,
            id="memory-progress",
        )

    def update_memory(self, memory_data):
        """Update the widget with data returned by stats.get_memory()."""

        total = memory_data["total"]
        used = memory_data["used"]
        available = memory_data["available"]
        percent = memory_data["percent"]

        # Convert bytes → GB
        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        available_gb = available / (1024 ** 3)

        # Update labels
        self.query_one("#memory-total", Label).update(
            f"Total: {total_gb:.2f} GB"
        )

        self.query_one("#memory-used", Label).update(
            f"Used: {used_gb:.2f} GB"
        )

        self.query_one("#memory-available", Label).update(
            f"Available: {available_gb:.2f} GB"
        )

        self.query_one("#memory-percent", Label).update(
            f"Usage: {percent:.1f}%"
        )

        # Update progress bar
        self.query_one("#memory-progress", ProgressBar).update(
            progress=percent
        )