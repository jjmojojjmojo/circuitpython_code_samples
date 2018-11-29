# Using Mutiple Samples To Smooth Out Photocell Signal
from setup import photocell
import time

sample_checkin = time.monotonic()
smoothing_checkin = time.monotonic()

value = photocell.value
previous = value
smoothed = value

while True:
    if time.monotonic() - smoothing_checkin > 0.1:
        print("({})".format(smoothed))
        smoothing_checkin = time.monotonic()
    
    if time.monotonic() - sample_checkin > 0.5:
        previous = value
        value = photocell.value
        sample_checkin = time.monotonic()
        
    if abs(previous - value)/previous >= 0.05:
        smoothed = value