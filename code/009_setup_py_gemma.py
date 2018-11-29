# setup.py for the GEMMA M0
import board
from digitalio import DigitalInOut, Direction, Pull
import adafruit_dotstar
import analogio
import adafruit_thermistor

thermistor = adafruit_thermistor.Thermistor(board.A1, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
photocell = analogio.AnalogIn(board.A2)

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

rgb = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
rgb.brightness = 0.3

buttons = analogio.AnalogIn(board.A0)

def voltage(pin):
    return round((pin.value * 3.3) / 65536, 2)

def check(token):
    if token == "A" and abs(voltage(buttons) - 1.0) < 0.1:
        return True
        
    if token == "B" and abs(voltage(buttons) - 2.8) < 0.1:
        return True
    
    return False