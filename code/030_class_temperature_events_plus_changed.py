﻿# Analog Event Detection: Adding A "changed" Event
from setup import thermistor
import time

def fahrenheit(value):
    return (value * (9/5)) + 32

class ThermistorEvents:
    _threshold = 1.0
    _sample_rate = 2.0
    
    def __init__(self):
        self.state = round(thermistor.temperature)
        self.previous = self.state
        self.value = self.state
        
        self.range = None
        self.previous_range = None
        
        self.checkin = time.monotonic()
        
        self.set_range()
        self.dispatch()
        
    def high(self):
        print("'High' event detected")
        
    def medium(self):
        print("'Medium' event detected")
        
    def low(self):
        print("'Low' event detected")
    
    def changed(self):
        print("'Changed' event detected")
    
    def set_range(self):
        self.previous_range = self.range
        
        if self.value <= 15:
            self.range = "low"
        elif 15 < self.value <= 25:
            self.range = "medium"
        elif self.value > 25:
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
            self.value = round(thermistor.temperature)
            self.checkin = time.monotonic()
        
            if abs(self.previous - self.value) >= self._threshold:
                self.set_range()
                self.dispatch()
            

events = ThermistorEvents()

checkin = time.monotonic()
print("({})".format(fahrenheit(events.value)))

while True:
    events.update()
    
    if time.monotonic() - checkin > 1.0:
        print("({})".format(fahrenheit(events.value)))
        checkin = time.monotonic()