# Button Event Detection: Simple Variables
from setup import check
import time

checkin = time.monotonic()
a = False
b = False

while True:
    if time.monotonic() - checkin > 0.2:
        if not a and check("A"):
            print("'A' button pressed")
            
        if a and not check("A"):
            print("'A' button released")
        
        if not b and check("B"):
            print("'B' button pressed")
            
        if b and not check("B"):
            print("'B' button released")
            
        a = check("A")
        b = check("B")
        checkin = time.monotonic()
        
        