# GEMMA button multiplexing test
import board
import time
import analogio

def voltage(value):
    return round((value * 3.3) / 65536, 2)

def print_button(pin):
    count = voltage(pin.value)
    if abs(count - 1.0) < 0.1:
        print("'A' button pressed")
    
    if abs(count - 2.8) < 0.1:
        print("'B' button pressed")
    

buttons = analogio.AnalogIn(board.A0)

while True:
    print_button(buttons)
    
    time.sleep(0.2)