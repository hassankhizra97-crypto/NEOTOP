from textual.widget import Widget
import math 
from textual.containers import Grid

import math

from textual.widget import Widget


class CircularProgress(Widget):

    def __init__(self, percentage: float = 0) -> None:
        super().__init__()
        self.percentage = max(0, min(percentage, 100))

    def draw_circle(self):
        width = self.size.width
        height = self.size.height

        if width <= 0 or height <= 0:
            return []

        # Create an empty canvas.
        canvas = [
            [" " for _ in range(width)]
            for _ in range(height)
        ]

        # Find the center of the widget.
        center_x = width / 2
        center_y = height / 2

        # Leave a little space around the edges.
        radius = min(width / 2, height / 2) - 1

        # Terminal characters are usually taller than they are wide,
        # so compensate for the difference.
        radius_x = radius
        radius_y = radius * 0.5

        # Convert percentage into the amount of the circle to draw.
        progress_angle = (self.percentage / 100) * 360

        # Number of points used to construct the circle.
        steps = max(360, int(radius * 20))

        for i in range(steps):

            # Current angle in degrees.
            angle = (i / steps) * 360

            # Only draw the active part of the circle.
            if angle > progress_angle:
                continue

            # Convert degrees to radians.
            radians = math.radians(angle)

            # Calculate the position of this point.
            x = round(
                center_x + radius_x * math.cos(radians)
            )

            y = round(
                center_y + radius_y * math.sin(radians)
            )

            # Make sure the coordinate is inside the widget.
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = "●"

        return canvas

    def render(self):
        canvas = self.draw_circle()

        return "\n".join(
            "".join(row)
            for row in canvas
        )