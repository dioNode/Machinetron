import numpy as np
import math

from Commands.StopCommand import StopCommand
from Commands.EmptyCommand import EmptyCommand
from Commands.PushCommand import PushCommand
from Commands.SpinCommand import SpinCommand
from Commands.RaiseCommand import RaiseCommand
from Commands.ShiftCommand import ShiftCommand
from Commands.FlipCommand import FlipCommand
from Commands.CombinedCommand import CombinedCommand
from Commands.SelectFaceCommand import SelectFaceCommand
from Commands.SequentialCommand import SequentialCommand
from Commands.PauseCommand import PauseCommand
from support.supportFunctions import getLinearVelocityTime
from config import configurationMap


class CommandGenerator:
    """A class for building complex command instructions.

    Args:
        controller (Controller): The main controller.

    """
    def __init__(self, controller):
        self.controller = controller

    def reshapeM(self, widthHeightTuples, face):
        """Reshapes the surface of the block based on width and heights from bottom up.

        Args:
            widthHeightTuples (tuple array): List of tuples in the form (width, height) starting from bottom.
            face (string): The surface being used in focus and where the widthHeightTuples are based off.

        """
        # Some useful variables to have
        controller = self.controller
        millSpinCommand = SpinCommand(controller.mill)
        radius = configurationMap['mill']['diameter'] / 2

        # Get to initial positioning
        # self.selectFace(face)
        # controller.addCommand(CombinedCommand([
        #     RaiseCommand(controller.mill, 0, rapid=True),
        #     ShiftCommand(controller.mill, controller.handler, -controller.currentFaceWidth / 2 - radius, rapid=True)
        # ], 'Setup initial position and face'))
        self.moveTo(controller.mill, -controller.currentFaceWidth/2 - radius, face=face)

        # Push into depth
        controller.addCommand(CombinedCommand([
            PushCommand(controller.mill, controller.currentFaceDepth, controller),
            millSpinCommand
        ]))

        # Go up left hand side
        currentHeight = 0
        for tupleNum in range(len(widthHeightTuples)):
            widthHeightTuple = widthHeightTuples[tupleNum]
            width, height = widthHeightTuple
            currentHeight += height
            x = -width / 2 - radius
            z = currentHeight + radius
            controller.addCommand(CombinedCommand([ShiftCommand(controller.mill, controller.handler, x), millSpinCommand]))
            controller.addCommand(CombinedCommand([RaiseCommand(controller.mill, z), millSpinCommand]))


        # Go back down right hand side
        for tupleNum in range(len(widthHeightTuples) - 1, -1, -1):
            widthHeightTuple = widthHeightTuples[tupleNum]
            width, height = widthHeightTuple
            currentHeight -= height
            x = width / 2 + radius
            z = currentHeight + radius
            controller.addCommand(CombinedCommand([ShiftCommand(controller.mill, controller.handler, x), millSpinCommand]))
            controller.addCommand(CombinedCommand([RaiseCommand(controller.mill, z), millSpinCommand]))

        # Go back down to bottom
        controller.addCommand(CombinedCommand([RaiseCommand(controller.mill, 0), millSpinCommand]))
        controller.addCommand(PushCommand(controller.mill, 0, controller))

    def drill(self, face, x, z, depth):
        """Uses the drill to drill a hole.

        Args:
            face (string): The face being worked on (front, top, left, right, back).
            x (double): The horizontal displacement of the drill from center.
            z (double): The vertical displacement from the face's bottom of the drill's center point.
            depth (double): Depth of the drill into the foam.

        """
        startSpinOffset = 30
        commandString = ', '.join(['drill(' + '"'+str(face)+'"', str(x), str(z), str(depth)+')'])
        self.controller.writeToHistory(commandString)
        # Align to face
        controller = self.controller
        # z = controller.currentFaceHeight - z
        self.selectFace(face)
        controller.addCommand(CombinedCommand([
            ShiftCommand(controller.drill, controller.handler, x, rapid=True),
            RaiseCommand(controller.drill, z, controller, rapid=True)], 'Align Drill'))
        # Drill in
        controller.addCommand(PushCommand(controller.drill, -startSpinOffset, controller, rapid=True))
        controller.addCommand(CombinedCommand([
            PushCommand(controller.drill, depth, controller),
            SpinCommand(controller.drill)
        ], 'Drill In'))
        controller.addCommand(CombinedCommand([
            PushCommand(controller.drill, -startSpinOffset, controller),
            SpinCommand(controller.drill)
        ], 'Drill Out'))
        # Pull drill out
        self.retractDrill()

    def lathe(self, z0, z1, radius):
        """Uses the lathe to create a radial cut from z0 to z1.

        Args:
            z0 (double): The initial vertical displacement from the face's bottom of the circle's center point.
            z1 (double): The final vertical displacement from the face's bottom of the circle's center point.
            radius (double): Radius of the circle being cut out.

        """
        cuttingDepthOffset = 40
        commandString = ', '.join(['lathe(' + str(z0), str(z1), str(radius)+')'])
        self.controller.writeToHistory(commandString)
        controller = self.controller
        if z0 > z1:
            zBot = z1
            zTop = z0
        else:
            zBot = z0
            zTop = z1

        # Offset to account for lathe length
        latheLength = configurationMap['lathe']['length']
        zTop -= latheLength

        pushIncrement = configurationMap['lathe']['pushIncrement']
        self.selectFace('front')


        handlerSpinCommand = SpinCommand(controller.handler, rapid=True)

        # Set starting positions
        controller.addCommand(CombinedCommand([
            RaiseCommand(controller.lathe, zBot, controller, rapid=True),
            ShiftCommand(controller.lathe, controller.handler, 0, rapid=True),
        ]))
        controller.addCommand(RaiseCommand(controller.lathe, zTop, controller, rapid=True))
        # Push it close first
        controller.addCommand(PushCommand(controller.lathe, -cuttingDepthOffset, controller, rapid=True))

        # Start lathing
        maxRadius = max(controller.currentFaceDepth, controller.currentFaceWidth) / 2
        sequenceCommand = SequentialCommand([])
        sequenceCommand.addCommand(SpinCommand(controller.handler, 360*5, configurationMap['handler']['initialRampUpSpeed'],
                                          configurationMap['handler']['rapidSpinSpeed']))
        sequenceCommand.addCommand(handlerSpinCommand)

        for currentRadius in np.arange(maxRadius, radius, -pushIncrement):
            # Push in
            sequenceCommand.addCommand(CombinedCommand([
                PushCommand(controller.lathe, currentRadius, controller, fromCenter=True),
                handlerSpinCommand
            ], 'Push Lathe in'))
            # Go up
            sequenceCommand.addCommand(CombinedCommand([
                RaiseCommand(controller.lathe, zTop, controller),
                handlerSpinCommand
            ], 'Lathe Up'))
            # Back down
            sequenceCommand.addCommand(CombinedCommand([
                RaiseCommand(controller.lathe, zBot, controller),
                handlerSpinCommand
            ], 'Lathe Down'))

        controller.addCommand(sequenceCommand)

        # if not controller.useSimulator:
        #     controller.addCommand(StopCommand())

        self.retractLathe()

    def resetAll(self):
        """Resets all the sub machines to their default starting state.

        All the sub machines should move towards their 0 location until the limit switches are hit. This command should
        generally be called on start and finish of a piece.

        """
        self.homeMill()
        self.homeLathe()
        self.homeDrill()
        self.homeHandler()


    def millArcDiscrete(self, face, x, z, radius, depth, startAngle, endAngle):
        """Uses the mill to cut out in an arc shape.

        All variables are relative to the center of the mill cutting tool so functions that use this command will need
        to keep in mind to offset by the mill cutting tool's radius if needed. The starting and ending angles are all
        in degrees. The zero starts on the right axis and moves in the clockwise direction.

        Args:
            face (string): The surface being worked on (front, left, right, top, back).
            x (double): The horizontal displacement of center point of the mill arc.
            z (double): The vertical displacement of the center point of the mill arc.
            radius (double): The radius that the mill is working around.
            depth (double): The depth of the mill from the foam surface.
            startAngle(double): The starting angle of the mill in radians.
            endAngle(double): The ending angle of the mill in radians.

        """
        motorStartOffset = configurationMap['mill']['offsets']['motorStartDepthOffset']
        sequentialCommand = SequentialCommand([])
        # Set starting location
        self.selectFace(face)
        # Start with top right quadrant
        actualZ = z
        angle = startAngle
        currentX = x + radius * math.cos(angle)
        currentZ = actualZ + radius * math.sin(angle)
        self.controller.addCommand(CombinedCommand([
            ShiftCommand(self.controller.mill, self.controller.handler, currentX, rapid=True),
            RaiseCommand(self.controller.mill, currentZ, self.controller, rapid=True),
        ]))
        # Move closer to foam
        self.controller.addCommand(PushCommand(self.controller.mill, -motorStartOffset, self.controller, rapid=True))

        # Insert mill into foam
        self.controller.addCommand(CombinedCommand([
            PushCommand(self.controller.mill, depth, self.controller),
            SpinCommand(self.controller.mill),
        ]))

        maxStep = 1
        minSpeed = 1
        # Figure out synchronizing speed
        moveSpeed = min(configurationMap['handler']['railSpeed'], configurationMap['mill']['raiseSpeed'])
        angleStep = 2 * math.asin(maxStep / (2 * radius))
        distPerPoint = 2 * radius * math.sin(angleStep/2)
        timePerPoint = distPerPoint / moveSpeed
        if radius != 0:
            for angle in np.arange(startAngle, endAngle, angleStep):
                prevX = currentX
                prevZ = currentZ
                currentX = x + radius * math.cos(angle)
                currentZ = actualZ + radius * math.sin(angle)
                dx = abs(currentX - prevX)
                dz = abs(currentZ - prevZ)
                # Time for each movement
                tx = max(dx / timePerPoint, minSpeed)
                tz = max(dz / timePerPoint, minSpeed)
                sequentialCommand.addCommand(CombinedCommand([
                    SpinCommand(self.controller.mill),
                    ShiftCommand(self.controller.mill, self.controller.handler, currentX, startSpeed=tx),
                    RaiseCommand(self.controller.mill, currentZ, self.controller, startSpeed=tz),
                ]))
        # angle = endAngle
        # currentX = x + radius * math.cos(angle)
        # currentZ = actualZ + radius * math.sin(angle)
        # syncSpeed = configurationMap['other']['syncSpeed']
        # sequentialCommand.addCommand(CombinedCommand([
        #     SpinCommand(self.controller.mill),
        #     ShiftCommand(self.controller.mill, self.controller.handler, currentX, startSpeed=syncSpeed),
        #     RaiseCommand(self.controller.mill, currentZ, self.controller, startSpeed=syncSpeed),
        # ]))
        self.controller.addCommand(sequentialCommand)
        self.retractMill()

    def cutInCircle(self, face, x, z, radius, depth):
        """Completely cuts out the inside of a given circle.

        Args:
            face (string): The face being worked on (front, top, left, right, back).
            x (double): The horizontal displacement from the face's center of the center of the circle's center point.
            z (double): The vertical displacement from the face's bottom of the circle's center point.
            radius (double): Radius of the circle being cut out.
            depth (double): Depth of the circle being cut out.

        """
        self.selectFace(face)
        millRadius = configurationMap['mill']['diameter'] / 2
        # Go through and cut out from inner to out
        for r in np.arange(millRadius, radius-millRadius, millRadius*2):
            self.millCircleDiscrete(face, x, z, r, depth)
        self.millCircleDiscrete(face, x, z, radius - millRadius, depth)

    def cutOutCircle(self, face, x, z, radius, depth):
        """Cuts once around the outside of the circle.

        This assumes that the mill only needs to go around the outer border once and extra foam with fall off.

        Args:
            face (string): The face being worked on (front, top, left, right, back).
            x (double): The horizontal displacement from the face's center of the center of the circle's center point.
            z (double): The vertical displacement from the face's bottom of the circle's center point.
            radius (double): Radius of the circle being cut out.
            depth (double): Depth of the circle being cut out.

        """
        self.selectFace(face)
        millRadius = configurationMap['mill']['diameter'] / 2
        self.millCircleDiscrete(face, x, z, radius + millRadius, depth)
        # Retract mill
        self.retractMill()

    def millCircleDiscrete(self, face, x, z, radius, depth):
        """Mills a full circle cut out from the center point of the mill using discrete steps.

        Args:
            face (string): The face being worked on (front, top, left, right, back).
            x (double): The horizontal displacement from the face's center of the center of the circle's center point.
            z (double): The vertical displacement from the face's bottom of the circle's center point.
            radius (double): Radius of the circle being cut out.
            depth (double): Depth of the circle being cut out.

        """
        self.millArcDiscrete(face, x, z, radius, depth, 0, 2*math.pi)

    def millCircle(self, face, x, z, radius, depth):
        """Mills a full circle cut out from the center point of the mill using smooth curves.

        Args:
            face (string): The face being worked on (front, top, left, right, back).
            x (double): The horizontal displacement from the face's center of the center of the circle's center point.
            z (double): The vertical displacement from the face's bottom of the circle's center point.
            radius (double): Radius of the circle being cut out.s
            depth (double): Depth of the circle being cut out.

        """
        # Set starting location
        # Start with top right quadrant
        actualZ = self.controller.currentFaceHeight - z
        currentZ = actualZ
        currentX = x + radius
        self.selectFace(face)
        self.controller.addCommand(CombinedCommand([
            ShiftCommand(self.controller.mill, self.controller.handler, currentX, rapid=True),
            RaiseCommand(self.controller.mill, currentZ, self.controller, rapid=True),
        ]))
        self.controller.addCommand(CombinedCommand([
            PushCommand(self.controller.mill, depth, self.controller),
            SpinCommand(self.controller.mill),
        ]))

        # Move to right
        fastSpeed = 30
        slowSpeed = 5
        timeTaken = getLinearVelocityTime(fastSpeed, slowSpeed, radius)
        constantSpeed = radius / timeTaken
        # Curve to top
        self.controller.addCommand(CombinedCommand([
            SpinCommand(self.controller.mill),
            RaiseCommand(self.controller.mill, actualZ - radius, self.controller, startSpeed=slowSpeed, endSpeed=fastSpeed*2),
            ShiftCommand(self.controller.mill, self.controller.handler, x, startSpeed=fastSpeed, endSpeed=slowSpeed)
        ]))
        # Curve to left
        self.controller.addCommand(CombinedCommand([
            SpinCommand(self.controller.mill),
            RaiseCommand(self.controller.mill, actualZ, self.controller, startSpeed=constantSpeed),
            ShiftCommand(self.controller.mill, self.controller.handler, x - radius, startSpeed=slowSpeed, endSpeed=fastSpeed)
        ]))
        # Curve to bottom
        self.controller.addCommand(CombinedCommand([
            SpinCommand(self.controller.mill),
            RaiseCommand(self.controller.mill, actualZ + radius, self.controller, startSpeed=constantSpeed),
            ShiftCommand(self.controller.mill, self.controller.handler, x, startSpeed=fastSpeed, endSpeed=slowSpeed)
        ]))
        # Curve back to right
        self.controller.addCommand(CombinedCommand([
            SpinCommand(self.controller.mill),
            RaiseCommand(self.controller.mill, currentZ, self.controller, startSpeed=constantSpeed),
            ShiftCommand(self.controller.mill, self.controller.handler, currentX, startSpeed=slowSpeed, endSpeed=fastSpeed)
        ]))

    def fillet(self, face, x, z, radius, quadrant, depth):
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
        if quadrant == 1:
            startAngle = 0
            endAngle = math.pi/2
            x -= radius
            z -= radius
        elif quadrant == 2:
            startAngle = math.pi/2
            endAngle = math.pi
            x += radius
            z -= radius
        elif quadrant == 3:
            startAngle = math.pi
            endAngle = 3*math.pi/2
            x += radius
            z += radius
        elif quadrant == 4:
            startAngle = 3*math.pi/2
            endAngle = 2 * math.pi
            x -= radius
            z += radius
        else:
            print('Quadrant not valid')
            startAngle = 0
            endAngle = 0
        radius += configurationMap['mill']['diameter']/2
        self.millArcDiscrete(face, x, z, radius, depth, startAngle, endAngle)
        self.retractMill()

    def retractMill(self):
        """Stops the mill spin and pulls the mill back to base position."""
        self.controller.addCommand(PushCommand(self.controller.mill, 0, self.controller, home=True, rapid=True))

    def retractDrill(self):
        """Stops the drill spin and pulls the drill back to base position."""
        self.controller.addCommand(PushCommand(self.controller.drill, 0, self.controller, home=True, rapid=True))

    def retractLathe(self):
        """Stops the handler spin and pulls the lathe back to base position."""
        self.controller.addCommand(CombinedCommand([
            PushCommand(self.controller.lathe, 0, self.controller, rapid=True, home=True),
            SpinCommand(self.controller.handler, 0, home=True)
        ]))

    def homeCutmachine(self, cutmachine):
        self.controller.addCommand(PushCommand(cutmachine, 0, self.controller, home=True, rapid=True))
        self.controller.addCommand(RaiseCommand(cutmachine, 0, self.controller, home=True, rapid=True))

    def homeMill(self):
        self.homeCutmachine(self.controller.mill)

    def homeLathe(self):
        self.homeCutmachine(self.controller.lathe)

    def homeDrill(self):
        self.homeCutmachine(self.controller.drill)

    def homeHandler(self):
        self.controller.addCommand(FlipCommand(self.controller.handler, 'down', home=True))
        self.controller.addCommand(CombinedCommand([
            ShiftCommand(self.controller.drill, self.controller.handler, 0,
                         inAbsolute=True, home=True, rapid=True),
            SpinCommand(self.controller.handler, 0, home=True),
        ]))

    def selectFace(self, face):
        """Rotates the handler to turn the desired face towards the cut machines.

        Args:
            face (string): The face to turn towards the cut machines.

        """
        self.controller.setFace(face)
        self.controller.addCommand(SelectFaceCommand(face, self.controller))

    def moveTo(self, cutMachine, x, z, d=None, face=None):
        """Moves the handler towards the desired location.

        Args:
            cutMachine (CutMachine): The cut machine that is in focus.
            x (double): The horizontal displacement of the cutting tool from the center of the foam.
            z (double): The vertical displacement of the cutting tool from the bottom of the foam.
            d (double): The depth of the cutting tool into the surface of the foam.
            face (string): The face that is being worked on. This can be left None to use current face.

        """
        d = -configurationMap[cutMachine.name.lower()]['offsets']['motorStartDepthOffset'] if d is None else d
        # Ensure cutmachine is retracted
        self.controller.addCommand(PushCommand(cutMachine, d, self.controller, rapid=True, home=True))
        # Select the right face
        if face is not None:
            self.selectFace(face)
        # Move to specific position
        moveCommand = CombinedCommand([
            ShiftCommand(cutMachine, self.controller.handler, x, rapid=True),
            RaiseCommand(cutMachine, z, self.controller, rapid=True),
        ])
        # Move to spot and push cutmachine in
        self.controller.addCommand(moveCommand)
        self.controller.addCommand(PushCommand(cutMachine, d, self.controller, rapid=True))

    def intrude(self, face, x0, x1, z0, z1, d0, d1, radius):
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
        self.selectFace(face)
        controller = self.controller
        if z0 > z1:
            zLow = z1
            xLow = x1
            dLow = d1
            zHigh = z0
            xHigh = x0
            dHigh = d0
        else:
            zLow = z0
            xLow = x0
            dLow = d0
            zHigh = z1
            xHigh = x1
            dHigh = d1
        millRadius = configurationMap['mill']['diameter']/2
        speed = configurationMap['coordination']['speed']
        # Calculate speed coordinations
        xDiff = abs(x1 - x0)
        zDiff = abs(z1 - z0)
        dDiff = abs(d1 - d0)
        maxDiff = max([xDiff, zDiff, dDiff])
        xSpeed = speed * xDiff / maxDiff if xDiff != 0 else 1
        zSpeed = speed * zDiff / maxDiff if zDiff != 0 else 1
        dSpeed = speed * dDiff / maxDiff if dDiff != 0 else 1

        tiltAngle = np.arctan2(zHigh-zLow, xHigh-xLow) + np.pi/2
        r = radius-millRadius
        if r < 0:
            print('WARNING intrude radius too small')
        # Start at top left
        self.moveTo(controller.mill, xHigh - r*np.cos(tiltAngle), zHigh - r*np.sin(tiltAngle), 0)
        # Push in
        self.controller.addCommand(self.getSpinningPushCommand(controller.mill, dHigh))

        radiusRange = np.arange(radius-millRadius, 0, -millRadius*2)
        if float(radius) == float(millRadius):
            radiusRange = np.append(radiusRange, 0)
        for r in radiusRange:
            # Half circle around to right hand side
            self.millArcDiscrete(face, xHigh, zHigh, r, dHigh,
                                 math.pi + tiltAngle, 2*math.pi + tiltAngle)
            # Move down to bottom right
            self.controller.addCommand(CombinedCommand([
                SpinCommand(controller.mill),
                RaiseCommand(controller.mill, zLow + r*np.sin(tiltAngle), controller, startSpeed=zSpeed),
                ShiftCommand(controller.mill, controller.handler, xLow + r*np.cos(tiltAngle), startSpeed=xSpeed),
                PushCommand(controller.mill, dLow, controller, startSpeed=dSpeed)
            ]))
            # Half circle around to left hand side
            self.millArcDiscrete(face, xLow, zLow, r,
                                 dLow, 0 + tiltAngle, math.pi + tiltAngle)
            # Move up to top left
            self.controller.addCommand(CombinedCommand([
                SpinCommand(controller.mill),
                RaiseCommand(controller.mill, zHigh - r*np.sin(tiltAngle), controller, startSpeed=zSpeed),
                ShiftCommand(controller.mill, controller.handler, xHigh - r*np.cos(tiltAngle), startSpeed=xSpeed),
                PushCommand(controller.mill, dHigh, controller, startSpeed=dSpeed)
            ]))
        self.retractMill()

    def getSpinningPushCommand(self, cutMachine, d):
        """Generates a command of a cut machine pushing while spinning.

        Args:
            cutMachine (CutMachine): The cut machine in focus.
            d (depth): The depth of the cutting tool into the foam face.

        """
        return CombinedCommand([
            PushCommand(cutMachine, d, self.controller),
            SpinCommand(cutMachine)
        ])

    def pauseCommand(self):
        """Sends a command to the submachines to pause all motion. This does not pause the Raspberry Pi."""
        self.controller.addCommand(PauseCommand())

    def calibrateCutmachine(self, cutmachine):
        """Checks the endpoints of each cutmachine by looking at where it touches the edge of the foam.

        Args:
            cutmachine (CutMachine): The cutmachine you want to test.

        """
        # Move to bottom left corner
        self.controller.addCommand(CombinedCommand([
            ShiftCommand(cutmachine, self.controller.handler, -38.8, rapid=True),
            RaiseCommand(cutmachine, 0, self.controller, rapid=True)
        ]))
        # Poke foam
        self.controller.addCommand(PushCommand(cutmachine, 0, self.controller, rapid=True))
        self.pauseCommand()
        self.controller.addCommand(PushCommand(cutmachine, 0, self.controller, home=True, rapid=True))

        # Move to top right corner
        self.controller.addCommand(CombinedCommand([
            ShiftCommand(cutmachine, self.controller.handler, 38.8, rapid=True),
            RaiseCommand(cutmachine, 110, self.controller, rapid=True)
        ]))
        # Poke foam
        self.controller.addCommand(PushCommand(cutmachine, 0, self.controller, rapid=True))
        self.pauseCommand()
        self.controller.addCommand(PushCommand(cutmachine, 0, self.controller, home=True, rapid=True))


    def calibrateHandler(self):
        self.controller.addCommand(FlipCommand(self.controller.handler, 'up'))
        self.pauseCommand()
        self.controller.addCommand(FlipCommand(self.controller.handler, 'down'))


    def calibrationRoutine(self):
        """A routine used to check if the coordinate system is calibrated correctly in real life.

        This goes around for each cutmachine and uses its cutting tool to poke the top left and bottom right corner of
        the foam. It then checks the flip mechanism for the Handler. The routine pauses after every step to give the
        user time to take measurements.

        """
        self.resetAll()
        cutmachines = [self.controller.mill, self.controller.lathe, self.controller.drill]
        # self.controller.addCommand(FlipCommand(self.controller.handler, 'up'))
        for cutmachine in cutmachines:
            self.calibrateCutmachine(cutmachine)
        # self.calibrateHandler()

    def millPointsSequence(self, ptsList, depth, face):
        """Uses the mill to cut through a sequence of points in order.

        Args:
            ptsList (List(tuples)): A list of x, z coordinate tuples for the path you want the mill to follow.
            depth (double): The depth of the path in the foam.
            face (String): The face you want to work on.

        """
        startDepthOffset = 40

        commandString = ', '.join(['millPointSequence(' + str(ptsList), str(depth), '"' + face + '")'])
        self.controller.writeToHistory(commandString)
        self.selectFace(face)
        # Go to starting point
        (x0, z0) = ptsList[0] if len(ptsList) > 0 else (0,0)
        self.moveTo(self.controller.mill, x0, z0, -startDepthOffset)

        # Push in with mill to depth
        self.controller.addCommand(CombinedCommand([
            PushCommand(self.controller.mill, depth, self.controller),
            SpinCommand(self.controller.mill)
        ]))

        # Make mill go through all the points in sequence
        sequenceCommand = SequentialCommand([])
        for (x, z) in ptsList:
            sequenceCommand.addCommand(CombinedCommand([
                SpinCommand(self.controller.mill),
                RaiseCommand(self.controller.mill, z, self.controller),
                ShiftCommand(self.controller.mill, self.controller.handler, x),
            ]))
        self.controller.addCommand(sequenceCommand)

        # Retract mill
        self.controller.addCommand(CombinedCommand([
            PushCommand(self.controller.mill, -startDepthOffset, self.controller),
            SpinCommand(self.controller.mill)
        ]))
        self.retractMill()

