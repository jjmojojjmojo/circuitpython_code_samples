# Using Simple State To Reduce Button Sample Frequency
from setup import check, led, rgb
import time

button_a = False
button_b = False

checkin = time.monotonic()

while True:
    if time.monotonic() - checkin > 0.2:
        button_a = check("A")
        button_b = check("B")
        checkin = time.monotonic()
        
    if button_a:
        print("Button 'A' pressed")
        
    if button_b:
        print("Button 'B' pressed")