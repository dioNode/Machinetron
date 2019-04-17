from Controller import Controller
from Simulators.OutputSimulator import OutputSimulator
from config import configurationMap

controller = Controller()

def main():
    setMountFace(76.6, 80, 110)
    controller.start()
    controller.tick()


    ################ Commands go here ################
    # reshapeSideM([(76.6, 20), (50, 30), (60, 30)])
    # fillet('front', 20, 20, 20, 1, 10)
    # cutInCircle('front', 0, 30, 30, 20)
    # lathe(30, 50, 40)
    # drill('front', 0, 30, 10)
    # drill('left', -30, 60, 10)




    lathe(50, 80, 25)
    drill('front', -20, 25, 50)
    drill('front', 20, 25, 50)
    cutInCircle('top', 0, 40, 25, 40)
    fillet('top', -38.3, 0, 10, 3, 30)
    fillet('top', -38.3, 80, 10, 2, 30)
    fillet('top', 38.3, 0, 10, 4, 30)
    fillet('top', 38.3, 80, 10, 1, 30)






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
    controller.commandGenerator.cutInCircle(face, x, z, radius, depth)


def cutOutCircle(face, x, z, radius, depth):
    controller.commandGenerator.cutOutCircle(face, x, z, radius, depth)


def fillet(face, x, z, radius, quadrant, depth):
    controller.commandGenerator.fillet(face, x, z, radius, quadrant, depth)


def intrude(face, x0, x1, z0, z1, d0, d1, radius):
    print("TODO: intrude")


def lathe(z0, z1, radius):
    controller.commandGenerator.lathe(z0, z1, radius)


def drill(face, x, z, depth):
    controller.commandGenerator.drill(face, x, z, depth)


if __name__== "__main__":
    main()
