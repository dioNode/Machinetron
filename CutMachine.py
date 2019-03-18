from SubMachine import SubMachine

class CutMachine(SubMachine):
    """A submachine responsible for cutting.
    
    This is either the drill, mill or lathe.
    
    """    
    def __init__(self):
        print("TODO: CutMachine init")
        super().__init__()
        
    def raiseTo(self, z):
        print("TODO: CutMachine raiseTo")
        
    def pushTo(self, y):
        print("TODO: CutMachine pushTo")
        
    def spin(self):
        print("TODO: CutMachine spin")
        
    def reset(self):
        print("TODO: CutMachine reset")