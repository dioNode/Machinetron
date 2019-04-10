from Commands.Command import Command

class SpinCommand(Command):
    def __init__(self, subMachine, targetValue=None):
        super().__init__()
        self.name = "Spinning "+subMachine.name
        self.targetValue = targetValue
        if not isinstance(subMachine, SubMachine):
            print("SpinCommand: Not a cut machine")
        else:
            self.subMachine = subMachine

    def generateTargets(self):
        targets = {}
        subMachine = self.subMachine
        speed = configurationMap[subMachine.name.lower()]['spinSpeed']

        if self.targetValue != None:
            # Set target value relative to where the current angle is
            currentValue = subMachine.spinMotor.currentDisplacement
            offsetFromZero = currentValue % 360
            zeroValue = currentValue - offsetFromZero
            self.targetValue += zeroValue


        name = subMachine.name.lower()
        targets[name] = {'spin': {
            'targetValue': self.targetValue,
            'startSpeed': speed,
            'endSpeed': speed,
            'status': statusMap['started']
            }
        }

        return targets


from SubMachines.SubMachine import SubMachine
from support.supportMaps import statusMap

from config import configurationMap
