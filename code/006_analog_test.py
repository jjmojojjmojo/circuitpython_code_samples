# Basic Analog Sensor Test
import board
import time
import adafruit_thermistor
import analogio

thermistor = adafruit_thermistor.Thermistor(board.A1, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
photocell = analogio.AnalogIn(board.A2)

def voltage(value):
    return round((value * 3.3) / 65536, 2)   

while True:
    print("Temperature in degrees C:", thermistor.temperature)
    print("Light level in voltage:", voltage(photocell.value))
    time.sleep(1.0)