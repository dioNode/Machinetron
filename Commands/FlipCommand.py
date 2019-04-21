from Commands.Command import Command


class FlipCommand(Command):
    """Flips the handler up and down.

    Args:
          handler (Handler): The handler sub machine.
          position (string): The flipping position (up, down).
          startSpeed (double): Initial speed of push (degrees/s).
          endSpeed (double): Final speed of push (degrees/s).

    """
    def __init__(self, handler, position, startSpeed=None, endSpeed=None):
        super().__init__()
        self.name = 'Flipping ' + position
        self.position = position
        if not isinstance(handler, Handler):
            print("SpinCommand: Not a cut machine")
        else:
            self.handler = handler

        # Set speeds
        self.startSpeed = startSpeed if startSpeed is not None else configurationMap[handler.name.lower()]['flipSpeed']
        self.endSpeed = endSpeed if endSpeed is not None else self.startSpeed

    def generateTargets(self):
        targets = {}
        handler = self.handler

        self.targetValue = 0
        if self.position == 'up':
            self.targetValue = 90

        name = handler.name.lower()
        targets[name] = {'flip': {
            'targetValue': self.targetValue,
            'startSpeed': self.startSpeed,
            'endSpeed': self.endSpeed,
            'status': statusMap['started']
            }
        }

        return targets


from SubMachines.Handler import Handler
from support.supportMaps import statusMap

from config import configurationMap
