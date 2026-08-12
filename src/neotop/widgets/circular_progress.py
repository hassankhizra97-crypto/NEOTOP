from textual.widget import Widget
import math 

class CircularProgress(Widget):
    def __init__(self,percentage:float=0):
        super().__init__()
        self.percentage=percentage

    def draw_cricle(percentage):
        

        angle = math.radians(percentage / 100 * 360)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

    def render(self):
        yield Grid(
        )


    
    
