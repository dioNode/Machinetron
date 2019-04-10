from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap


from config import configurationMap

class PushCommand(Command):
    def __init__(self, cutMachine, depth):
        super().__init__()
        self.name = "Pushing "+cutMachine.name
        self.depth = depth
        if not isinstance(cutMachine, CutMachine):
            print("PushCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine

    def generateTargets(self):
        targets = {}
        cutMachine = self.cutMachine
        speed = configurationMap[cutMachine.name.lower()]['raiseSpeed']

        name = cutMachine.name.lower()
        targets[name] = {'pen': {
            'targetValue': self.depth,
            'startSpeed': speed,
            'endSpeed': speed,
            'status': statusMap['started']
            }
        }

        return targets

