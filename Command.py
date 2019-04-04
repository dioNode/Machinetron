import random

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

    def isComplete(self):
        complete = False
        for submachine, motors in self.targetList:
            for motor, values in motors:
                print(values)
        return complete

