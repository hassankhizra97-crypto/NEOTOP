from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class NetworkWidget(Widget):
    """Displays network upload and download rates."""

    def compose(self) -> ComposeResult:
        yield Label("NETWORK", id="network-title")
        yield Label("↑ Sent: 0.00 bytes/sec", id="network-sent")
        yield Label("↓ Received: 0.00 bytes/sec", id="network-received")

    def update_network(self, network_data):
        """Update the widget with data from stats.get_network_io()."""

        sent_rate = network_data["sent_rate"]
        received_rate = network_data["received_rate"]

        self.query_one("#network-sent", Label).update(
            f"↑ Sent: {sent_rate:.2f} bytes/sec"
        )

        self.query_one("#network-received", Label).update(
            f"↓ Received: {received_rate:.2f} bytes/sec"
        )