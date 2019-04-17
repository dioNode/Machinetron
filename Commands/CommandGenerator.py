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
        controller.addCommand(SelectFaceCommand(face, controller))
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
        self.controller.addCommand(SelectFaceCommand(face, self.controller))
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
        self.controller.addCommand(CombinedCommand([
            SpinCommand(self.controller.mill),
            ShiftCommand(self.controller.mill, x + radius),
            RaiseCommand(self.controller.mill, actualZ),
        ]))

    def cutInCircle(self, face, x, z, radius, depth):
        self.controller.addCommand(SelectFaceCommand(face, self.controller))
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
        elif quadrant == 2:
            startAngle = 2*math.pi
            endAngle = 3*math.pi/2
        elif quadrant == 3:
            startAngle = math.pi/2
            endAngle = 2*math.pi
        elif quadrant == 4:
            startAngle = 0
            endAngle = math.pi/2
        else:
            print('Quadrant not valid')
            startAngle = 0
            endAngle = 0
        self.millArcDiscrete(face, x, z, radius, depth, startAngle, endAngle)

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
