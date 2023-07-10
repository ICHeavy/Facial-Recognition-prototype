# Untitled - By: simaj - Mon Apr 24 2023

import sensor, image, time

from pyb import LED
from pyb import Pin
from time import sleep
import utime

def initSensor():
    sensor.reset()
    # Sensor settings
    sensor.set_contrast(3)
    sensor.set_gainceiling(16)
    # HQVGA and GRAYSCALE are the best for face tracking.
    sensor.set_framesize(sensor.HQVGA)
    sensor.set_pixformat(sensor.GRAYSCALE)

# Create a map between keypad buttons and characters
matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['*', '0', '#', 'D']]

# PINs according to schematic - Change the pins to match with your connections
keypad_rows = ['P0']
keypad_columns = ['P1']

# Create two empty lists to set up pins ( Rows output and columns input )
col_pins = []
row_pins = []

# Loop to assign GPIO pins and setup input and outputs
for x in range(0,1):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)

##############################Scan keys ####################

print("Please enter a key from the keypad")

def scankeys():
    temp = 0
    for row in range(1):
        for col in range(1):
            row_pins[row].high()

            if col_pins[col].value() == 1:
                temp = 1
                utime.sleep(0.3)

        row_pins[row].low()
        return temp

while True:
    x = scankeys()
    if x != 0:
        print(x)



