from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap

from config import configurationMap

class SelectCutmachineCommand(Command):
    def __init__(self, cutMachine):
        super().__init__()
        self.name = "Selecting "+cutMachine.name
        if not isinstance(cutMachine, CutMachine):
            print("SelectCutmachineCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine

    def generateTargets(self):
        targets = {}
        cutMachine = self.cutMachine

        targets['handler'] = {'rail': {
            'targetValue': cutMachine.homeX,
            'startSpeed': configurationMap['handler']['railSpeed'],
            'endSpeed': configurationMap['handler']['railSpeed'],
            'status': statusMap['started']
            }
        }

        return targets

