from SubMachines.CutMachine import CutMachine
from Motors.Motor import Motor
from Motors.SpinMotor import SpinMotor
from config import configurationMap

class Drill(CutMachine):
    """The machine responsible for drilling.
    
    This directly sends commands to drill microcontroller to generate 
    actuations.
    
    """
    def __init__(self, controller):
        super().__init__(controller)
        self.name = "Drill"
        self.homeX = configurationMap['drill']['homeX']
        self.spinMotor = SpinMotor(configurationMap['drill']['spinDPR'])
        self.vertMotor = Motor(configurationMap['drill']['raiseDPR'])
        self.penMotor = Motor(configurationMap['drill']['pushDPR'])
