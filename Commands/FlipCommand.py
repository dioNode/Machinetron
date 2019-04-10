from Commands.Command import Command

class FlipCommand(Command):
    def __init__(self, handler, position):
        super().__init__()
        self.name = 'Flipping ' + position
        self.position = position
        if not isinstance(handler, Handler):
            print("SpinCommand: Not a cut machine")
        else:
            self.handler = handler

    def generateTargets(self):
        targets = {}
        handler = self.handler
        speed = configurationMap[handler.name.lower()]['flipSpeed']

        self.targetValue = 0
        if self.position == 'up':
            self.targetValue = 90

        name = handler.name.lower()
        targets[name] = {'flip': {
            'targetValue': self.targetValue,
            'startSpeed': speed,
            'endSpeed': speed,
            'status': statusMap['started']
            }
        }

        return targets


from SubMachines.Handler import Handler
from support.supportMaps import statusMap

from config import configurationMap
