from Commands.Command import Command
from support.supportFunctions import dict_merge


class CombinedCommand(Command):
    """Creates a command that combines all the commands inside commandList.

    The command created will generate a list of targets that corresponds to the targets generated of each of the
    commands in the command list. Note this expects that all commands in the commandList are unique and will override
    each other if otherwise.

    args:
        commandList (array(Command)): A list of commands to be combined.

    """
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