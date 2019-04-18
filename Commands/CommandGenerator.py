import numpy as np
import math

from Commands.PushCommand import PushCommand
from Commands.SpinCommand import SpinCommand
from Commands.RaiseCommand import RaiseCommand
from Commands.ShiftCommand import ShiftCommand
from Commands.CombinedCommand import CombinedCommand
from Commands.SelectFaceCommand import SelectFaceCommand
from Commands.SelectCutmachineCommand import SelectCutmachineCommand

from support.supportFunctions import getLinearVelocityTime
from config import configurationMap

class CommandGenerator:
    def __init__(self, controller):
        self.controller = controller

    def reshapeM(self, widthHeightTuples, face):
        # Some useful variables to have
        controller = self.controller
        millSpinCommand = SpinCommand(controller.mill)
        radius = configurationMap['mill']['diameter'] / 2

        # Get to initial positioning
        controller.addCommand(CombinedCommand([
            SelectFaceCommand(face, controller),
            RaiseCommand(controller.mill, controller.currentFaceHeight),
            ShiftCommand(controller.mill, -controller.currentFaceWidth / 2 - radius, startSpeed=200, endSpeed=50)
        ], 'Setup initial position and face'))

        # Push into depth
        controller.addCommand(CombinedCommand([
            PushCommand(controller.mill, controller.currentFaceDepth, controller.currentFaceDepth),
            millSpinCommand
        ]))

        # Go up left hand side
        currentHeight = 0
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
        controller.addCommand(CombinedCommand([RaiseCommand(controller.mill, controller.currentFaceHeight), millSpinCommand]))
        controller.addCommand(PushCommand(controller.mill, 0, controller.currentFaceDepth))

    def drill(self, face, x, z, depth):
        # Align to face
        controller = self.controller
        z = controller.currentFaceHeight - z
        self.selectFace(face)
        controller.addCommand(CombinedCommand([
            ShiftCommand(controller.drill, x),
            RaiseCommand(controller.drill, z)], 'Align Drill'))
        # Drill in
        controller.addCommand(CombinedCommand([
            PushCommand(controller.drill, depth, controller.currentFaceDepth),
            SpinCommand(controller.drill)
        ], 'Drill In'))
        # Pull drill out
        controller.addCommand(PushCommand(controller.drill, 0, controller.currentFaceDepth))

    def lathe(self, z0, z1, radius):
        controller = self.controller
        if z0 > z1:
            zBot = controller.currentFaceHeight - z1
            zTop = controller.currentFaceHeight - z0
        else:
            zBot = controller.currentFaceHeight - z0
            zTop = controller.currentFaceHeight - z1

        # Offset to account for lathe length
        latheLength = configurationMap['lathe']['length']
        zTop += latheLength

        pushIncrement = configurationMap['lathe']['pushIncrement']
        handlerSpinCommand = SpinCommand(controller.handler)
        # Set starting positions
        controller.addCommand(CombinedCommand([
            SpinCommand(controller.handler, 0),
            RaiseCommand(controller.lathe, 0),
            ShiftCommand(controller.lathe, 0),
        ]))
        controller.addCommand(RaiseCommand(controller.lathe, zTop))

        # Start lathing
        maxRadius = max(controller.currentFaceDepth, controller.currentFaceWidth) / 2
        for currentRadius in np.arange(maxRadius, radius, -pushIncrement):
            # Push in
            controller.addCommand(CombinedCommand([
                PushCommand(controller.lathe, currentRadius, controller.currentFaceDepth, True),
                handlerSpinCommand
            ], 'Push Lathe in'))
            # Go down
            controller.addCommand(CombinedCommand([
                RaiseCommand(controller.lathe, zBot),
                handlerSpinCommand
            ], 'Lathe Down'))
            # Back up
            controller.addCommand(CombinedCommand([
                RaiseCommand(controller.lathe, zTop),
                handlerSpinCommand
            ], 'Lathe Up'))

        self.resetAll()

    def resetAll(self):
        # Remove all potential cutting bits from workpiece
        controller = self.controller
        controller.addCommand(CombinedCommand([
            PushCommand(controller.drill, 0, controller.currentFaceDepth),
            PushCommand(controller.mill, 0, controller.currentFaceDepth),
            PushCommand(controller.lathe, 0, controller.currentFaceDepth),
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

    def millArcDiscrete(self, face, x, z, radius, depth, startAngle, endAngle):
        # Set starting location
        self.selectFace(face)
        # Start with top right quadrant
        actualZ = self.controller.currentFaceHeight - z
        angle = startAngle
        currentX = x + radius * math.cos(angle)
        currentZ = actualZ + radius * math.sin(angle)
        self.controller.addCommand(CombinedCommand([
            ShiftCommand(self.controller.mill, currentX),
            RaiseCommand(self.controller.mill, currentZ),
        ]))
        self.controller.addCommand(CombinedCommand([
            PushCommand(self.controller.mill, depth, self.controller.currentFaceDepth),
            SpinCommand(self.controller.mill),
        ]))

        maxStep = 1
        angleStep = 2 * math.asin(maxStep / (2 * radius))
        for angle in np.arange(startAngle, endAngle, angleStep):
            currentX = x + radius * math.cos(angle)
            currentZ = actualZ + radius * math.sin(angle)
            self.controller.addCommand(CombinedCommand([
                SpinCommand(self.controller.mill),
                ShiftCommand(self.controller.mill, currentX),
                RaiseCommand(self.controller.mill, currentZ),
            ]))
        angle = endAngle
        currentX = x + radius * math.cos(angle)
        currentZ = actualZ + radius * math.sin(angle)
        self.controller.addCommand(CombinedCommand([
            SpinCommand(self.controller.mill),
            ShiftCommand(self.controller.mill, currentX),
            RaiseCommand(self.controller.mill, currentZ),
        ]))

    def cutInCircle(self, face, x, z, radius, depth):
        self.selectFace(face)
        millRadius = configurationMap['mill']['diameter'] / 2
        # Go through and cut out from inner to out
        for r in np.arange(millRadius, radius-millRadius, millRadius*2):
            self.millCircleDiscrete(face, x, z, r, depth)
        self.millCircleDiscrete(face, x, z, radius - millRadius, depth)

    def cutOutCircle(self, face, x, z, radius, depth):
        self.controller.addCommand(SelectFaceCommand(face, self.controller))
        millRadius = configurationMap['mill']['diameter'] / 2
        self.millCircleDiscrete(face, x, z, radius + millRadius, depth)
        # Retract mill
        self.retractMill()

    def millCircleDiscrete(self, face, x, z, radius, depth):
        self.millArcDiscrete(face, x, z, radius, depth, 0, 2*math.pi)

    def millCircle(self, face, x, z, radius, depth):
        # Set starting location
        # Start with top right quadrant
        actualZ = self.controller.currentFaceHeight - z
        currentZ = actualZ
        currentX = x + radius
        self.controller.addCommand(CombinedCommand([
            SelectFaceCommand(face, self.controller),
            ShiftCommand(self.controller.mill, currentX),
            RaiseCommand(self.controller.mill, currentZ),
        ]))
        self.controller.addCommand(CombinedCommand([
            PushCommand(self.controller.mill, depth, self.controller.currentFaceDepth),
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
            RaiseCommand(self.controller.mill, actualZ - radius, startSpeed=slowSpeed, endSpeed=fastSpeed*2),
            ShiftCommand(self.controller.mill, x, startSpeed=fastSpeed, endSpeed=slowSpeed)
        ]))
        # Curve to left
        self.controller.addCommand(CombinedCommand([
            SpinCommand(self.controller.mill),
            RaiseCommand(self.controller.mill, actualZ, startSpeed=constantSpeed),
            ShiftCommand(self.controller.mill, x - radius, startSpeed=slowSpeed, endSpeed=fastSpeed)
        ]))
        # Curve to bottom
        self.controller.addCommand(CombinedCommand([
            SpinCommand(self.controller.mill),
            RaiseCommand(self.controller.mill, actualZ + radius, startSpeed=constantSpeed),
            ShiftCommand(self.controller.mill, x, startSpeed=fastSpeed, endSpeed=slowSpeed)
        ]))
        # Curve back to right
        self.controller.addCommand(CombinedCommand([
            SpinCommand(self.controller.mill),
            RaiseCommand(self.controller.mill, currentZ, startSpeed=constantSpeed),
            ShiftCommand(self.controller.mill, currentX, startSpeed=slowSpeed, endSpeed=fastSpeed)
        ]))

    def fillet(self, face, x, z, radius, quadrant, depth):
        if quadrant == 1:
            startAngle = 3*math.pi/2
            endAngle = 2*math.pi
            x -= radius
            z -= radius
        elif quadrant == 2:
            startAngle = math.pi
            endAngle = 3*math.pi/2
            x += radius
            z -= radius
        elif quadrant == 3:
            startAngle = math.pi/2
            endAngle = math.pi
            x += radius
            z += radius
        elif quadrant == 4:
            startAngle = 0
            endAngle = math.pi/2
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
        self.controller.addCommand(PushCommand(self.controller.mill, 0, self.controller.currentFaceDepth))

    def retractDrill(self):
        self.controller.addCommand(PushCommand(self.controller.drill, 0, self.controller.currentFaceDepth))

    def retractLathe(self):
        self.controller.addCommand(CombinedCommand([
            PushCommand(self.controller.lathe, 0, self.controller.currentFaceDepth),
            SpinCommand(self.controller.handler, 0)
        ]))

    def selectFace(self, face):
        self.controller.addCommand(SelectFaceCommand(face, self.controller))

    def moveTo(self, cutMachine, x, z, d, face=None):
        moveCommand = CombinedCommand([
            ShiftCommand(cutMachine, x),
            RaiseCommand(cutMachine, z),
            PushCommand(cutMachine, d, self.controller.currentFaceDepth)
        ])
        if face is not None:
            moveCommand = CombinedCommand([
                moveCommand,
                SelectFaceCommand(face, self.controller)
            ])
        self.controller.addCommand(moveCommand)

    def intrude(self, face, x0, x1, z0, z1, d0, d1, radius):
        self.selectFace(face)
        controller = self.controller
        if z0 > z1:
            zLow = controller.currentFaceHeight - z1
            xLow = x1
            dLow = d1
            zHigh = controller.currentFaceHeight - z0
            xHigh = x0
            dHigh = d0
        else:
            zLow = controller.currentFaceHeight - z0
            xLow = x0
            dLow = d0
            zHigh = controller.currentFaceHeight - z1
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

        # print(zHigh-zLow, xHigh-xLow)
        print(xDiff, zDiff)
        tiltAngle = np.arctan2(zHigh-zLow, xHigh-xLow) + np.pi/2
        print('tiltANgle', tiltAngle)
        r = radius-millRadius
        if r < 0:
            print('WARNING intrude radius too small')
        # Start at top left
        self.moveTo(controller.mill, xHigh - r*np.cos(tiltAngle), zHigh - r*np.sin(tiltAngle), 0)
        # Push in
        self.controller.addCommand(self.getSpinningPushCommand(controller.mill, dHigh))
        for r in np.arange(radius-millRadius, 0, -millRadius*2):
            # Half circle around to right hand side
            self.millArcDiscrete(face, xHigh, self.controller.currentFaceHeight - zHigh, r, dHigh,
                                 math.pi + tiltAngle, 2*math.pi + tiltAngle)
            # Move down to bottom right
            self.controller.addCommand(CombinedCommand([
                SpinCommand(controller.mill),
                RaiseCommand(controller.mill, zLow + r*np.sin(tiltAngle), startSpeed=zSpeed),
                ShiftCommand(controller.mill, xLow + r*np.cos(tiltAngle), startSpeed=xSpeed),
                PushCommand(controller.mill, dLow, controller.currentFaceDepth, startSpeed=dSpeed)
            ]))
            # Half circle around to left hand side
            self.millArcDiscrete(face, xLow, self.controller.currentFaceHeight - zLow, r,
                                 dLow, 0 + tiltAngle, math.pi + tiltAngle)
            # Move up to top left
            self.controller.addCommand(CombinedCommand([
                SpinCommand(controller.mill),
                RaiseCommand(controller.mill, zHigh - r*np.sin(tiltAngle), startSpeed=zSpeed),
                ShiftCommand(controller.mill, xHigh - r*np.cos(tiltAngle), startSpeed=xSpeed),
                PushCommand(controller.mill, dHigh, controller.currentFaceDepth, startSpeed=dSpeed)
            ]))
        self.retractMill()

    def getSpinningPushCommand(self, cutMachine, d):
        return CombinedCommand([
            PushCommand(cutMachine, d, self.controller.currentFaceDepth),
            SpinCommand(cutMachine)
        ])

