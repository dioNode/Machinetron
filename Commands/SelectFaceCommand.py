from Commands.Command import Command
from Commands.FlipCommand import FlipCommand
from Commands.SpinCommand import SpinCommand
from Commands.CombinedCommand import CombinedCommand
from support.supportMaps import statusMap, faceMap

from config import configurationMap

class SelectFaceCommand(Command):
    def __init__(self, face, controller):
        super().__init__()
        self.name = 'Selecting ' + face + ' face'
        self.handler = controller.handler
        self.face = face
        controller.setFace(face)

    def generateTargets(self):
        face = self.face

        def front():
            return CombinedCommand([
                SpinCommand(self.handler, 0),
                FlipCommand(self.handler, 'down')
            ])
        def back():
            return CombinedCommand([
                SpinCommand(self.handler, 180),
                FlipCommand(self.handler, 'down')
            ])
        def left():
            return CombinedCommand([
                SpinCommand(self.handler, -90),
                FlipCommand(self.handler, 'down')
            ])
        def right():
            return CombinedCommand([
                SpinCommand(self.handler, 90),
                FlipCommand(self.handler, 'down')
            ])
        def top():
            return CombinedCommand([
                SpinCommand(self.handler, 0),
                FlipCommand(self.handler, 'up')
            ])

        switcher = {
            'front': front,
            'back': back,
            'left': left,
            'right': right,
            'top': top,
        }

        command = switcher.get(face)
        targets = command().generateTargets()

        return targets

