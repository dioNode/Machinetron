from SubMachines.CutMachine import CutMachine
from Motors.Motor import Motor
from Motors.SpinMotor import SpinMotor
from config import configurationMap

class Mill(CutMachine):
    """The machine responsible for drilling.
    
    This directly sends commands to drill microcontroller to generate 
    actuations.
    
    """
    def __init__(self, controller):
        super().__init__(controller)
        self.name = "Mill"
        self.homeX = configurationMap['mill']['homeX']
        self.spinMotor = SpinMotor(configurationMap['mill']['spinDPR'])
        self.vertMotor = Motor(configurationMap['mill']['raiseDPR'])
        self.penMotor = Motor(configurationMap['mill']['pushDPR'])
