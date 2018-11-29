# Code to test the red LED on pin 13
import board
from digitalio import DigitalInOut, Direction, Pull
import time

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

while True:
    led.value = not led.value
    
    time.sleep(0.5)