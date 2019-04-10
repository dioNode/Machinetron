from Commands.Command import Command
from support.supportFunctions import dict_merge

class CombinedCommand(Command):
    def __init__(self, commandList, name=""):
        self.commandList = commandList
        self.name = name
        if self.name == "":
            for command in commandList:
                self.name += command.name + ' | '

    def generateTargets(self):
        targets = {}
        for command in self.commandList:
            dict_merge(targets, command.generateTargets())

        return targets