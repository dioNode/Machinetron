from SubMachine import SubMachine

class Handler(SubMachine):
    """This controls the handler submachine.
    
    It directly sends information to the handler microcontroller to actuate 
    motions.
    
    """
    def __init__(self):
        super().__init__()
        print("TODO: Handler init")
        
    def positionFace(self, face, submachine):
        print("TODO: Handler positionFace")
        
    def moveTo(self, x):
        print("TODO: Handler moveTo")

    def moveX(self, steps):
        print("TODO: Handler moveX")

    def spin(self):
        print("TODO: Handler spin")
        
    def rotate(self, steps):
        print("TODO: Handler rotate")

    def reset(self):
        print("TODO: Handler reset")
        
    def spinOff(self):
        print("TODO: Handler spinOff")
