from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap

from config import configurationMap


class RaiseCommand(Command):
    """Moves the handler to horizontally align your cutting tool to the desired point on the foam.

    Args:
        cutMachine (CutMachine): The cut machine in focus.
        heightDisplacement (double): The vertical displacement for the cutting tool from the bottom of the foam.
        startSpeed (double): Initial speed of push (mm/s).
        endSpeed (double): Final speed of push (mm/s).

    """
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

    def generateTargets(self, inSteps=False):
        targets = {}
        cutMachine = self.cutMachine

        heightDisplacement = self.heightDisplacement
        startSpeed = self.startSpeed
        endSpeed = self.endSpeed

        if inSteps:
            heightDisplacement = cutMachine.vertMotor.displacementToSteps(heightDisplacement)
            startSpeed = cutMachine.vertMotor.displacementToSteps(startSpeed)
            endSpeed = cutMachine.vertMotor.displacementToSteps(endSpeed)

        name = cutMachine.name.lower()
        targets[name] = {'vert': {
            'targetValue': heightDisplacement,
            'startSpeed': startSpeed,
            'endSpeed': endSpeed,
            'status': statusMap['started']
            }
        }

        return targets

