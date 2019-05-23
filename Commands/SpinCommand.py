from Commands.Command import Command
from config import configurationMap


class SpinCommand(Command):
    """Moves the handler to horizontally align your cutting tool to the desired point on the foam.

    Args:
        subMachine (SubMachine): The sub machine in focus.
        targetValue (double): The number of degrees to be spun relative to the current nearest zero point.
        startSpeed (double): Initial speed of push (mm/s).
        endSpeed (double): Final speed of push (mm/s).

    """
    def __init__(self, subMachine, targetValue=None, startSpeed=None, endSpeed=None, home=False, rapid=False):
        super().__init__()
        self.name = "Spinning "+subMachine.name
        self.targetValue = targetValue % 360
        self.home = home
        if not isinstance(subMachine, SubMachine):
            print("SpinCommand: Not a cut machine")
        else:
            self.subMachine = subMachine

        # Set speeds
        slowSpeed = configurationMap[subMachine.name.lower()]['spinSpeed']
        rapidSpeed = configurationMap[subMachine.name.lower()]['rapidSpinSpeed']
        defaultSpeed = rapidSpeed if rapid else slowSpeed
        self.startSpeed = startSpeed if startSpeed is not None else defaultSpeed
        self.endSpeed = endSpeed if endSpeed is not None else self.startSpeed

    def generateTargets(self, inSteps=False):
        targets = {}
        subMachine = self.subMachine

        targetValue = self.targetValue
        startSpeed = self.startSpeed
        endSpeed = self.endSpeed

        if inSteps:
            if targetValue is None:
                targetValue = configurationMap['other']['infVal']
            else:
                targetValue = subMachine.spinMotor.displacementToSteps(targetValue)
            startSpeed = subMachine.spinMotor.displacementToSteps(startSpeed)
            endSpeed = subMachine.spinMotor.displacementToSteps(endSpeed)

        name = subMachine.name.lower()
        targets[name] = {'spin': {
            'targetValue': targetValue,
            'startSpeed': startSpeed,
            'endSpeed': endSpeed,
            'status': statusMap['started'],
            'home': self.home,
            }
        }

        return targets


from SubMachines.SubMachine import SubMachine
from support.supportMaps import statusMap

from config import configurationMap
