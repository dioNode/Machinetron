from Commands.Command import Command
from Commands.CombinedCommand import CombinedCommand
from support.supportFunctions import dict_merge


class SequentialCommand(Command):
    """Creates a command that combines all the commands inside commandList and runs them one after another.

    The command created will generate a list of targets that corresponds to the targets generated of each of the
    commands in the command list.

    args:
        commandList (array(Command)): A list of commands to be combined.

    """
    def __init__(self, commandList, name=""):
        self.commandList = commandList
        self.name = name
        if self.name == "":
            self.name = "Sequential Command"

    def generateTargets(self, inSteps=False):
        targets = []
        for command in self.commandList:
            targets.append(command.generateTargets(inSteps))

        return targets

    def addCommand(self, command):
        self.commandList.append(command)

