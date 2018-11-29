# Extreme Configuration and DI Example
from setup import thermistor, photocell, rgb, check
import time

THERMISTOR = 1
PHOTOCELL = 2
BUTTON_A = 3
BUTTON_B = 4
THERMISTOR_COLOR = 5
PHOTOCELL_COLOR = 6

class State:
    def __init__(self):
        self.mode = "temperature"
        self.enabled = True
        
        self._previous = {
            BUTTON_A: False,
            BUTTON_B: False,
            THERMISTOR: self.check(THERMISTOR),
            PHOTOCELL: self.check(PHOTOCELL),
            THERMISTOR_COLOR: (0, 0, 0),
            PHOTOCELL_COLOR: (0, 0, 0)
        }
        self._external = {
            BUTTON_A: False,
            BUTTON_B: False,
            THERMISTOR: self.check(THERMISTOR),
            PHOTOCELL: self.check(PHOTOCELL),
            THERMISTOR_COLOR: (0, 0, 0),
            PHOTOCELL_COLOR: (0, 0, 0)
        }
    
    def toggle_mode(self):
        if self.mode == "temperature":
            self.mode = "light"
        else:
            self.mode = "temperature"
            
    
    def toggle_enabled(self):
        self.enabled = not self.enabled
    
    def get(self, what):
        return self._external[what]
        
    def previous(self, what):
        return self._previous[what]
        
    def set(self, what, value=None):
        self._previous[what] = self._external[what]
        
        if value is None:
            self._external[what] = self.check(what)
        else:
            self._external[what] = value
        
        return self._external[what]
    
    def check(self, what):
        if what == THERMISTOR:
            return self.temperature()
            
        if what == PHOTOCELL:
            return photocell.value
            
        if what == BUTTON_A:
            return check("A")
            
        if what == BUTTON_B:
            return check("B")
            
    
    def temperature(self):
        return (thermistor.temperature * (9/5)) + 32

class AnalogHandlersWithColor:
    def __init__(self, state, token, colors=None):
        self.state = state
        self.token = token
        
        self.previous_range = None
        
        if colors is None:
            self.colors = {
                'low': (0, 0, 255),    # blue
                'medium': (0, 255, 0), # green
                'high': (255, 0, 0)    # red
            }
        else:
            self.colors = colors
    
    def high(self):
        pass
        
    def low(self):
        pass
    
    def medium(self):
        pass
        
    def changed(self):
        pass
    
    def dispatch(self, range):
        if range != self.previous_range:
            self.changed()
            
            if range == "low":
                self.state.set(self.token, self.colors["low"])
                self.low()
            elif range == "medium":
                self.state.set(self.token, self.colors["medium"])
                self.medium()
            elif range == "high":
                self.state.set(self.token, self.colors["high"])
                self.high()
                
            self.previous_range = range

class PrintHandlersWithColor(AnalogHandlersWithColor):
    def high(self):
        print("'HIGH' event detected with token", self.token)
    

class ButtonEvents:
    _debounce = 0.2
    
    def __init__(self, state, token, onpress=None, onrelease=None):
        self.checkin = time.monotonic()
        self._press = onpress
        self._release = onrelease
        
        self.token = token
        self.state = state
    
    def press(self):
        if self._press is not None:
            self._press()
            
    def release(self):
        if self._release is not None:
            self._release()
    
    def update(self):
        if time.monotonic() - self.checkin > self._debounce:
            if not self.state.get(self.token) and self.state.check(self.token):
                self.press()
                
            if self.state.get(self.token) and not self.state.check(self.token):
                self.release()
                
            self.state.set(self.token)
            
            self.checkin = time.monotonic()
    
class AnalogEvents:
    def __init__(self, state, token, handlers, threshold=1.0, sample_rate=2.0, low=21845, high=43690):
        self.range = None
        
        self.token = token
        self.state = state
        
        self.sample_rate = sample_rate
        self.threshold = threshold
        
        self.handlers = handlers
        
        self._ranges = {
            'low': low,
            'high': high
        }
        
        self.checkin = time.monotonic()
        
        self.state.set(self.token)
        self.set_range()
        self.dispatch()
    
    def dispatch(self):
        self.handlers.dispatch(self.range)
        
    def set_range(self):
        value = self.state.get(self.token)
        if value <= self._ranges["low"]:
            self.range = "low"
        elif self._ranges["low"] < value <= self._ranges["high"]:
            self.range = "medium"
        elif value > self._ranges["high"]:
            self.range = "high"
    
    def update(self):
        if time.monotonic() - self.checkin > self.sample_rate:
            self.state.set(self.token)
            self.checkin = time.monotonic()
        
            if abs(self.state.previous(self.token) - self.state.get(self.token)) >= self.threshold:
                self.set_range()
                self.dispatch()
        

state = State()

a_button = ButtonEvents(state, BUTTON_A, onrelease=state.toggle_enabled)
b_button = ButtonEvents(state, BUTTON_B, onrelease=state.toggle_mode)

thermistor_events = AnalogEvents(
    state=state,
    token=THERMISTOR,
    handlers=AnalogHandlersWithColor(
        state, 
        THERMISTOR_COLOR),
    threshold=1.0, 
    sample_rate=2.0, 
    low=59.0, 
    high=77.0)
    
photocell_events = AnalogEvents(
    state,
    PHOTOCELL,
    threshold=10.0, 
    sample_rate=0.1,
    handlers=PrintHandlersWithColor(
        state, 
        PHOTOCELL_COLOR,
        colors={
        'high': (255, 0, 255),  # purple
        'medium': (255,140,0),  # orange
        'low': (255, 255, 255)  # white 
    }))

while True:
    thermistor_events.update()
    photocell_events.update()
    a_button.update()
    b_button.update()
    
    if state.enabled:
        if state.mode == "temperature":
            rgb[0] = state.get(THERMISTOR_COLOR)
        else:
            rgb[0] = state.get(PHOTOCELL_COLOR)
    else:
        rgb[0] = (0, 0, 0)