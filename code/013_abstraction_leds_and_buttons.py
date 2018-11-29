# The setup.py Abstraction In Practice
from setup import check, led, rgb
import time

while True:
    if check("A"):
        led.value = True
    else:
        led.value = False
        
    if check("B"):
        rgb[0] = (255, 255, 255)
    else:
        rgb[0] = (0, 0, 0)