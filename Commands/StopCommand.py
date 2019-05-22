from Commands.Command import Command


class StopCommand(Command):
    def __init__(self):
        self.name = "Stop"
        self.targetList = {}

    def generateTargets(self, inSteps=False):
        return {}