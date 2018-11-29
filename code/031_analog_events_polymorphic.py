# Analog Event Detection: Implemtation That Changes The RGB LED Depending On The Range
from setup import thermistor, photocell
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
        
    def sample(self):
        self.value = fahrenheit(thermistor.temperature)
        
    def high(self):
        print("'High' temperature event detected")
        
    def medium(self):
        print("'Medium' temperature event detected")
        
    def low(self):
        print("'Low' temperature event detected")
    
    def changed(self):
        print("'Changed' temperature event detected")
            
            

class PhotocellEvents(AnalogEvents):
    _threshold = 10.0
    _sample_rate = 0.1
        
    def sample(self):
        self.value = photocell.value
        
    def high(self):
        print("'High' light event detected")
        
    def medium(self):
        print("'Medium' light event detected")
        
    def low(self):
        print("'Low' light event detected")
    
    def changed(self):
        print("'Changed' light event detected")    

thermistor_events = ThermistorEvents()
photocell_events = PhotocellEvents()

checkin = time.monotonic()
print("({}, {})".format(thermistor_events.value, photocell_events.value))

while True:
    thermistor_events.update()
    photocell_events.update()
    
    if time.monotonic() - checkin > 1.0:
        print("({}, {})".format(thermistor_events.value, photocell_events.value))
        checkin = time.monotonic()