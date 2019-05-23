USE_GUI = False
USE_SIM = False
AUTO_START = False
AUTO_TOOLPATH = False

from Controller import Controller

if AUTO_TOOLPATH:
    from STL.STLProcessor import STLProcessor
    stlProcessor = STLProcessor()

if USE_GUI:
    from Simulators.OutputSimulator import OutputSimulator

controller = Controller(USE_SIM)


def main():
    setMountFace(76.6, 80, 110)
    controller.tick()

    if AUTO_TOOLPATH:
        stlProcessor.generateCommands('part3.STL', controller)

    # runDemoPart1()

    ################ Commands go here ################
    from Commands.RaiseCommand import RaiseCommand
    from Commands.CombinedCommand import CombinedCommand
    from Commands.PushCommand import PushCommand
    from Commands.FlipCommand import FlipCommand
    from Commands.PauseCommand import PauseCommand
    from Commands.ShiftCommand import ShiftCommand
    from Commands.SpinCommand import SpinCommand
    from Commands.StopCommand import StopCommand
    from Commands.SequentialCommand import SequentialCommand


    # controller.commandGenerator.resetAll()

    # controller.commandGenerator.selectFace('left')

    # lathe(30, 50, 30)

    controller.commandGenerator.resetAll()

    # controller.commandGenerator.millCircleDiscrete('front', 0, 50, 10, 50)


    # controller.commandGenerator.millPointsSequence([
    #     (0, 10), (-20, 50), (20, 50), (0, 10)
    # ], 30)

    # controller.commandGenerator.resetAll()
    # drill('left', 0, 70, 20)

    # controller.commandGenerator.millPointsSequence([(-5, 70), (5, 70)], 10, 'front')

    # controller.commandGenerator.resetAll()
    # controller.addCommand(RaiseCommand(controller.lathe, 90, controller))
    # controller.addCommand(PushCommand(controller.lathe, 10, controller))
    # lathe(30,50, 30)


    # runDemoPart0()

    ################ End of Commands ################

    # controller.commandGenerator.resetAll()
    # controller.setFace('front')

    controller.start()

    if USE_GUI:
        outputSimulator = OutputSimulator(controller)
        outputSimulator.simulate()

    if AUTO_START:
        controller.goButtonClicked()


    while True:
        controller.tick()
        controller.updateEndeffactorValues()
        if USE_GUI:
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

def millPointsSequence(ptsList, depth, face):
    controller.commandGenerator.millPointsSequence(ptsList, depth, face)


def calibrationRoutine():
    controller.commandGenerator.calibrationRoutine()


def runDemoPart0():
    drill('front', -20, 25, 50)
    drill('front', 20, 25, 50)
    lathe(30, 60, 25)
    cutInCircle('top', 0, 40, 25, 40)
    fillet('top', 38.3, 80, 10, 1, 30)
    fillet('top', -38.3, 80, 10, 2, 30)
    fillet('top', -38.3, 0, 10, 3, 30)
    fillet('top', 38.3, 0, 10, 4, 30)
    intrude('top', 0, 0, 12.5, 80 - 12.5, 40, 40, 6)


def runDemoPart1():
    #12 mins
    reshapeFrontM([(76.6, 20), (40, 90-55-20), (80, 40), (40, 55-20)])
    reshapeSideM([(76.6, 20), (40, 90 - 55 - 20), (80, 40), (40, 55 - 20)])
    lathe(20, 35, 20)
    for face in ['front', 'right', 'back', 'left']:
        cutOutCircle(face, 0, 110-55, 20, 18.3)

    fillet('top', 20, 60, 10, 1, 20)
    fillet('top', -20, 60, 10, 2, 20)
    fillet('top', -20, 20, 10, 3, 20)
    fillet('top', 20, 20, 10, 4, 20)

    drill('front', 0, 110-10, 40+18.3)
    drill('right', 0, 110 - 10, 40 + 18.3)


def runDemoPart2():
    #20min
    reshapeFrontM([(76.6, 20), (65, 5), (70, 5), (60, 110-5-5-20)])
    reshapeSideM([(76.6, 20), (65, 6), (70, 5), (60, 110 - 5 - 5 - 20)])
    lathe(20, 25, 32.5)
    lathe(25, 30, 35)
    lathe(30, 50, 30)
    drill('top', 0, 40, 40)
    fillet('top', 30-10, 40+30-10, 10, 1, 60)
    fillet('top', -30+10, 40+30-10, 10, 2, 60)
    fillet('top', -30+10, 40-30+10, 10, 3, 60)
    fillet('top', 30-10, 40-30+10, 10, 4, 60)


def runDemoPart3():
    reshapeFrontM([(80, 30), (30, 80)])
    lathe(30, 110, 37.5)
    drill('front', -27.5, 100, 72)
    drill('front', -27.5, 40, 72)
    drill('front', 0, 100, 72)
    drill('front', 0, 40, 72)
    drill('front', 27.5, 100, 72)
    drill('front', 27.5, 40, 72)
    intrude('front', -15, -15, 45, 95, 72, 72, 5)
    intrude('front', 15, 15, 45, 95, 72, 72, 5)

if __name__== "__main__":
    main()
