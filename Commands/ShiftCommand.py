from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap

from config import configurationMap

class ShiftCommand(Command):
    def __init__(self, cutMachine, horizontalDisplacement):
        super().__init__()
        self.name = "Shifting "+cutMachine.name
        self.horizontalDisplacement = horizontalDisplacement
        if not isinstance(cutMachine, CutMachine):
            print("ShiftCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine

    def generateTargets(self):
        targets = {}
        cutMachine = self.cutMachine
        globalTargetX = self.horizontalDisplacement + cutMachine.homeX

        targets['handler'] = {'rail': {
            'targetValue': globalTargetX,
            'startSpeed': configurationMap['handler']['railSpeed'],
            'endSpeed': configurationMap['handler']['railSpeed'],
            'status': statusMap['started']
            }
        }

        return targets

