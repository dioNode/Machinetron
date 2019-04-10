from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap

from config import configurationMap

class RaiseCommand(Command):
    def __init__(self, cutMachine, heightDisplacement):
        super().__init__()
        self.name = "Raising "+cutMachine.name
        self.heightDisplacement = heightDisplacement
        if not isinstance(cutMachine, CutMachine):
            print("RaiseCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine

    def generateTargets(self):
        targets = {}
        cutMachine = self.cutMachine
        speed = configurationMap[cutMachine.name.lower()]['raiseSpeed']

        name = cutMachine.name.lower()
        targets[name] = {'vert': {
            'targetValue': self.heightDisplacement,
            'startSpeed': speed,
            'endSpeed': speed,
            'status': statusMap['started']
            }
        }

        return targets

