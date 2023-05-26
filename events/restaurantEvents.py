from backbone_classes import *
import copy

"""
Actions Characters Can Take / Events:
Character Arrives in scene
Character leaves the scene
Character A shake hands with Character B
Character A talks to Character B
Character A hits on Character B
Character A Insults Character B
Character A Attacks Character B
Character A Plays a game with Character B
Character A sits down at a table
Character A eats food.
Character A orders food.
Host delivers food to the table. 
Host slips and throws food on Character B
Character A throws drink in Character B’s face
"""

class ArrivesInRestaurant(PlotFragment):
    def __init__(self):
        self.drama = 3

    def checkPreconditions(self, worldstate):
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, []
        valid_characters = []
        environments = []
        for character in worldstate.characters:
                if character.locationoc(character2):
                    valid_characters.append([character, character2])
                    environments.append([])

class CoffeeSpill(PlotFragment):
    def __init__(self):
        self.drama = 3

    def checkPreconditions(self, worldstate):
        if not self.withinRepeatLimit(worldstate, 2):
            return False, None, []
        valid_characters = []
        environments = []
        for character in worldstate.characters:
            for character2 in character.relationships:
                if character.sameLoc(character2):
                    valid_characters.append([character, character2])
                    environments.append([])

        if valid_characters:
            return True, valid_characters, environments
        else:
            return False, None, environments

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event:
            print("{} is walking along with a fresh cup of hydrozine, and loses their footing right as they would pass by {}, spilling their drink all over them! \"Oh goodness, sorry about that!\" says {}.".format(characters[0].name, characters[1].name, characters[0].name))
        char_index = worldstate.characters.index(characters[0])
        char_two_index = worldstate.characters.index(characters[1])
        char = reachable_worldstate.characters[char_index]
        char_two = reachable_worldstate.characters[char_two_index]
        char.updateRelationship(char_two, 3)
        char_two.updateRelationship(char, -5)
        reachable_worldstate.drama_score += self.drama
        return self.updateEventHistory(reachable_worldstate, characters, environment)


class DoNothing(PlotFragment):
    # Purely exists to allow some flexibility in pacing.
    def __init__(self):
        self.drama = 0

    def checkPreconditions(self, worldstate):
        if self.withinRecentHistoryLimit(worldstate, [], [], 3):
            return True, [[]], [[]]
        return False, [[]], [[]]

    def doEvent(self, worldstate, characters, environment, print_event=True):
        reachable_worldstate = copy.deepcopy(worldstate)
        if print_event == True:
            print(".")
        return self.updateEventHistory(reachable_worldstate, characters, environment)