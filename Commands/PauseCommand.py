from Commands.Command import Command


class PauseCommand(Command):
    def __init__(self):
        self.name = "Pause"
        self.targetList = {}

    def generateTargets(self, inSteps=False):
        return {}

