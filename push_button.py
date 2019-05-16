# import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
# import time
#
# def button_callback(channel):
#     print("Button was pushed!")
#
# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
# GPIO.add_event_detect(37,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
#
# while True:
#     print(1)
#     time.sleep(1)

from GoButton import GoButton
import time

goButton = GoButton()

while True:
    print(1)
    time.sleep(1)


GPIO.cleanup() # Clean up