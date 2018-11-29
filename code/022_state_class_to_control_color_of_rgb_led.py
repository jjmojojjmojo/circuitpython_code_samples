# Using State To Control The Color Of The RGB LED
from setup import check, led, rgb
import time

class State:
    _colors = (
        (255, 255, 255),  # white
        (148, 0, 211),    # violet
        (255, 0, 255),    # purple
        (0, 0, 255),      # blue
        (150, 191, 51),   # blue_green
        (0, 255, 0),      # green
        (255, 0, 0),      # red
        (226, 87, 30),    # ornange_red
        (255,140,0),      # orange
        (255, 255, 0)     # yellow
    )                       
    
    def __init__(self):
        self.a = False
        self.b = False
        self.color = None
        self._index = -1
        self.enabled = False
        self.checkin = time.monotonic()
        self.rotate_color()
        
    def rotate_color(self):
        self._index += 1
        
        if self._index >= len(self._colors):
            self._index = 0
            
        self.color = self._colors[self._index]
        
    def update(self):
        if time.monotonic() - self.checkin > 0.2:
            self.a = check("A")
            self.b = check("B")
            self.checkin = time.monotonic()
            
            if state.a:
                self.enabled = not self.enabled
                
            if state.b:
                self.rotate_color()

state = State()

while True:
    state.update()
    
    if state.enabled:
        rgb[0] = state.color
    else:
        rgb[0] = (0, 0, 0)
        