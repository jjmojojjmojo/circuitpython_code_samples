# Code to test buttons - CircuitPlayground Express
import board
from digitalio import DigitalInOut, Direction, Pull
import time

a_button = DigitalInOut(board.D4)
a_button.direction = Direction.INPUT
a_button.pull = Pull.DOWN

b_button = DigitalInOut(board.D5)
b_button.direction = Direction.INPUT
b_button.pull = Pull.DOWN

while True:
    if a_button.value:
        print("'A' button pressed.")
        
    if b_button.value:
        print("'B' button pressed.")
    
    time.sleep(0.2)