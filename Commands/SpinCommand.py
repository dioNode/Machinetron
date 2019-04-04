from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap

from config import configurationMap

class SpinCommand(Command):
    def __init__(self, cutMachine):
        super().__init__()
        self.name = "Spinning "+cutMachine.name
        if not isinstance(cutMachine, CutMachine):
            print("SpinCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine

    def generateTargets(self):
        targets = {}
        cutMachine = self.cutMachine
        speed = configurationMap['cutMachine']['spinSpeed']

        name = cutMachine.name.lower()
        targets[name] = {'spin': {
            'targetValue': None,
            'startSpeed': speed,
            'endSpeed': speed,
            'status': statusMap['started']
            }
        }

        return targets

