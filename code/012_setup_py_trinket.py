# setup.py For The Trinket M0
import board
from digitalio import DigitalInOut, Direction, Pull
import adafruit_dotstar
import adafruit_thermistor
import analogio

thermistor = adafruit_thermistor.Thermistor(board.D3, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
photocell = analogio.AnalogIn(board.D0)

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

rgb = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
rgb.brightness = 0.3

a_button = DigitalInOut(board.D1)
a_button.direction = Direction.INPUT
a_button.pull = Pull.UP

b_button = DigitalInOut(board.D2)
b_button.direction = Direction.INPUT
b_button.pull = Pull.UP

def check(token):
    if token == "A":
        return not a_button.value
    if token == "B":
        return not b_button.value