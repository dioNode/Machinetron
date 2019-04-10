from SubMachines.SubMachine import SubMachine

class CutMachine(SubMachine):
    """A submachine responsible for cutting.
    
    This is either the drill, mill or lathe.
    
    """    
    def __init__(self, controller):
        super().__init__(controller)
        self.vertMotor = Motor(1)
        self.penMotor = Motor(1)
        self.name = 'Cut Machine'
        self.homeX = 0
        
    def raiseTo(self, z):
        print("TODO: CutMachine raiseTo")
        
    def pushTo(self, y):
        print("TODO: CutMachine pushTo")
        
    def spin(self):
        print("TODO: CutMachine spin")
        
    def reset(self):
        self.controller.addCommand(PushCommand(self, 0))
        self.controller.addCommand(RaiseCommand(self, 0))


from Motors.Motor import Motor
from Commands.PushCommand import PushCommand
from Commands.RaiseCommand import RaiseCommand