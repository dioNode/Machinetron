from Commands.Command import Command
from SubMachines.CutMachine import CutMachine
from support.supportMaps import statusMap


from config import configurationMap

class PushCommand(Command):
    def __init__(self, cutMachine, depth, faceDepth, fromCenter=False, flipped=False, startSpeed=None, endSpeed=None):
        super().__init__()
        self.name = "Pushing "+cutMachine.name

        self.startSpeed = startSpeed if startSpeed is not None else configurationMap[cutMachine.name.lower()]['pushSpeed']
        self.endSpeed = endSpeed if endSpeed is not None else self.startSpeed

        if depth != 0:
            if flipped:
                offset2Face = configurationMap['offsets']['cuttingBit2HandlerFlipBase'] - faceDepth
                self.depth = depth + offset2Face
            else:
                offset2Face = configurationMap['offsets']['cuttingBit2HandlerCenter'] * 2 - faceDepth
                if not fromCenter:
                    self.depth = depth + offset2Face
                else:
                    self.depth = offset2Face - depth

        else:
            self.depth = 0
        if not isinstance(cutMachine, CutMachine):
            print("PushCommand: Not a cut machine")
        else:
            self.cutMachine = cutMachine


    def generateTargets(self):
        targets = {}
        cutMachine = self.cutMachine

        name = cutMachine.name.lower()
        targets[name] = {'pen': {
            'targetValue': self.depth,
            'startSpeed': self.startSpeed,
            'endSpeed': self.endSpeed,
            'status': statusMap['started']
            }
        }

        return targets

