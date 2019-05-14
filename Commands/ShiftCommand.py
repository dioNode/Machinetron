from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap
from config import configurationMap


class ShiftCommand(Command):
    """Moves the handler to horizontally align your cutting tool to the desired point on the foam.

    Args:
        cutMachine (CutMachine): The cut machine in focus.
        horizontalDisplacement (double): The horizontal displacement for the cutting tool from the center of the foam.
        startSpeed (double): Initial speed of push (mm/s).
        endSpeed (double): Final speed of push (mm/s).

    """
    def __init__(self, cutMachine, handler, horizontalDisplacement, startSpeed=None, endSpeed=None):
        super().__init__()
        self.name = "Shifting "+cutMachine.name
        self.horizontalDisplacement = horizontalDisplacement
        if not isinstance(cutMachine, CutMachine):
            print("ShiftCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine
            self.handler = handler

        # Set speeds
        self.startSpeed = startSpeed if startSpeed is not None else configurationMap['handler']['railSpeed']
        self.endSpeed = endSpeed if endSpeed is not None else self.startSpeed

    def generateTargets(self, inSteps=False):
        targets = {}
        cutMachine = self.cutMachine
        handler = self.handler
        globalTargetX = self.horizontalDisplacement + cutMachine.homeX
        startSpeed = self.startSpeed
        endSpeed = self.endSpeed

        # Cap variables
        globalTargetX = min(globalTargetX, configurationMap['handler']['maxRail'])
        startSpeed = min(startSpeed, configurationMap['handler']['maxRailSpeed'])
        endSpeed = min(endSpeed, configurationMap['handler']['maxRailSpeed'])

        if inSteps:
            globalTargetX = handler.railMotor.displacementToSteps(globalTargetX)
            startSpeed = handler.railMotor.displacementToSteps(startSpeed)
            endSpeed = handler.railMotor.displacementToSteps(endSpeed)

        targets['handler'] = {'rail': {
            'targetValue': globalTargetX,
            'startSpeed': startSpeed,
            'endSpeed': endSpeed,
            'status': statusMap['started']
            }
        }

        return targets

