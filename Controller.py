from SubMachines.Handler import Handler
from SubMachines.Drill import Drill
from SubMachines.Mill import Mill
from SubMachines.Lathe import Lathe
from Commands.Command import Command
from Microcontroller import Microcontroller
from Simulators.MicrocontrollerSimulator import MicrocontrollerSimulator
from Commands.CommandGenerator import CommandGenerator

from support.supportMaps import statusMap
from config import configurationMap

import time

class Controller:
    """The class that controls all functionality of MACHINETRON.
    
    All control logic should flow through the controller class which controls
    everything MACHINETRON needs to do.
    
    """
    def __init__(self, useSimulator=False):
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
        self.commandQueueHistory = []
        self.currentCommand = None

        self.state = statusMap['stopped']
        self.facename = 'front'

        self.timeStep = 0.001 if useSimulator else 1
        speedMultiplier = configurationMap['other']['speedMultiplier']
        self.microcontroller = MicrocontrollerSimulator(speedMultiplier) if useSimulator else Microcontroller()

    def __repr__(self):
        print(self.commandQueue)
        return str(self.currentCommand)

    def tick(self):
        """Updates the information variables on the controller.

        This involves:
        - Checking for whether the current command has been complete
        - Updating the current time
        - Checking for the handler direction

        """
        if self.state == statusMap['started']:
            if not self.isComplete():
                if self.commandComplete():
                    self.startNextCommand()
            else:
                # self.goButtonClicked()
                # Reset buffer
                self.commandQueue = self.commandQueueHistory.copy()

        time.sleep(self.timeStep)
        self.currentTime += self.timeStep
        self.updateDirectionFaced()

    def start(self):
        """Allows the controller to start issuing commands."""
        # Store current command list in history to be reloaded again when finished
        self.commandQueueHistory = self.commandQueue.copy()
        # Setup bus to allow i2c transfer
        self.microcontroller.setupBus()

    def pause(self):
        """Pauses the current controls so no new commands can be issued."""
        # TODO change to pause immediately
        self.state = statusMap['stopped']

    def stop(self):
        """Stops the current controls so no new commands can be issued."""
        # TODO reset commands to start
        self.state = statusMap['stopped']

    def setMountFace(self, xLength, yLength, zLength):
        """Sets the current mounting orientation.

        Args:
            xLength (double): The length of the foam along the rail direction.
            yLength (double): The length of the foam along the cut machine penetration direction.
            zLength (double): The vertical length of the foam.

        """
        self.xLength = xLength
        self.yLength = yLength
        self.zLength = zLength
        
    def getLengths(self):
        """Gets the dimensions relative to the initial foam placement.

        Returns:
            Tuple of each of the lengths.

        """
        return self.xLength, self.yLength, self.zLength

    def addCommand(self, command):
        """Adds a command onto the command queue.

        Args:
            command (Command): The command that you want to have added.

        """
        if isinstance(command, Command):
            self.commandQueue.append(command)
        else:
            print("Throw not a command exception")

    def startNextCommand(self):
        """Starts the next command.

        This should only be triggered after the STM has signalled the command has finished.

        """
        if not self.commandQueue:
            # Command queue is empty
            self.currentCommand = None
        else:
            self.currentCommand = self.commandQueue.pop(0)
            self.startExecuteCurrentCommand()

    def isComplete(self):
        """Checks if all the commands have been complete."""
        # Return true if list is commands are empty
        return not self.commandQueue and self.currentCommand is None

    def startExecuteCurrentCommand(self):
        """Starts executing the current command.

        This sends the current command to be processed by the STM.

        """
        print(self.currentCommand.generateTargets(True))
        self.microcontroller.processCommand(self.currentCommand)
        self.microcontroller.updateSubmachinesUsed(self.currentCommand.generateTargets())

    def updateEndeffactorValues(self):
        """Updates the information for the end location for each of the actuators.

        This is primarily useful for the simulation and most of the end locations should be tracked within the STM.

        """
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
        """Checks whether the current command has been complete."""
        return self.microcontroller.isComplete()

    def getMicrocontrollerResults(self):
        """Gets all the current positions of each of the motors.

        Returns:
            A dictionary of the current location of each of the motors.

        """

        return self.microcontroller.getLocationResults()

    def getMicrocontrollerTargets(self):
        """Gets all the current target instructions for all of the motors.

        Returns:
            A dictionary of targets displacements and speeds for each motor.

        """
        return self.microcontroller.getTargets()

    def setFace(self, face):
        """Sets relative face dimensions based on which side is facing the cut machines.

        This is used both as the commands are being set as well as when the machines are in action.

        Args:
            face (string): The current face turned towards the cut machines.

        """
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
        self.facename = face

    def updateDirectionFaced(self):
        """Updates the direction the handler is facing based on the current motor values.

        This is used mainly to track the handler position is while it is in operation.

        """

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

    def goButtonClicked(self):
        if self.state == statusMap['started']:
            self.state = statusMap['stopped']
            self.sendPauseCommand()
        else:
            self.state = statusMap['started']
            self.sendResumeCommand()

    def sendPauseCommand(self):
        self.microcontroller.pause()

    def sendResumeCommand(self):
        self.microcontroller.resume()
