"""
Room

Rooms are simple containers that has no location of their own.

"""
##
#  Title: ASSIGNMENT 1
#  Name: Melissa Kimble
#  Date: 02/18/2018
#  Description: Room "objects", and how they behave based on types of rooms.
##

from evennia import DefaultRoom

from evennia import utils
from characters import Character
from npc import Npc
from commands.mycmdsets import MoodCmdset


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    ## example from https://github.com/evennia/evennia/wiki/Tutorial:--Aggressive-NPCs
    def at_object_receive(self, obj, source_location):
        if utils.inherits_from(obj, Npc): # An NPC has entered
            pass
        else:
            if utils.inherits_from(obj, Character):
                # A PC has entered, NPC is caught above.
                # Cause the character to look around
                obj.execute_cmd('look')
                for item in self.contents:
                    if utils.inherits_from(item, Npc):
                        # An NPC is in the room
                        item.at_char_entered(obj)
    pass

class MoodRoom(Room):
    """
    This room class is used by mood altering rooms. It makes
    the MoodCmdset available.
    """
    def at_object_creation(self):
        "this is called only at first creation"
        self.cmdset.add(MoodCmdset, permanent=True)