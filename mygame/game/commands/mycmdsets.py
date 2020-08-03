"""
mycmdsets

Sets of commands describe the input the account can do to the game.

"""
##
#  Title: ASSIGNMENT 1
#  Name: Melissa Kimble
#  Date: 02/18/2018
#  Description: Adding commands to objects at their creation. "Treat" commandset can only be used in MoodRoom object.
##

from commands import mycommands
from commands import command

from evennia import CmdSet

class MyCmdSet(CmdSet):
    key = "MyCmdSet"

    def at_cmdset_creation(self):
        self.add(command.CmdEcho())
        self.add(command.CmdSmile())
        self.add(command.CmdCreateNPC())
        self.add(command.CmdEditNPC())
        self.add(command.CmdNPC())

class MoodCmdset(CmdSet):
    """
    This cmdset it used in character generation areas.
    """
    key = "MoodRoom"
    def at_cmdset_creation(self):
        "This is called at initialization"
        self.add(mycommands.CmdTreatNPC())