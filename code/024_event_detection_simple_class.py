# Button Event Detection: Using Classes
from setup import check, led, rgb
import time

class AButtonEvents:
    _debounce = 0.2
    
    def __init__(self):
        self.state = False
        self.checkin = time.monotonic()

    def press(self):
        print("'A' button pressed")
        
    def release(self):
        print("'A' button released")
    
    def update(self):
        if time.monotonic() - self.checkin > self._debounce:
            if not self.state and check("A"):
                self.press()
                
            if self.state and not check("A"):
                self.release()
                
            self.state = check("A")
            
            self.checkin = time.monotonic()
            
class BButtonEvents:
    _debounce = 0.2
    
    def __init__(self):
        self.state = False
        self.checkin = time.monotonic()

    def press(self):
        print("'B' button pressed")
        
    def release(self):
        print("'B' button released")
    
    def update(self):
        if time.monotonic() - self.checkin > self._debounce:
            if not self.state and check("B"):
                self.press()
                
            if self.state and not check("B"):
                self.release()
                
            self.state = check("B")
            
            self.checkin = time.monotonic()
        
b = BButtonEvents()
a = AButtonEvents()

while True:
    a.update()
    b.update()