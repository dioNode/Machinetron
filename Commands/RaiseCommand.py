from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap

from config import configurationMap

class RaiseCommand(Command):
    def __init__(self, cutMachine, heightDisplacement, startSpeed=None, endSpeed=None):
        super().__init__()
        self.name = "Raising "+cutMachine.name
        self.heightDisplacement = heightDisplacement
        if not isinstance(cutMachine, CutMachine):
            print("RaiseCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine

        # Set speeds
        self.startSpeed = startSpeed if startSpeed is not None else configurationMap[cutMachine.name.lower()]['raiseSpeed']
        self.endSpeed = endSpeed if endSpeed is not None else self.startSpeed

    def generateTargets(self):
        targets = {}
        cutMachine = self.cutMachine

        name = cutMachine.name.lower()
        targets[name] = {'vert': {
            'targetValue': self.heightDisplacement,
            'startSpeed': self.startSpeed,
            'endSpeed': self.endSpeed,
            'status': statusMap['started']
            }
        }

        return targets

