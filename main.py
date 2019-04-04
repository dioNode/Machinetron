from Controller import Controller
from Simulator import Simulator
from Command import Command
from OutputSimulator import OutputSimulator
import time


controller = Controller()

# fig = plt.figure()
#simulator = Simulator(controller, fig)

def main():
    
    setMountFace(76.6, 110, 80)
    
    # Commands go here
    #reshapeFrontM([(70, 29), (50, 20), (40, 40)])
    for i in range(2):
        command = Command("G01 X1 Y1")
        controller.addCommand(command)
        controller.addCommand(Command("C2 X2 Y2"))
        controller.addCommand(Command("P2 X3 Y3"))


    controller.start()

    outputSimulator = OutputSimulator(controller)

    outputSimulator.simulate()

    while True:
        controller.tick()
        outputSimulator.update()
        # controller.handler.railMotor.step()
        # controller.handler.spinMotor.step()
        # controller.mill.vertMotor.step()
        # controller.drill.spinMotor.step()











    
    
    # end of commands
    #simulator.simulate()







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
