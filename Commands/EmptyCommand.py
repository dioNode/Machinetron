from Commands.Command import Command


class EmptyCommand(Command):
    def __init__(self):
        self.name = "Empty"
        self.targetList = {}

    def generateTargets(self, inSteps=False):
        return {}

