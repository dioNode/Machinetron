import time

class GoButton:

    def __init__(self, controller):
        import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
        # GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(37, GPIO.IN,
                   pull_up_down=GPIO.PUD_DOWN)  # Set pin 37 to be an input pin and set initial value to be pulled low (off)
        GPIO.add_event_detect(37, GPIO.RISING, callback=self.buttonClicked)  # Setup event on pin 37 rising edge
        GPIO.add_event_detect(37, GPIO.FALLING, callback=self.buttonReleased)  # Setup event on pin 37 rising edge
        self.depressed = False
        self.controller = controller
        self.lastPressedTime = 0
        self.pushDownTime = 0

    def buttonClicked(self, channel):
        currentTime = time.time()

        if currentTime - self.lastPressedTime > 1:
            self.lastPressedTime = currentTime
            self.pressDownTime = currentTime

    def buttonReleased(self, channel):
        releaseTime = time.time()
        if releaseTime - self.lastPressedTime < 2:
            print('normal press')
            self.controller.goButtonClicked()
        else:
            print('long press')
            self.controller.resetCurrentCommand()


