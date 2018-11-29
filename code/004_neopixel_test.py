# Code to test the built-in Neopixel
import board
import time
import random
import neopixel

rgb = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgb.brightness = 0.3

def random_color():
    return (
        random.randrange(0, 255, 25), 
        random.randrange(0, 255, 25),
        random.randrange(0, 255, 25))

while True:
    rgb.fill(random_color())
    time.sleep(0.5)