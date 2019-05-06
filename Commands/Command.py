class Command:
    """The command class that keeps track of the details to be passed off to the sub machines.

    """
    def __init__(self):
        self.name = "Unknown Command"
        self.targetList = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def generateTargets(self, inSteps=False):
        """Generates a dictionary of instructions for what the submachine motors should do next.

        These targets hold information about the desired endpoints, starting speeds and ending speeds.

        """
        print("Command: No target")
        return {}

