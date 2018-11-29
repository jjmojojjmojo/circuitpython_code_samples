# Using The Constructor To Configure Instances
from setup import thermistor, photocell, rgb, check
import time

def fahrenheit(value):
    return (value * (9/5)) + 32
    
class AnalogEventsWithColor:
    def __init__(self, threshold=1.0, sample_rate=2.0, low=21845, high=43690, colors=None):
        self.state = None
        self.previous = None
        self.range = None
        self.previous_range = None
        
        self.sample_rate = sample_rate
        self.threshold = threshold
        
        self.color = (0, 0, 0)
        
        self._ranges = {
            'low': low,
            'high': high
        }
        
        if colors is None:
            self.colors = {
                'low': (0, 0, 255),    # blue
                'medium': (0, 255, 0), # green
                'high': (255, 0, 0)    # red
            }
        else:
            self.colors = colors
        
        self.checkin = time.monotonic()
        
        self.sample()
        self.set_range()
        self.dispatch()
    
    def high(self):
        pass
        
    def medium(self):
        pass
        
    def high(self):
        pass
        
    def changed(self):
        pass
    
    def sample(self):
        pass
        
    def set_range(self):
        self.previous_range = self.range
        
        if self.value <= self._ranges["low"]:
            self.range = "low"
            self.color = self.colors["low"]
        elif self._ranges["low"] < self.value <= self._ranges["high"]:
            self.range = "medium"
            self.color = self.colors["medium"]
        elif self.value > self._ranges["high"]:
            self.range = "high"
            self.color = self.colors["high"]
            
    def dispatch(self):
        if self.range != self.previous_range:
            self.changed()
            
            if self.range == "low":
                self.low()
            elif self.range == "medium":
                self.medium()
            elif self.range == "high":
                self.high()
                
    def update(self):
        if time.monotonic() - self.checkin > self.sample_rate:
            self.previous = self.value
            self.sample()
            self.checkin = time.monotonic()
        
            if abs(self.previous - self.value) >= self.threshold:
                self.set_range()
                self.dispatch()
        

class ThermistorEvents(AnalogEventsWithColor):        
    def sample(self):
        self.value = fahrenheit(thermistor.temperature)   

class PhotocellEvents(AnalogEventsWithColor):
    def sample(self):
        self.value = photocell.value 

class State:
    _debounce = 0.2
    
    def __init__(self):
        self.a = check("A")
        self.b = check("B")
        self.enabled = True
        self.mode = "temperature"
        
        self.checkin = time.monotonic()
        
    def update(self):
        if time.monotonic() - self.checkin > self._debounce:
            if self.a and not check("A"):
                self.enabled = not self.enabled
                
            if self.b and not check("B"):
                if self.mode == "temperature":
                    self.mode = "light"
                else:
                    self.mode = "temperature"
                    
            self.a = check("A")
            self.b = check("B")
            
            self.checkin = time.monotonic()

thermistor_events = ThermistorEvents(
    threshold=1.0, 
    sample_rate=2.0, 
    low=59.0, 
    high=77.0)

photocell_events = PhotocellEvents(
    threshold=10.0, 
    sample_rate=0.1,
    colors={
        'high': (255, 0, 255),  # purple
        'medium': (255,140,0),  # orange
        'low': (255, 255, 255)  # white 
    })

state = State()

while True:
    thermistor_events.update()
    photocell_events.update()
    state.update()
    
    if state.enabled:
        if state.mode == "temperature":
            rgb[0] = thermistor_events.color
        else:
            rgb[0] = photocell_events.color
    else:
        rgb[0] = (0, 0, 0)