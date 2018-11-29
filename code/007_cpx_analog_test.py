# Analog Sensor test for the CircuitPlayground Express
import board
import time
import adafruit_thermistor
import analogio

thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)
photocell = analogio.AnalogIn(board.LIGHT)

def voltage(value):
    return round((value * 3.3) / 65536, 2)  

while True:
    print("Temperature in degrees C:", thermistor.temperature)
    print("Light level in voltage:", voltage(photocell.value))
    time.sleep(1.0)