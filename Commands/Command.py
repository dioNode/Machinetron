class Command:
    def __init__(self):
        self.name = "Unknown Command"
        self.targetList = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def generateTargets(self):
        print("Command: No target")
        return {}

