# Typical Noisy Readings From A Photocell
from setup import photocell
import time

checkin = time.monotonic()

while True:
    if time.monotonic() - checkin > 0.1:
        print(photocell.value)
        checkin = time.monotonic()