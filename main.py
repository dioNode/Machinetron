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

    controller.addCommand(SelectCutmachineCommand(controller.lathe))
    combined = [RaiseCommand(controller.drill, 100), SpinCommand(controller.drill), ShiftCommand(controller.drill, 50)]
    controller.addCommand(CombinedCommand(combined))

    controller.addCommand(RaiseCommand(controller.drill, 50))


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
    print("TODO: reshapeFrontM")
    # simulator.reshapeFrontM(widthHeightTuples)

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
