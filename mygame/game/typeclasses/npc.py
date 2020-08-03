"""
NPCs

Non Player Characters (NPCs) are characters that are not pupped by an account.
They run based on preset conditions and respond to external, rather than internal, commands.
"""
##
#  Title: ASSIGNMENT 1
#  Name: Melissa Kimble
#  Date: 02/18/2018
#  Description: NPC, which inherits from the Character class. Defines
##

from random import randint
import random
from characters import Character
from world.rules import check_mood
from world.rules import set_wants


HAPPYSAY = ["Greetings,",
            "It's a beautiful day,",
            "You look well,",
            "Feel free to explore my home,"]
NEUTRALSAY = ["Hello."]
ANGRYSAY = ["Go away,",
            "Why are you here? Go away,",
            "Not interested,",
            "Stop trying,"]
AMBISAY = [".."]

class Npc(Character):
    """
    A NPC typeclass which extends the character class.
    """
    def at_object_creation(self):
        "This is called when object is first created, only."
        self.db.mood = randint(1, 100)
        set_wants(self)
        check_mood(self)

    def at_char_entered(self, character):
        """
         A simple mood check.
         Can be expanded upon later.
        """
        # adapted from https://github.com/evennia/evennia/wiki/Tutorial:--Aggressive-NPCs
        set_wants(self)
        if self.db.is_happy:
            happysay = random.choice(HAPPYSAY)
            self.execute_cmd("say {} {}!".format(happysay,character))
        elif self.db.is_neutral:
            neutralsay = random.choice(NEUTRALSAY)
            self.execute_cmd("say {}.".format(neutralsay))
        elif self.db.is_angry:
            angrysay = random.choice(ANGRYSAY)
            self.execute_cmd("say {} {}.".format(angrysay,character))
        elif self.db.is_ambivalent:
            ambisay = random.choice(AMBISAY)
            self.execute_cmd("say {}.".format(ambisay))

    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        text = super(Character, self).return_appearance(looker)
        mscore = " (Mood: %s)" % self.db.mood
        if "\n" in text:
            # text is multi-line, add score after first line
            first_line, rest = text.split("\n", 1)
            text = first_line + mscore + "\n" + rest
        else:
            # text is only one line; add score to end
            text += mscore
        return text

class Parrot(Character):
    """
    A NPC typeclass which extends the character class.
    """
    # adapted from https://github.com/evennia/evennia/wiki/Tutorial:--NPC's-listening
    def at_heard_say(self, message):
        """
        A simple listener and response. This makes it easy to change for
        subclasses of NPCs reacting differently to says.

        """
        # message will be on the form `<Person> says, "say_text"`
        # we want to get only say_text without the quotes and any spaces
        message = message.split('says, ')[1].strip(' "')

        # we'll make use of this in .msg() below
        return "%s" % (message)

    def msg(self, text=None, from_obj=None, **kwargs):
        "Custom msg() method reacting to say."

        if from_obj != self:
            # make sure to not repeat what we ourselves said or we'll create a loop
            try:
                # if text comes from a say, `text` is `('say_text', {'type': 'say'})`
                say_text, is_say = text[0], text[1]['type'] == 'say'
            except Exception:
                is_say = False
            if is_say:
                # First get the response (if any)
                response = self.at_heard_say(say_text)
                # If there is a response
                if response != None:
                    # speak ourselves, using the return
                    self.execute_cmd("say %s" % response)

        # this is needed if anyone ever puppets this NPC - without it you would never
        # get any feedback from the server (not even the results of look)
        super(Parrot, self).msg(text=text, from_obj=from_obj, **kwargs)