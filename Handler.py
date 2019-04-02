from SubMachine import SubMachine
from Motor import Motor

class Handler(SubMachine):
    """This controls the handler submachine.
    
    It directly sends information to the handler microcontroller to actuate 
    motions.
    
    """
    def __init__(self, controller):
        super().__init__(controller)
        # Initialise motors
        self.railMotor = Motor(2)
        self.flipMotor = Motor(0.5)
        self.spinMotor = Motor(2)
        
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
