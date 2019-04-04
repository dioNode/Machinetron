from SubMachines.SubMachine import SubMachine
from Motors.Motor import Motor

class CutMachine(SubMachine):
    """A submachine responsible for cutting.
    
    This is either the drill, mill or lathe.
    
    """    
    def __init__(self, controller):
        print("TODO: CutMachine init")
        super().__init__(controller)
        self.spinMotor = Motor(1)
        self.vertMotor = Motor(0.02)
        self.penMotor = Motor(0.07)
        self.name = "Cut Machine"
        self.homeX = 0
        
    def raiseTo(self, z):
        print("TODO: CutMachine raiseTo")
        
    def pushTo(self, y):
        print("TODO: CutMachine pushTo")
        
    def spin(self):
        print("TODO: CutMachine spin")
        
    def reset(self):
        print("TODO: CutMachine reset")