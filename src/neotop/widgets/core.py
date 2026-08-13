from textual.app import ComposeResult
from textual.containers import Horizontal,Vertical
from textual.widgets import Label, ProgressBar, Sparkline
from textual.widget import Widget


class CoreWidget(Widget):
    """Displays per-core CPU usage."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._num_cores = 0 

    def compose(self)->ComposeResult:
        yield Label("Per Core CPU Usage", id="core-title")
        yield Vertical(id="core-container")
    def update_per_core(self,cpu_data):
        per_core = cpu_data["per_core"]
        # Update per-core values
        core_container = self.query_one("#core-container", Vertical)
        
        if len(per_core) != self._num_cores:
            # First run, or core count changed - (re)build one row per core
            core_container.remove_children()
            for core_number in range(len(per_core)):
                row = Horizontal(classes="core-row")
                core_container.mount(row)
                row.mount(Label(f"Core {core_number}:0.0%", id=f"core-label--{core_number}",classes="core-label"))
                row.mount(
                    ProgressBar(
                        total=100,
                        show_eta=False,
                        id=f"core-progress-{core_number}",
                        classes="core-progress",
                    )
                )
                core_container.mount(row)

            self._num_cores = len(per_core)

        for core_number, usage in enumerate(per_core):

            label = self.query_one(
                f"#core-label--{core_number}",
                Label,
            )

            progress_bar = self.query_one(
                f"#core-progress-{core_number}",
                ProgressBar,
            )

            label.update(f"Core {core_number}: {usage:.1f}%")
            progress_bar.update(progress=usage)