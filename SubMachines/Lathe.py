from SubMachines.CutMachine import CutMachine

class Lathe(CutMachine):
    """The machine responsible for drilling.
    
    This directly sends commands to drill microcontroller to generate 
    actuations.
    
    """
    def __init__(self, controller):
        super().__init__(controller)
        self.name = "Lathe"
        self.homeX = 200