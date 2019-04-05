from Controller import Controller
from Simulators.OutputSimulator import OutputSimulator
from Commands.SelectCutmachineCommand import SelectCutmachineCommand
from Commands.RaiseCommand import RaiseCommand
from Commands.ShiftCommand import ShiftCommand
from Commands.PushCommand import PushCommand
from Commands.SpinCommand import SpinCommand
from Commands.CombinedCommand import CombinedCommand


controller = Controller()

def main():
    
    setMountFace(76.6, 110, 80)
    
    # Commands go here
    reshapeFrontM([(76.6, 20), (50, 30), (60, 30)])




    controller.start()
    outputSimulator = OutputSimulator(controller)
    outputSimulator.simulate()




    while True:
        controller.tick()
        controller.updateEndeffactorValues()
        outputSimulator.update()








    
    # end of commands





def setMountFace(xLength, yLength, zLength):
    """Tells the system how the block has been arranged.
    
    Args:
        xLength (double): Length of block in the direction of rails.
        yLength (double): Length of block in vertically.
        zLength (double): Length of block in the direction of drilling.
    
    """
    controller.setMountFace(xLength, yLength, zLength)

def reshapeFrontM(widthHeightTuples):
    # simulator.reshapeFrontM(widthHeightTuples)
    # TODO turn face
    controller.addCommand(SelectCutmachineCommand(controller.mill))

    controller.addCommand(RaiseCommand(controller.mill, controller.zLength))
    controller.addCommand(ShiftCommand(controller.mill, 0))

    currentHeight = 0

    millSpinCommand = SpinCommand(controller.mill)

    # Push into depth
    controller.addCommand(PushCommand(controller.mill, controller.yLength))

    # Go up left hand side
    for tupleNum in range(len(widthHeightTuples)):
        widthHeightTuple = widthHeightTuples[tupleNum]
        width, height = widthHeightTuple
        currentHeight += height
        x = controller.xLength / 2 - width / 2
        z = controller.zLength - currentHeight
        controller.addCommand(CombinedCommand([ShiftCommand(controller.mill, x), millSpinCommand]))
        controller.addCommand(CombinedCommand([RaiseCommand(controller.mill, z), millSpinCommand]))

    # Go back down right hand side
    for tupleNum in range(len(widthHeightTuples) - 1, -1, -1):
        widthHeightTuple = widthHeightTuples[tupleNum]
        width, height = widthHeightTuple
        currentHeight -= height
        x = controller.xLength / 2 + width / 2
        z = controller.zLength - currentHeight
        controller.addCommand(CombinedCommand([ShiftCommand(controller.mill, x), millSpinCommand]))
        controller.addCommand(CombinedCommand([RaiseCommand(controller.mill, z), millSpinCommand]))


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
    print("TODO: lathe")
    
def drill(face, x, z, depth):
    print("TODO: drill")    
    

if __name__== "__main__":
    main()
