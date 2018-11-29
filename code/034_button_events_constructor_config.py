# Using Dependency Injection To Configure The Event Handlers
from setup import thermistor, photocell, rgb, check
import time

def fahrenheit(value):
    return (value * (9/5)) + 32

class ButtonEvents:
    _debounce = 0.2
    
    def __init__(self, check, onpress=None, onrelease=None):
        self.checkin = time.monotonic()
        self._press = onpress
        self._release = onrelease
        self._check = check
        
        self.state = False

    def check(self):
        return self._check()
    
    def press(self):
        if self._press is not None:
            self._press()
            
    def release(self):
        if self._release is not None:
            self._release()
    
    def update(self):
        if time.monotonic() - self.checkin > self._debounce:
            if not self.state and self.check():
                self.press()
                
            if self.state and not self.check():
                self.release()
                
            self.state = self.check()
            
            self.checkin = time.monotonic()
    
class AnalogEventsWithColor:
    def __init__(self, sample, threshold=1.0, sample_rate=2.0, low=21845, high=43690, colors=None, onchange=None, onhigh=None, onlow=None, onmedium=None):
        self.value = None
        self.previous = None
        self.range = None
        self.previous_range = None
        
        self.sample_rate = sample_rate
        self.threshold = threshold
        
        self._sample = sample
        self._high = onhigh
        self._medium = onmedium
        self._low = onlow
        self._changed = onchange
        
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
        if self._high is not None:
            self._high()
            
    def medium(self):
        if self._medium is not None:
            self._medium()
        
    def low(self):
        if self._low is not None:
            self._low()
        
    def changed(self):
        if self._changed is not None:
            self._changed()
    
    def sample(self):
        self.previous = self.value
        self.value = self._sample()
        
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
            self.sample()
            self.checkin = time.monotonic()
        
            if abs(self.previous - self.value) >= self.threshold:
                self.set_range()
                self.dispatch()
        
        
def temperature_sample():
    return fahrenheit(thermistor.temperature)   

def light_sample():
    return photocell.value 

thermistor_events = AnalogEventsWithColor(
    sample=temperature_sample,
    threshold=1.0, 
    sample_rate=2.0, 
    low=59.0, 
    high=77.0)

photocell_events = AnalogEventsWithColor(
    sample=light_sample,
    threshold=10.0, 
    sample_rate=0.1,
    colors={
        'high': (255, 0, 255),  # purple
        'medium': (255,140,0),  # orange
        'low': (255, 255, 255)  # white 
    })

class State:
    def __init__(self):
        self.mode = "temperature"
        self.enabled = True
        
    def toggle_mode(self):
        if self.mode == "temperature":
            self.mode = "light"
        else:
            self.mode = "temperature"
            
    def toggle_enabled(self):
        self.enabled = not self.enabled

def check_a():
    return check("A")
    
def check_b():
    return check("B")

state = State()

a_button = ButtonEvents(check_a, onrelease=state.toggle_enabled)
b_button = ButtonEvents(check_b, onrelease=state.toggle_mode)

while True:
    thermistor_events.update()
    photocell_events.update()
    a_button.update()
    b_button.update()
    
    if state.enabled:
        if state.mode == "temperature":
            rgb[0] = thermistor_events.color
        else:
            rgb[0] = photocell_events.color
    else:
        rgb[0] = (0, 0, 0)