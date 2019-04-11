import numpy as np

from Controller import Controller
from Simulators.OutputSimulator import OutputSimulator
from Commands.SelectCutmachineCommand import SelectCutmachineCommand
from Commands.SelectFaceCommand import SelectFaceCommand
from Commands.RaiseCommand import RaiseCommand
from Commands.ShiftCommand import ShiftCommand
from Commands.PushCommand import PushCommand
from Commands.SpinCommand import SpinCommand
from Commands.CombinedCommand import CombinedCommand

from config import configurationMap

controller = Controller()

def main():
    setMountFace(76.6, 110, 80)
    controller.start()
    controller.tick()


    
    # Commands go here
    reshapeFrontM([(76.6, 20), (50, 30), (60, 30)])
    lathe(30, 50, 40)
    drill('front', 0, 30, 10)
    drill('left', -30, 60, 10)







    controller.commandGenerator.resetAll()
    # end of commands


    outputSimulator = OutputSimulator(controller)
    outputSimulator.simulate()



    while True:
        controller.tick()
        controller.updateEndeffactorValues()
        outputSimulator.update()





def setMountFace(xLength, yLength, zLength):
    """Tells the system how the block has been arranged.
    
    Args:
        xLength (double): Length of block in the direction of rails.
        yLength (double): Length of block in vertically.
        zLength (double): Length of block in the direction of drilling.
    
    """
    controller.setMountFace(xLength, yLength, zLength)

def reshapeFrontM(widthHeightTuples):
    controller.commandGenerator.reshapeFrontM(widthHeightTuples)

def reshapeSideM(widthHeightTuples):
    print("TODO: reshapeSideM")

def reshapeTopM(xzMiddleTuples):
    print("TODO: reshapeTopM")
    
def cutInCircle(face, x, z, radius, depth):
    print("TODO: cutInCircle")
    
def cutOutCircle(face, x, z, radius, depth):
    print("TODO: cutOutCircle")
    
def fillet(face, x, z, radius, quadrant, depth):
    print("TODO: fillet")
    
def intrude(face, x0, x1, z0, z1, d0, d1, radius):
    print("TODO: intrude")
    
def lathe(z0, z1, radius):
    controller.commandGenerator.lathe(z0, z1, radius)

    
def drill(face, x, z, depth):
    controller.commandGenerator.drill(face, x, z, depth)

if __name__== "__main__":
    main()
