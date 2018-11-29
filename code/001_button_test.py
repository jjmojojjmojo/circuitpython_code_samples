# Code to test buttons (general)
import board
from digitalio import DigitalInOut, Direction, Pull
import time

a_button = DigitalInOut(board.D11)
a_button.direction = Direction.INPUT
a_button.pull = Pull.UP

b_button = DigitalInOut(board.D7)
b_button.direction = Direction.INPUT
b_button.pull = Pull.UP

while True:
    if not a_button.value:
        print("'A' button pressed.")
        
    if not b_button.value:
        print("'B' button pressed.")
    
    time.sleep(0.2)