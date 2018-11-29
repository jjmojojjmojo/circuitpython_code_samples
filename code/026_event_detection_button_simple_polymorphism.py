# Event Detection Using Polymorphism
from setup import check
import time

class ButtonEvents:
    _debounce = 0.2
    
    def __init__(self):
        self.state = False
        self.checkin = time.monotonic()

    def press(self):
        pass
        
    def release(self):
        pass
        
    def check(self):
        pass
    
    def update(self):
        if time.monotonic() - self.checkin > self._debounce:
            if not self.state and self.check():
                self.press()
                
            if self.state and not self.check():
                self.release()
                
            self.state = self.check()
            
            self.checkin = time.monotonic()

class AButtonEvents(ButtonEvents):
    def check(self):
        return check("A")
    
    def release(self):
        print("Released 'A': this is a special method override event!")
    
    
class BButtonEvents(ButtonEvents):
    def check(self):
        return check("B")
        
    def press(self):
        print("Pressed 'B', in a very special method.")

b = BButtonEvents()
a = AButtonEvents()

while True:
    a.update()
    b.update()