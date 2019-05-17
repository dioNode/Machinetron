
import RPi.GPIO as GPIO

class StatusLed:

    def __init__(self, isConnected=True):
        self.isConnected = isConnected
        if isConnected:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(33, GPIO.OUT)
            GPIO.setup(35, GPIO.OUT)

    def turnGreen(self):
        if self.isConnected:
            GPIO.output(33, GPIO.HIGH)
            GPIO.output(35, GPIO.LOW)

    def turnYellow(self):
        if self.isConnected:
            GPIO.output(33, GPIO.HIGH)
            GPIO.output(35, GPIO.HIGH)

    def turnRed(self):
        if self.isConnected:
            GPIO.output(33, GPIO.LOW)
            GPIO.output(35, GPIO.HIGH)