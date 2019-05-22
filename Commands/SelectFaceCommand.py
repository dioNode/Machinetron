from Commands.Command import Command
from Commands.FlipCommand import FlipCommand
from Commands.SpinCommand import SpinCommand
from Commands.CombinedCommand import CombinedCommand


class SelectFaceCommand(Command):
    """Turns the handler to turn the desired face of the foam towards cut machines.

    args:
        face (string): The face to turn towards the cut machines (font, left, right, back, top).
        controller (Controller): The main controller.

    """
    def __init__(self, face, controller):
        super().__init__()
        self.name = 'Selecting ' + face + ' face'
        self.handler = controller.handler
        self.face = face
        controller.setFace(face)

    def generateTargets(self, inSteps=False):
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
        targets = command().generateTargets(inSteps)

        return targets

