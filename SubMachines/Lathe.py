from SubMachines.CutMachine import CutMachine
from Motors.Motor import Motor
from Motors.SpinMotor import SpinMotor
from config import configurationMap

class Lathe(CutMachine):
    """The machine responsible for drilling.
    
    This directly sends commands to drill microcontroller to generate 
    actuations.
    
    """
    def __init__(self, controller):
        super().__init__(controller)
        self.name = 'Lathe'
        self.homeX = configurationMap['lathe']['homeX']
        self.spinMotor = SpinMotor(configurationMap['lathe']['spinDPR'])
        self.vertMotor = Motor(configurationMap['lathe']['raiseDPR'])
        self.penMotor = Motor(configurationMap['lathe']['pushDPR'])
