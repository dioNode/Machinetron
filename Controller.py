from SubMachines.Handler import Handler
from SubMachines.Drill import Drill
from SubMachines.Mill import Mill
from SubMachines.Lathe import Lathe
from Commands.Command import Command
from Simulators.MicrocontrollerSimulator import MicrocontrollerSimulator
from Commands.CommandGenerator import CommandGenerator

from support.supportMaps import statusMap

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

        self.currentFaceWidth = self.xLength
        self.currentFaceHeight = self.zLength
        self.currentFaceDepth = self.yLength
        
        self.handler = Handler(self)
        self.drill = Drill(self)
        self.lathe = Lathe(self)
        self.mill = Mill(self)
        self.commandGenerator = CommandGenerator(self)

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
                    self.startNextCommand()

        time.sleep(TIME_STEP)
        self.currentTime += TIME_STEP
        self.updateDirectionFaced()

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
        else:
            print("Throw not a command exception")

    def startNextCommand(self):
        self.microcontrollerSimulator.clearTargets()
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

    def setFace(self, face):
        xLength = self.xLength
        yLength = self.yLength
        zLength = self.zLength
        if face == 'front':
            self.currentFaceWidth = xLength
            self.currentFaceDepth = yLength
            self.currentFaceHeight = zLength
        elif face == 'right':
            self.currentFaceWidth = yLength
            self.currentFaceDepth = xLength
            self.currentFaceHeight = zLength
        elif face == 'back':
            self.currentFaceWidth = xLength
            self.currentFaceDepth = yLength
            self.currentFaceHeight = zLength
        elif face == 'left':
            self.currentFaceWidth = yLength
            self.currentFaceDepth = xLength
            self.currentFaceHeight = zLength
        elif face == 'top':
            self.currentFaceWidth = xLength
            self.currentFaceHeight = yLength
            self.currentFaceDepth = zLength

    def updateDirectionFaced(self):

        spinAngle = self.handler.spinMotor.currentDisplacement % 360
        flipAngle = self.handler.flipMotor.currentDisplacement % 360

        xLength = self.xLength
        yLength = self.yLength
        zLength = self.zLength

        if flipAngle == 0:
            # Handler is down
            if spinAngle == 0:
                # Facing front
                self.setFace('front')
            elif spinAngle == 90:
                # Facing right
                self.setFace('right')
            elif spinAngle == 180:
                # Facing back
                self.setFace('back')
            elif spinAngle == 270:
                # Facing left
                self.setFace('left')
        elif flipAngle == 90:
            # Handler is up
            self.currentFaceDepth = zLength
            if spinAngle == 0:
                # Facing front
                self.currentFaceWidth = xLength
                self.currentFaceHeight = yLength
            elif spinAngle == 90:
                # Facing right
                self.currentFaceWidth = yLength
                self.currentFaceHeight = xLength
            elif spinAngle == 180:
                # Facing right
                self.currentFaceWidth = xLength
                self.currentFaceHeight = yLength
            elif spinAngle == 270:
                # Facing right
                self.currentFaceWidth = yLength
                self.currentFaceHeight = xLength

