


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)

def turnGreen():
    GPIO.output(33, GPIO.HIGH)
    GPIO.output(35, GPIO.LOW)


def turnYellow():
    GPIO.output(33, GPIO.HIGH)
    GPIO.output(35, GPIO.HIGH)


def turnRed():
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.HIGH)

while True:
    print('loop')
    turnGreen()
    time.sleep(1)
    turnRed()
    time.sleep(1)
    turnYellow()
    time.sleep(1)

