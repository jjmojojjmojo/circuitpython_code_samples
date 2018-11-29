from setup import thermistor, photocell, rgb, check
import time

def fahrenheit(value):
    return (value * (9/5)) + 32
    
class AnalogEvents:
    _threshold = 1.0
    _sample_rate = 2.0
    _ranges = {
        "low": 21845,
        "high": 43690
    }
    
    def __init__(self):
        self.state = None
        self.previous = None
        self.range = None
        self.previous_range = None
        
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
        elif self._ranges["low"] < self.value <= self._ranges["high"]:
            self.range = "medium"
        elif self.value > self._ranges["high"]:
            self.range = "high"
            
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
        if time.monotonic() - self.checkin > self._sample_rate:
            self.previous = self.value
            self.sample()
            self.checkin = time.monotonic()
        
            if abs(self.previous - self.value) >= self._threshold:
                self.set_range()
                self.dispatch()
        

class ThermistorEvents(AnalogEvents):
    _threshold = 1.0
    _sample_rate = 2.0
    
    _ranges = {
        "low": 59.0,
        "high": 77.0
    }
    
    def __init__(self):
        self.color = (0, 0, 0)
        AnalogEvents.__init__(self)
        
    def sample(self):
        self.value = fahrenheit(thermistor.temperature)
        
    def high(self):
        self.color = (255, 0, 0) # red
        
    def medium(self):
        self.color = (0, 255, 0) # green
        
    def low(self):
        self.color = (0, 0, 255) # blue
            
            

class PhotocellEvents(AnalogEvents):
    _threshold = 10.0
    _sample_rate = 0.1
    
    def __init__(self):
        self.color = (0, 0, 0)
        AnalogEvents.__init__(self)
        
    def sample(self):
        self.value = photocell.value
        
    def high(self):
        self.color = (255, 0, 255) # purple
        
    def medium(self):
        self.color = (255,140,0) # orange
        
    def low(self):
        self.color = (255, 255, 255) # white   

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

thermistor_events = ThermistorEvents()
photocell_events = PhotocellEvents()
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