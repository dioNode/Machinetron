from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap

from config import configurationMap


class PushCommand(Command):
    """This command pushes the cutMachine towards the foam.

    Args:
        cutMachine (CutMachine): The cut machine in focus.
        depth (double): Depth of cut machine betting pushed into the initial face surface.
        faceDepth (double): Current depth of the foam relative to the current face.
        fromCenter (boolean): Whether the depth variable is defined from the center.
        flipped (boolean): Whether the foam block is currently flipped.
        startSpeed (double): Initial speed of push (mm/s).
        endSpeed (double): Final speed of push (mm/s).

    """
    def __init__(self, cutMachine, depth, faceDepth, fromCenter=False, flipped=False, startSpeed=None, endSpeed=None,
                 home=False):
        super().__init__()
        self.name = "Pushing "+cutMachine.name

        self.startSpeed = startSpeed if startSpeed is not None else configurationMap[cutMachine.name.lower()]['pushSpeed']
        self.endSpeed = endSpeed if endSpeed is not None else self.startSpeed

        self.home = home

        if flipped:
            offset2Face = configurationMap['offsets']['cuttingBit2HandlerFlipBase'] - faceDepth
            self.depth = depth + offset2Face
        else:
            offset2Face = configurationMap['offsets']['cuttingBit2HandlerCenter'] * 2 - faceDepth
            if not fromCenter:
                self.depth = depth + offset2Face
            else:
                self.depth = offset2Face + configurationMap['offsets']['cuttingBit2HandlerCenter'] - depth

        if not isinstance(cutMachine, CutMachine):
            print("PushCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine


    def generateTargets(self, inSteps=False):
        targets = {}
        cutMachine = self.cutMachine

        depth = self.depth
        startSpeed = self.startSpeed
        endSpeed = self.endSpeed

        # Cap variables
        cutMachineName = cutMachine.name.lower()
        depth = min(depth, configurationMap[cutMachineName]['maxPush'])
        depth = max(0, depth)
        startSpeed = min(startSpeed, configurationMap[cutMachineName]['maxPushSpeed'])
        endSpeed = min(endSpeed, configurationMap[cutMachineName]['maxPushSpeed'])

        if inSteps:
            depth = cutMachine.penMotor.displacementToSteps(depth)
            startSpeed = cutMachine.penMotor.displacementToSteps(startSpeed)
            endSpeed = cutMachine.penMotor.displacementToSteps(endSpeed)

        name = cutMachine.name.lower()
        targets[name] = {'pen': {
            'targetValue': depth if not self.home else configurationMap['other']['homeVal'],
            'startSpeed': startSpeed,
            'endSpeed': endSpeed,
            'status': statusMap['started']
            }
        }

        return targets

