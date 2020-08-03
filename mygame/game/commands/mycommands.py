"""
mycommands

Commands describe the input the account can do to the game.

"""
##
#  Title: ASSIGNMENT 1
#  Name: Melissa Kimble
#  Date: 02/18/2018
#  Description: The "treat" command and how it affects the NPC's state and what it says in that state.
##

from evennia import Command
from world.rules import check_mood
from world.rules import set_wants
from world.rules import add_mood
import random

## expressions from receiving the correct treat based on current mood state.
CHAPPYTREAT = ["You're the best,",
            "What would I do without",
            "I think I really like ",
            "Amazing,",
            "Perfect,",
            "You know me so well,"]
CNEUTRALTREAT = ["Oh, thanks.",
                 "I guess I needed that.",
                 "Thank you."]
CANGRYTREAT = ["You only got lucky.",
               "Yes. I'll take it.",
               "What took you so long?"]
CAMBITREAT = ["... Thanks ...",
              "... Ok ..."]
## expressions from receiving the wrong treat based on current mood state.
WHAPPYTREAT = ["Um, no thanks.",
               "No, I'm okay.",
               "Great, but I don't need this right now.",
               "I appreciate the effort ... but I really don't need it."]
WNEUTRALTREAT = ["It's like I don't even know you.",
               "It's like you don't even know me.",
               "It's not you, it's me.",
               "This isn't working.",
               "Who are you, again?",
               "Bye."]
WANGRYTREAT = ["Forget it.",
               "Why would you think I want that?",
               "You don't know me at all!",
               "No.",
               "No?",
               "I give up.",
               "I'm fine.",
               "I'm just going to do something else ... without you.",
               "You again!",
               "Bugger off, already!",
               "You're terrible at this."]
WAMBITREAT = ["..."]
WNOTHING = ["No thanks",
            "I don't really want anything right now.",
            "Do I look like I want something?"]

class CmdTreatNPC(Command):
    """
    Treat an NPC with food, a book, or rest. But be careful, if the NPC doesn't want it, they're not going to be happy!

    Usage:
      +treat NPC/food
      +treat NPC/book
      +treat NPC/sleep


    This selects what you would like to treat the NPC with, which affects their current mood. of the current character.
    This can only be used in mood rooms.
    """
    # adapted from: https://github.com/evennia/evennia/wiki/Tutorial-for-basic-MUSH-like-game

    key = "+treat"
    aliases = ["+treat",
               "+treated"]
    help_category = "mush"

    def parse(self):
        "We need to do some parsing here"
        args = self.args
        treatname = None
        if "/" in args:
            args, treatname = [part.strip() for part in args.rsplit("/", 1)]
        # store, so we can access it below in func()
        self.name = args
        self.treatname = treatname
    def func(self):
        "do the editing"
        allowed_treatnames = ("food", "book", "sleep")
        caller = self.caller
        if not self.args or not self.name:
            caller.msg("Usage: +treat name[/treatname]")
            return
        ## sets npc to the npc this command is being used with
        npc = caller.search(self.name)
        npcwants = str(npc.db.npc_wants)
        treatchosen = str(self.treatname)
        if not npc:
            return
        elif self.treatname not in allowed_treatnames:
            caller.msg("You may only treat with %s." %
                       ", ".join(allowed_treatnames))
        elif self.treatname in allowed_treatnames:
            #altering mood based NPC mood and on whether NPC got what they were asking for.
            # caller got the treat correct, positively affects mood
            if npc.db.is_ambivalent and treatchosen == npcwants:
                cambitreat = random.choice(CAMBITREAT)
                npc.execute_cmd("say {}".format(cambitreat))
                moodval = random.randint(0, 5)
                add_mood(npc, moodval)
                check_mood(npc)
                set_wants(npc)
            elif npc.db.is_angry and treatchosen == npcwants:
                cangrytreat = random.choice(CANGRYTREAT)
                npc.execute_cmd("say {}".format(cangrytreat))
                moodval = random.randint(0, 15)
                add_mood(npc, moodval)
                check_mood(npc)
                set_wants(npc)
            elif npc.db.is_neutral and treatchosen == npcwants:
                cneutraltreat = random.choice(CNEUTRALTREAT)
                npc.execute_cmd("say {}".format(cneutraltreat))
                moodval = random.randint(1, 10)
                add_mood(npc, moodval)
                check_mood(npc)
                set_wants(npc)
            elif npc.db.is_happy and treatchosen == npcwants:
                chappytreat = random.choice(CHAPPYTREAT)
                npc.execute_cmd("say {} {}!".format(chappytreat, caller))
                moodval = random.randint(1, 5)
                add_mood(npc, moodval)
                check_mood(npc)
                set_wants(npc)
            # caller got the treat wrong, negatively affects mood
            elif npc.db.is_ambivalent and treatchosen != npcwants and npcwants != "nothing":
                wambitreat = random.choice(WAMBITREAT)
                npc.execute_cmd("say {}".format(wambitreat))
                moodval = random.randint(-5, -1)
                add_mood(npc, moodval)
                check_mood(npc)
            elif npc.db.is_angry and treatchosen != npcwants and npcwants != "nothing":
                wangrytreat = random.choice(WANGRYTREAT)
                npc.execute_cmd("say {}".format(wangrytreat))
                moodval = random.randint(-15, -1)
                add_mood(npc, moodval)
                check_mood(npc)
            elif npc.db.is_neutral and treatchosen != npcwants and npcwants != "nothing":
                wneutraltreat = random.choice(WNEUTRALTREAT)
                npc.execute_cmd("say {}".format(wneutraltreat))
                moodval = random.randint(-10, 0)
                add_mood(npc, moodval)
                check_mood(npc)
            elif npc.db.is_happy and treatchosen != npcwants and npcwants != "nothing":
                whappytreat = random.choice(WHAPPYTREAT)
                npc.execute_cmd("say {}".format(whappytreat))
                moodval = random.randint(-5, 0)
                add_mood(npc, moodval)
                check_mood(npc)
            elif npcwants == "nothing":
                wnothing = random.choice(WNOTHING)
                npc.execute_cmd("say {}".format(wnothing))
                moodval = random.randint(-10, -5)
                add_mood(npc, moodval)
                check_mood(npc)