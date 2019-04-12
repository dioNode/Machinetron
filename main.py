from Controller import Controller
from Simulators.OutputSimulator import OutputSimulator

controller = Controller()

def main():
    setMountFace(76.6, 110, 80)
    controller.start()
    controller.tick()


    ################ Commands go here ################

    reshapeSideM([(76.6, 20), (50, 30), (60, 30)])
    lathe(30, 50, 40)
    drill('front', 0, 30, 10)
    drill('left', -30, 60, 10)







    ################ End of Commands ################

    controller.commandGenerator.resetAll()
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
    controller.commandGenerator.reshapeM(widthHeightTuples, 'front')

def reshapeSideM(widthHeightTuples):
    controller.commandGenerator.reshapeM(widthHeightTuples, 'left')

def reshapeTopM(xzMiddleTuples):
    # TODO fix to center vertically
    controller.commandGenerator.reshapeM(xzMiddleTuples, 'top')
    
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
