from Handler import Handler
from Drill import Drill
from Mill import Mill
from Lathe import Lathe
from Command import Command
from MicrocontrollerSimulator import MicrocontrollerSimulator

from supportMaps import statusMap

import time

TIME_STEP = 0.001

class Controller:
    """The class that controls all functionality of MACHINETRON.
    
    All control logic should flow through the controller class which controls
    everything MACHINETRON needs to do.
    
    """
    def __init__(self):
        self.currentTime = 0
        self.xLength = 0
        self.yLength = 0
        self.zLength = 0
        
        self.handler = Handler(self)
        self.drill = Drill(self)
        self.lathe = Lathe(self)
        self.mill = Mill(self)

        self.commandQueue = []
        self.currentCommand = None
        self.microcontrollerSimulator = MicrocontrollerSimulator()

        self.state = statusMap['stopped']

    def __repr__(self):
        print(self.commandQueue)
        return str(self.currentCommand)


    def tick(self):
        if self.state == statusMap['started']:
            if not self.isComplete():
                if self.commandComplete():
                    print("Completed " + str(self.currentCommand))
                    self.startNextCommand()

        time.sleep(TIME_STEP)
        self.currentTime += TIME_STEP

    def start(self):
        self.startNextCommand()

        self.state = statusMap['started']

    def pause(self):
        print("TODO: Pause controller")

    def stop(self):
        print("TODO: Stop controller")

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
            print("added comamnd")
        else:
            print("Throw not a command exception")

    def startNextCommand(self):
        if not self.commandQueue:
            # Command queue is empty
            self.currentCommand = None
        else:
            self.currentCommand = self.commandQueue.pop(0)
            self.startExecuteCurrentCommand()

    def isComplete(self):
        # Return true if list is commands are empty
        return not self.commandQueue and self.currentCommand == None

    def startExecuteCurrentCommand(self):
        targets = self.currentCommand.generateTargets()
        self.microcontrollerSimulator.setTargets(targets)

    def updateEndeffactorValues(self):

        results = self.getMicrocontrollerResults()
        for cutmachine in [self.drill, self.mill, self.lathe]:
            name = cutmachine.name.lower()
            cutmachine.spinMotor.currentDisplacement = results[name]['spin']
            cutmachine.vertMotor.currentDisplacement = results[name]['vert']
            cutmachine.penMotor.currentDisplacement = results[name]['pen']

        name = self.handler.name.lower()
        self.handler.spinMotor.currentDisplacement = results[name]['spin']
        self.handler.railMotor.currentDisplacement = results[name]['rail']
        self.handler.flipMotor.currentDisplacement = results[name]['flip']

    def commandComplete(self):
        self.microcontrollerSimulator.update()
        return self.microcontrollerSimulator.getCommandStatus() == statusMap['complete']


    def getMicrocontrollerResults(self):
        self.microcontrollerSimulator.update()
        return self.microcontrollerSimulator.results

    def getMicrocontrollerTargets(self):
        self.microcontrollerSimulator.update()
        return self.microcontrollerSimulator.targets
