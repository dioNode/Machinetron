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
    def __init__(self, cutMachine, heightDisplacement, controller, startSpeed=None, endSpeed=None, home=False, rapid=False):
        super().__init__()
        machineName = cutMachine.name.lower()
        self.name = "Raising "+cutMachine.name
        heightOffset = configurationMap[machineName]['offsets']['cuttingBitHeightOffset']
        heightOffsetFlipped = configurationMap[machineName]['offsets']['cuttingBitHeightOffsetFlipped']
        isFlipped = True if controller.facename == "top" else False
        offset = heightOffsetFlipped if isFlipped else heightOffset
        self.heightDisplacement = heightDisplacement + offset

        self.home = home
        if not isinstance(cutMachine, CutMachine):
            print("RaiseCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine

        # Set speeds
        slowSpeed = configurationMap[cutMachine.name.lower()]['raiseSpeed']
        rapidSpeed = configurationMap[cutMachine.name.lower()]['rapidRaiseSpeed']
        defaultSpeed = rapidSpeed if rapid else slowSpeed
        self.startSpeed = startSpeed if startSpeed is not None else defaultSpeed
        self.endSpeed = endSpeed if endSpeed is not None else self.startSpeed

    def generateTargets(self, inSteps=False):
        targets = {}
        cutMachine = self.cutMachine

        heightDisplacement = self.heightDisplacement
        startSpeed = self.startSpeed
        endSpeed = self.endSpeed

        # Cap variables
        cutMachineName = cutMachine.name.lower()
        heightDisplacement = min(heightDisplacement, configurationMap[cutMachineName]['maxRaise'])
        startSpeed = min(startSpeed, configurationMap[cutMachineName]['maxRaiseSpeed'])
        endSpeed = min(endSpeed, configurationMap[cutMachineName]['maxRaiseSpeed'])

        if inSteps:
            heightDisplacement = cutMachine.vertMotor.displacementToSteps(heightDisplacement)
            startSpeed = cutMachine.vertMotor.displacementToSteps(startSpeed)
            endSpeed = cutMachine.vertMotor.displacementToSteps(endSpeed)

        if self.heightDisplacement == -1:
            # Indicate homing bit
            heightDisplacement = -1

        name = cutMachine.name.lower()
        targets[name] = {'vert': {
            'targetValue': heightDisplacement,
            'startSpeed': startSpeed,
            'endSpeed': endSpeed,
            'status': statusMap['started'],
            'home': self.home
            }
        }

        return targets

