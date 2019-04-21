from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap

from config import configurationMap


class SelectCutmachineCommand(Command):
    """Moves the handler towards the desired cutting machine.

    Args:
        cutMachine (CutMachine): The desired cutting machine to operate with.

    """
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

