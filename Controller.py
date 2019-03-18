from Handler import Handler
from Drill import Drill

class Controller:
    """The class that controls all functionality of MACHINETRON.
    
    All control logic should flow through the controller class which controls
    everything MACHINETRON needs to do.
    
    """
    def __init__(self):
        print("Controller created...")
        self.xLength = 0
        self.yLength = 0
        self.zLength = 0
        
        self.handler = Handler()
        self.drill = Drill()
        
    def setMountFace(self, xLength, yLength, zLength):
        self.xLength = xLength
        self.yLength = yLength
        self.zLength = zLength
        print("mounted")
        
    def getLengths(self):
        return ((self.xLength, self.yLength, self.zLength))
        