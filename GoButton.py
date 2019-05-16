import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

class GoButton:

    def __init__(self, controller):
        # GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(37, GPIO.IN,
                   pull_up_down=GPIO.PUD_DOWN)  # Set pin 37 to be an input pin and set initial value to be pulled low (off)
        GPIO.add_event_detect(37, GPIO.RISING, callback=self.buttonClicked)  # Setup event on pin 37 rising edge
        self.depressed = False
        self.controller = controller

    def buttonClicked(self, channel):
        if not self.depressed:
            # DO button press
            print('Go button pressed!')
            self.controller.goButtonClicked()
            self.depressed = True
            time.sleep(1)
            self.depressed = False




