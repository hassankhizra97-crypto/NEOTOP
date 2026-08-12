from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, ProgressBar, Sparkline
from textual.widget import Widget


class CpuWidget(Widget):
    """Displays aggregate and per-core CPU usage."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cpu_history = []

    def compose(self) -> ComposeResult:
        yield Label("CPU", id="cpu-title")
        yield Label("Usage: 0%", id="cpu-usage")
        yield ProgressBar(total=100, show_eta=False, id="cpu-progress")
        yield Label("History", id="cpu-history-label")
        yield Sparkline([], id="cpu-sparkline")
        yield Label("Per Core CPU Usage", id="core-title")
        yield Vertical(id="core-container")

    def update_cpu(self, cpu_data):
        """Update the widget with data returned by stats.get_cpu()."""

        aggregate = cpu_data["aggregate"]
        per_core = cpu_data["per_core"]

        # Update aggregate CPU percentage
        self.query_one("#cpu-usage", Label).update(
            f"Usage: {aggregate:.1f}%"
        )

        # Update progress bar
        self.query_one("#cpu-progress", ProgressBar).update(
            progress=aggregate
        )

        # Keep recent CPU values for the sparkline
        self.cpu_history.append(aggregate)

        # Keep only the last 30 readings
        self.cpu_history = self.cpu_history[-30:]

        self.query_one("#cpu-sparkline", Sparkline).data = self.cpu_history

        # Update per-core values
        core_container = self.query_one("#core-container", Vertical)

        core_container.remove_children()

        for core_number, usage in enumerate(per_core):
            core_container.mount(
                Label(
                    f"Core {core_number}: {usage:.1f}%",
                    classes="core-usage",
                )
            )