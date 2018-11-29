# code to test the built-in DotStar
import board
import time
import random
import adafruit_dotstar

rgb = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
rgb.brightness = 0.3

def random_color():
    return (
        random.randrange(0, 255, 25), 
        random.randrange(0, 255, 25),
        random.randrange(0, 255, 25))

while True:
    rgb.fill(random_color())
    time.sleep(0.5)