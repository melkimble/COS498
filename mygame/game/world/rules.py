"""
rules

System rules that characters must obey. These rules alter character environments related to the Mood attribute.
"""
##
#  Title: ASSIGNMENT 1
#  Name: Melissa Kimble
#  Date: 02/18/2018
#  Description: Rules that define an NPC's "states" - happy, neutral, angry, or ambivalent.
##

import random

CHOICES = ["food",
           "book",
           "sleep",
           "nothing"]
def set_wants(character):
    npcwants = random.choice(CHOICES)
    character.db.npc_wants = npcwants

def check_mood(character):
    "Checks if a Character is 'angry, neutral, mad, or ambivalent'."
    if character.db.mood >= 0 and character.db.mood <= 25:
        character.db.is_ambivalent = True
        character.db.is_angry = False
        character.db.is_neutral = False
        character.db.is_happy = False
    elif character.db.mood > 25 and character.db.mood <= 50:
        character.db.is_angry = True
        character.db.is_ambivalent = False
        character.db.is_neutral = False
        character.db.is_happy = False
    elif character.db.mood > 50 and character.db.mood <= 75:
        character.db.is_neutral = True
        character.db.is_angry = False
        character.db.is_ambivalent = False
        character.db.is_happy = False
    elif character.db.mood > 75 and character.db.mood <= 100:
        character.db.is_happy = True
        character.db.is_neutral = False
        character.db.is_angry = False
        character.db.is_ambivalent = False
#        character.db.HP = 100  # reset

def add_mood(character, amount):
    "Add mood to character."
    character.db.mood += amount
    if character.db.mood > 100:
        character.db.mood = 100
    elif character.db.mood < 0:
        character.db.mood = 0