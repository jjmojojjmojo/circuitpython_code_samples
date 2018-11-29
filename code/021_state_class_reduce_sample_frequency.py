# Using A Class To Track Button State At A Reduced Sample Frequency
from setup import check, led, rgb
import time

class State:
    def __init__(self):
        self.a = False
        self.b = False
        self.checkin = time.monotonic()
        
    def update(self):
        if time.monotonic() - self.checkin > 0.2:
            self.a = check("A")
            self.b = check("B")
            self.checkin = time.monotonic()
            
            if state.a:
                print("Button 'A' pressed")
                
            if state.b:
                print("Button 'B' pressed")

state = State()

while True:
    state.update()