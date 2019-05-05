from Controller import Controller
from STL.STLProcessor import STLProcessor
from Simulators.OutputSimulator import OutputSimulator

controller = Controller(True)
stlProcessor = STLProcessor()

def main():
    setMountFace(76.6, 80, 110)
    controller.start()
    controller.tick()


    ################ Commands go here ################
    # stlProcessor.generateCommands('part0.STL', controller)

    lathe(50, 80, 25)
    drill('front', -20, 25, 50)
    drill('front', 20, 25, 50)
    cutInCircle('top', 0, 40, 25, 40)
    fillet('top', -38.3, 0, 10, 3, 30)
    fillet('top', -38.3, 80, 10, 2, 30)
    fillet('top', 38.3, 80, 10, 1, 30)
    fillet('top', 38.3, 0, 10, 4, 30)
    intrude('top', 0, 0, 12.5, 80-12.5, 40, 40, 6)




    ################ End of Commands ################

    controller.commandGenerator.resetAll()
    controller.setFace('front')
    if controller.useSimulator:
        outputSimulator = OutputSimulator(controller)
        outputSimulator.simulate()



    while True:
        controller.tick()
        controller.updateEndeffactorValues()
        if controller.useSimulator:
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
    """Reshapes the front surface of the block based on width and heights from bottom up.

    Args:
        widthHeightTuples (tuple array): List of tuples in the form (width, height) starting from bottom.

    """
    controller.commandGenerator.reshapeM(widthHeightTuples, 'front')


def reshapeSideM(widthHeightTuples):
    """Reshapes the side surface of the block based on width and heights from bottom up.

    Args:
        widthHeightTuples (tuple array): List of tuples in the form (width, height) starting from bottom.

    """
    controller.commandGenerator.reshapeM(widthHeightTuples, 'left')


def reshapeTopM(xzMiddleTuples):
    """Reshapes the top surface of the block based on width and heights from middle up.

    Args:
        xzMiddleTuples (tuple array): List of tuples in the form (width, height) starting from middle upwards.

    """
    # TODO fix to center vertically
    controller.commandGenerator.reshapeM(xzMiddleTuples, 'top')


def cutInCircle(face, x, z, radius, depth):
    """Completely cuts out the inside of a given circle.

    Args:
        face (string): The face being worked on (front, top, left, right, back).
        x (double): The horizontal displacement from the face's center of the center of the circle's center point.
        z (double): The vertical displacement from the face's bottom of the circle's center point.
        radius (double): Radius of the circle being cut out.
        depth (double): Depth of the circle being cut out.

    """
    controller.commandGenerator.cutInCircle(face, x, z, radius, depth)


def cutOutCircle(face, x, z, radius, depth):
    """Cuts once around the outside of the circle.

    This assumes that the mill only needs to go around the outer border once and extra foam with fall off.

    Args:
        face (string): The face being worked on (front, top, left, right, back).
        x (double): The horizontal displacement from the face's center of the center of the circle's center point.
        z (double): The vertical displacement from the face's bottom of the circle's center point.
        radius (double): Radius of the circle being cut out.
        depth (double): Depth of the circle being cut out.

    """
    controller.commandGenerator.cutOutCircle(face, x, z, radius, depth)


def fillet(face, x, z, radius, quadrant, depth):
    """Creates a fillet at a certain point.

    Args:
        face (string): The face being worked on (front, top, left, right, back).
        x (double): The horizontal displacement from the face's center of the center of the circle's center point.
        z (double): The vertical displacement from the face's bottom of the circle's center point.
        radius (double): Radius of the circle being cut out.
        quadrant(int): A number representing which quadrant needs to be filleted out (1 = top-right, 2 = top-left,
            3 = bottom-left, 4 = bottom-right).
        depth (double): Depth of the circle being cut out.

    """
    controller.commandGenerator.fillet(face, x, z, radius, quadrant, depth)


def intrude(face, x0, x1, z0, z1, d0, d1, radius):
    """Creates an intrusion from one point to another with a set radius.

    Args:
        face (string): The face being worked on (front, top, left, right, back).
        x0 (double): The initial horizontal displacement.
        x1 (double): The final horizontal displacement.
        z0 (double): The initial vertical displacement from the face's bottom of the circle's center point.
        z1 (double): The initial vertical displacement from the face's bottom of the circle's center point.
        d0 (double): The initial depth.
        d1 (double): The final depth.
        radius (double): Radius of the circle being cut out.

    """
    controller.commandGenerator.intrude(face, x0, x1, z0, z1, d0, d1, radius)


def lathe(z0, z1, radius):
    """Uses the lathe to create a radial cut from z0 to z1.

    Args:
        z0 (double): The initial vertical displacement from the face's bottom of the circle's center point.
        z1 (double): The final vertical displacement from the face's bottom of the circle's center point.
        radius (double): Radius of the circle being cut out.

    """
    controller.commandGenerator.lathe(z0, z1, radius)


def drill(face, x, z, depth):
    """Uses the drill to drill a hole.

    Args:
        face (string): The face being worked on (front, top, left, right, back).
        x (double): The horizontal displacement of the drill from center.
        z (double): The vertical displacement from the face's bottom of the drill's center point.
        depth (double): Depth of the drill into the foam.

    """
    controller.commandGenerator.drill(face, x, z, depth)


if __name__== "__main__":
    main()
