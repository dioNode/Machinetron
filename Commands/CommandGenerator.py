import numpy as np

from Commands.PushCommand import PushCommand
from Commands.SpinCommand import SpinCommand
from Commands.RaiseCommand import RaiseCommand
from Commands.ShiftCommand import ShiftCommand
from Commands.CombinedCommand import CombinedCommand
from Commands.SelectFaceCommand import SelectFaceCommand
from Commands.SelectCutmachineCommand import SelectCutmachineCommand

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
            SelectFaceCommand(face, controller.handler),
            RaiseCommand(controller.mill, controller.currentFaceHeight),
            ShiftCommand(controller.mill, -controller.currentFaceWidth / 2 - radius)
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
        controller.addCommand(PushCommand(controller.mill, 0, controller.currentFaceDepth, startSpeed=2))

    def drill(self, face, x, z, depth):
        # Align to face
        controller = self.controller
        controller.addCommand(SelectFaceCommand(face, controller.handler))
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