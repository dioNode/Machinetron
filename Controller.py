from Handler import Handler
from Drill import Drill
from Command import Command

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

        self.commandQueue = []
        self.currentCommand = None

    def __repr__(self):
        print(self.commandQueue)
        return str(self.currentCommand)
        
    def setMountFace(self, xLength, yLength, zLength):
        self.xLength = xLength
        self.yLength = yLength
        self.zLength = zLength
        print("mounted")
        
    def getLengths(self):
        return ((self.xLength, self.yLength, self.zLength))

    def addCommand(self, command):
        if isinstance(command, Command):
            self.commandQueue.append(command)
        else:
            print("Throw not a command exception")

    def startNextCommand(self):
        self.currentCommand = self.commandQueue.pop(0)

