from Handler import Handler
from Drill import Drill
from Mill import Mill
from Lathe import Lathe
from Command import Command

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

        self.state = 0  # 0=Stopped, 1=Running, 2=Paused

    def __repr__(self):
        print(self.commandQueue)
        return str(self.currentCommand)


    def tick(self):
        if self.state == 1:
            if not self.isComplete():
                print("tick")
                if self.currentCommand.isComplete():
                    print("Completed " + str(self.currentCommand))
                    self.startNextCommand()
            else:
                print("Finished")

        time.sleep(TIME_STEP)
        self.currentTime += TIME_STEP
        print(self.currentTime)

        self.handler.railMotor.step()
        self.handler.spinMotor.step()
        self.mill.vertMotor.step()
        self.drill.spinMotor.step()

    def start(self):
        self.startNextCommand()
        self.state = 1

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
        self.currentCommand = self.commandQueue.pop(0)

    def isComplete(self):
        # Return true if list is commands are empty
        return not self.commandQueue
