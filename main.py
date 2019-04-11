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
    
    # Commands go here
    lathe(30, 50, 40)
    drill('front', 0, 30, 10)
    drill('left', -30, 60, 10)
    reshapeFrontM([(76.6, 20), (50, 30), (60, 30)])







    resetAll()
    # end of commands


    controller.start()
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
    # Some useful variables to have
    currentHeight = 0
    millSpinCommand = SpinCommand(controller.mill)
    radius = configurationMap['mill']['diameter'] / 2

    # Get to initial positioning
    controller.addCommand(CombinedCommand([
        SelectFaceCommand('front', controller.handler),
        RaiseCommand(controller.mill, controller.zLength),
        ShiftCommand(controller.mill, -controller.xLength/2 - radius)
    ], 'Setup initial position and face'))

    # Push into depth
    controller.addCommand(CombinedCommand([
        PushCommand(controller.mill, controller.yLength),
        millSpinCommand
    ]))

    # Go up left hand side
    for tupleNum in range(len(widthHeightTuples)):
        widthHeightTuple = widthHeightTuples[tupleNum]
        width, height = widthHeightTuple
        currentHeight += height
        x = -width / 2 - radius
        z = controller.zLength - currentHeight - radius
        controller.addCommand(CombinedCommand([ShiftCommand(controller.mill, x), millSpinCommand]))
        controller.addCommand(CombinedCommand([RaiseCommand(controller.mill, z), millSpinCommand]))

    # Go back down right hand side
    for tupleNum in range(len(widthHeightTuples) - 1, -1, -1):
        widthHeightTuple = widthHeightTuples[tupleNum]
        width, height = widthHeightTuple
        currentHeight -= height
        x = width / 2 + radius
        z = controller.zLength - currentHeight - radius
        controller.addCommand(CombinedCommand([ShiftCommand(controller.mill, x), millSpinCommand]))
        controller.addCommand(CombinedCommand([RaiseCommand(controller.mill, z), millSpinCommand]))

    # Go back down to bottom
    controller.addCommand(CombinedCommand([RaiseCommand(controller.mill, 0), millSpinCommand]))
    controller.addCommand(PushCommand(controller.mill, 0))

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
    handlerSpinCommand = SpinCommand(controller.handler)
    

    
def drill(face, x, z, depth):
    # Align to face
    controller.addCommand(SelectFaceCommand(face, controller.handler))
    controller.addCommand(CombinedCommand([
        ShiftCommand(controller.drill, x),
        RaiseCommand(controller.drill, z)], 'Align Drill'))
    # Drill in
    controller.addCommand(CombinedCommand([
        PushCommand(controller.drill, depth),
        SpinCommand(controller.drill)
    ], 'Drill In'))
    # Pull drill out
    controller.addCommand(PushCommand(controller.drill, 0))

def resetAll():
    # Remove all potential cutting bits from workpiece
    controller.addCommand(CombinedCommand([
        PushCommand(controller.drill, 0),
        PushCommand(controller.mill, 0),
        PushCommand(controller.lathe, 0),
        SpinCommand(controller.drill, 0),
        SpinCommand(controller.mill, 0),
        SpinCommand(controller.lathe, 0),
        SpinCommand(controller.handler, 0),
    ], 'Retract Cutting Pieces'))
    # Reset all to original location
    controller.addCommand(CombinedCommand([
        ShiftCommand(controller.drill, 0),
        RaiseCommand(controller.drill, 0),
        RaiseCommand(controller.mill, 0),
        RaiseCommand(controller.lathe, 0),
    ], 'Move to Home Location'))

if __name__== "__main__":
    main()
