import random

class Command:
    def __init__(self, command):
        x = lambda a: a+10
        self.action = x
        self.command = command

    def __str__(self):
        return "Command["+self.command+"]"

    def __repr__(self):
        return str(self)

    def isComplete(self):
        return True if round(random.random()) == 1 else False