# Face Detection Example
#
# This example shows off the built-in face detection feature of the OpenMV Cam.
# Face detection works by using the Haar Cascade feature detector on an image. A
# Haar Cascade is a series of simple area contrasts checks. For the built-in
# frontalface detector there are 25 stages of checks with each stage having
# hundreds of checks a piece. Haar Cascades run fast because later stages are
# only evaluated if previous stages pass. Additionally, your OpenMV Cam uses
# a data structure called the integral image to quickly execute each area
# contrast check in constant time (the reason for feature detection being
# grayscale only is because of the space requirment for the integral image).

import sensor, time, image

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


def initFindFace():
    # Load Haar Cascade, default this will use all stages, lower satges is faster but less accurate.
    face_cascade = image.HaarCascade("frontalface", stages=25)
    print(face_cascade)
    return face_cascade

def scankeys():
    # GPIO init

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

    temp = 0
    for row in range(1):
        for col in range(1):
            row_pins[row].high()

            if col_pins[col].value() == 1:
                temp = 1
                utime.sleep(0.3)

        row_pins[row].low()
        return temp


def findFace(face_cascade):
    face_found = 0
    # Capture snapshot
    img = sensor.snapshot()

    # Note: Lower scale factor scales-down the image more and detects smaller objects.
    # Higher threshold results in a higher detection rate, with more false positives.
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

    if (len(objects) != 0):
        face_found = face_found + 1
        red_led.off()
        green_led.on()

    # Draw objects
        for r in objects:
            img.draw_rectangle(r)

        # Print FPS.
        # Note: Actual FPS is higher, streaming the FB makes it slower.
        #print(clock.fps())
        time.sleep_ms(100)

    return face_found

clock = time.clock()


# motor controls
IN1 = Pin('P2',Pin.OUT)
IN2 = Pin('P3',Pin.OUT)
IN3 = Pin('P4',Pin.OUT)
IN4 = Pin('P5',Pin.OUT)
pins = [IN1, IN2, IN3, IN4]
sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

button = Pin('P7', Pin.IN, Pin.PULL_UP)


red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)
ir_led    = LED(4)



initSensor()

fc = initFindFace()

begin = 0
validPin = 0
validFace = 0
numFaces = 0
done = 0
print('Waitng for sign-in...')
while (True):
    clock.tick()
    blue_led.on()
    pinBuff = []
    time.sleep_ms(500)
    #hold to start

    if button.value() == 1 and begin == 0:
        begin = 1

    while  begin == 1:
        blue_led.off()
        green_led.on()
        red_led.on()

        while button.value() == 1:
            print('Beginning sign-in!')
            print("Please enter a key from the keypad")
            time.sleep_ms(1000)


        while(scankeys() == 1 and validPin == 0):
            pinBuff.append(scankeys())
            print('User entered: *')
            blue_led.off()
            red_led.off()
            time.sleep_ms(400)

        while len(pinBuff) > 3 and validPin == 0:
            print('VALID PIN')
            red_led.off()
            validPin = 1
            time.sleep_ms(500)
            print('finding face....')


        while validPin == 1 and validFace == 0:
            red_led.on()
            time.sleep_ms(100)
            temp = findFace(fc)
            if temp:
                numFaces = numFaces + 1
                #print(numFaces)
            if numFaces > 15:
                print('Scan complete')
                validFace = 1
                break

            break

        while validPin == 1 and validFace == 1:
            print('Dispensing Methadone:')
            for j in range(500):
                for step in sequence:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        sleep(0.001)
            done = 1
            if done == 1:
                break



        if (done == 1 and begin == 1 and validPin == 1 and validFace == 1):
            begin = 0
            validPin = 0
            validFace = 0
            numFaces = 0
            done = 0
            sleep(1)












