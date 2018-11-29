# setup.py for the CircuitPlayground Express
import board
import neopixel
import adafruit_thermistor
from digitalio import DigitalInOut, Direction, Pull
import analogio

thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
photocell = analogio.AnalogIn(board.LIGHT)

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

rgb = neopixel.NeoPixel(board.NEOPIXEL, 10)
rgb.brightness = 0.1

a_button = DigitalInOut(board.D4)
a_button.direction = Direction.INPUT
a_button.pull = Pull.DOWN

b_button = DigitalInOut(board.D5)
b_button.direction = Direction.INPUT
b_button.pull = Pull.DOWN

def check(token):
    if token == "A":
        return a_button.value
    if token == "B":
        return b_button.value