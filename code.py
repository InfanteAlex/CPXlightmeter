import board
import board
import adafruit_tsl2591
from adafruit_circuitplayground import cp
import time
import math
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
# Setup for TSL2591 light sensor
i2c = board.I2C()
sensor = adafruit_tsl2591.TSL2591(i2c)
sensor.gain - adafruit_tsl2591.GAIN_LOW
def log2(x):
    return math.log(x, 2)


# evVal = log2(sensor.lux/2.5)

iso = 100
print(
    "For ISO 100 Press 1, ISO 200: 2, ISO 400: 3, ISO 800: 4, ISO 1600: 5, ISO 3200: 6, ISO 6400: 7"
)
isoInput = int(input())  # User input for ISO
if isoInput == 1:
    iso = 100
elif isoInput == 2:
    iso = 200
elif isoInput == 3:
    iso = 400
elif isoInput == 4:
    iso = 800
elif isoInput == 5:
    iso = 1600
elif isoInput == 6:
    iso = 3200
elif isoInput == 7:
    iso = 6400
else:
    print("Not valid value")


print("Aperture (Av):")
av = float(input())  # User input for aperture value

time.sleep(0.5)
# if iso:
#    isoEv = evVal + log2(iso / 100)
common_speeds = [
    1 / 8000,
    1 / 4000,
    1 / 2000,
    1 / 1000,
    1 / 500,
    1 / 250,
    1 / 125,
    1 / 60,
    1 / 30,
    1 / 15,
    1 / 8,
    1 / 4,
    1 / 2,
    1,
]
# Main loop
while True:
    if sensor.lux <= 0:
        print("Light sensor reading is invalid (lux <= 0). Retrying...")
        time.sleep(1)
        continue
    # if cp.button_a:  # Button A is pressed


    # Calculate EV value based on sensor lux, ISO
    evVal = log2(sensor.lux / 2.5)
    isoEv = evVal + log2(iso / 100)
    # Example Tv (shutter speed) calculation based on aperture and ISO
    # tv = (100 * (av ** 2)) / (isoEv * (2 ** isoEv))
    tv = (av ** 2) / (2 ** isoEv * (iso / 100))
    sSpeed = min(common_speeds, key=lambda x: abs(x - tv))
    print("Light: {0:.2f} lux".format(sensor.lux))
    print("EV: {0:.2f}".format(isoEv))
    # print("Shutter Speed (Tv): {0:.6f}".format(tv))
    layout.write(f"{sensor.lux}")
    time.sleep(0.1)
    kbd.send(Keycode.RIGHT_ARROW)
    time.sleep(0.1)
    if sSpeed >= 1:
        print(f"Shutter Speed: {int(tv)}")
        layout.write(f"{float(tv)}")
    else:
        print(f"Shutter Speed: 1/{int(1 / sSpeed)}")
        layout.write(f"1/{int(1 / sSpeed)}")
    time.sleep(0.1)
    kbd.send(Keycode.LEFT_ARROW)
    time.sleep(0.1)
    kbd.send(Keycode.DOWN_ARROW)

    time.sleep(1800)
#  if cp.button_b:  # Break loop if button B is pressed
#       break
    if cp.button_b:
        break
