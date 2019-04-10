from SubMachines.SubMachine import SubMachine
from Motors.Motor import Motor
from Motors.SpinMotor import SpinMotor
from Commands.SpinCommand import SpinCommand
from Commands.ShiftCommand import ShiftCommand

from config import configurationMap

class Handler(SubMachine):
    """This controls the handler submachine.
    
    It directly sends information to the handler microcontroller to actuate 
    motions.
    
    """
    def __init__(self, controller):
        super().__init__(controller)
        self.name = "Handler"
        # Initialise motors
        self.railMotor = Motor(configurationMap['handler']['railDPR'])
        self.flipMotor = SpinMotor(configurationMap['handler']['flipDPR'])
        self.spinMotor = SpinMotor(configurationMap['handler']['spinDPR'])
        
    def moveTo(self, x):
        print("TODO: Handler moveTo")

    def moveX(self, steps):
        print("TODO: Handler moveX")

    def reset(self):
        self.controller.addCommand(SpinCommand(self, 0))
        self.controller.addCommand(ShiftCommand(self, 0))

