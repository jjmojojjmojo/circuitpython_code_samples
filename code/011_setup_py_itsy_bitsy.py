# setup.py for the Itsy Bitsy M0 Express
import board
from digitalio import DigitalInOut, Direction, Pull
import analogio
import adafruit_dotstar
import adafruit_thermistor

thermistor = adafruit_thermistor.Thermistor(board.A1, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
photocell = analogio.AnalogIn(board.A2)

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

rgb = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
rgb.brightness = 0.3

a_button = DigitalInOut(board.D11)
a_button.direction = Direction.INPUT
a_button.pull = Pull.UP

b_button = DigitalInOut(board.D7)
b_button.direction = Direction.INPUT
b_button.pull = Pull.UP

def check(token):
    if token == "A":
        return not a_button.value
    if token == "B":
        return not b_button.value