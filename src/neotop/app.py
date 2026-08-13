from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.binding import Binding
from . import stats
from .widgets.cpu import CpuWidget
from .widgets.memory import MemoryWidget
from .widgets.processes import ProcessTableWidget
from .widgets.disk import DiskWidget
from .widgets.network import NetworkWidget

class NeotopApp(App):
    """Main neotop application."""

    CSS_PATH = "styles/neotop.tcss"
    BINDINGS = [
        # Syntax: Binding("key_combination", "action_name", "description")
        Binding("q", "quit", "Quit App"),
    ]
    def action_quit_app(self) -> None:
        self.exit()

    def compose(self) -> ComposeResult:
        yield Grid(
            CpuWidget(id="cpu"),
            # MemoryWidget(id="memory"),
            # ProcessTableWidget(id="processes"),
            # DiskWidget(id="disk"),
            # NetworkWidget(id="network"),
        )

    def on_mount(self) -> None:
        # Initialize process CPU measurements before
        # collecting the first real reading.
        stats.initialize_processes()

        # Refresh system statistics every second.
        self.set_interval(1, self.refresh_stats)

        # Get the first reading immediately.
        self.refresh_stats()

    def refresh_stats(self) -> None:
        """Get new system data and send it to the widgets."""

        # Get data from stats.py
        cpu_data = stats.get_cpu()
        # memory_data = stats.get_memory()
        # processes_data = stats.get_top_processes(5)
        # disk_data = stats.get_disk_io()
        # network_data = stats.get_network_io()

        # Get widgets
        cpu_widget = self.query_one("#cpu", CpuWidget)
        # memory_widget = self.query_one("#memory", MemoryWidget)
        # process_widget = self.query_one(
        #     "#processes",
        #     ProcessTableWidget,
        # )
        # disk_widget = self.query_one("#disk", DiskWidget)
        # network_widget = self.query_one(
        #     "#network",
        #     NetworkWidget,
        # )

        # Send new data to each widget
        cpu_widget.update_cpu(cpu_data)
        # memory_widget.update_memory(memory_data)
        # process_widget.update_processes(processes_data)
        # disk_widget.update_disk(disk_data)
        # network_widget.update_network(network_data)


if __name__ == "__main__":
    NeotopApp().run()

