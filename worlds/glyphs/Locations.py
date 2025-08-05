# Look at init or Items.py for more information on imports
from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData

if TYPE_CHECKING:
    from . import GlyphsWorld

# This is technique in programming to make things more readable for booleans
# A boolean is true or false
def did_include_extra_locations(world: "GlyphsWorld") -> bool:
    return bool(world.options.ExtraLocations)

# This is used by ap and in Items.py
# Theres a multitude of reasons to need to grab how many locations there are
def get_total_locations(world: "GlyphsWorld") -> int:
    # This is the total that we'll keep updating as we count how many locations there are
    total = 0
    for name in location_table:
        # If we did not turn on extra locations (see how readable it is with that thing from the top)
        # AND the name of it is found in our extra locations table, then that means we dont want to count it
        # So continue moves onto the next name in the table
        if not did_include_extra_locations(world) and name in extra_locations:
            continue

        # If the location is valid though, count it
        if is_valid_location(world, name):
            total += 1

    return total

def get_location_names() -> Dict[str, int]:
    # This is just a fancy way of getting all the names and data in the location table and making a dictionary thats {name, code}
    # If you have dynamic locations then you want to add them to the dictionary as well
    names = {name: data.ap_code for name, data in location_table.items()}

    return names

# The check to make sure the location is valid
# I know it looks like the same as when we counted it but thats because this is an example
# Things get complicated fast so having a back up is nice
def is_valid_location(world: "GlyphsWorld", name) -> bool:
    if not did_include_extra_locations(world) and name in extra_locations:
        return False
    
    return True

# You might need more functions as well so be liberal with them
# My advice, if you are about to type the same thing in a second time, turn it into a function
# Even if you only do it once you can turn it into a function too for organization

# Heres where you do the next fun part of listing out all those locations
# Its a lot
# My advice, zone out for half an hour listening to music and hope you wake up to a completed list
glyphs_locations = {
    # You can take a peak at Types.py for more information but,
    # LocData is code, region in this instance
    # Regions will be explained more in Regions.py
    # But just know that it's mostly about organization
    # Place locations together based on where they are in the game and what is needed to get there
    "Sword Pedestal":           LocData(1,  "Region 1"),
    "Defeat Runic Construct":   LocData(2,  "Region 1"),        # event location
    "Dash Orb Pickup":          LocData(3,  "Region 1"),
    "Map Pedestal":             LocData(4,  "Region 1"),
    "Silver Shard Puzzle 1":    LocData(5,  "Region 1"),
    "Silver Shard Puzzle 2":    LocData(6,  "Region 1"),
    "Silver Shard Puzzle 3":    LocData(7,  "Region 1"),
    "Smile Token Puzzle 3":     LocData(8,  "Region 1"),
    "Smile Token Puzzle 9":     LocData(9,  "Region 1"),
    "Master Puzzle 2":          LocData(10, "Region 1"),
    "False Ending":             LocData(11, "Region 1"),        # goal location
    "Serpent Lock 1":           LocData(12, "Region 2"),        # event location
    "Serpent Lock 2":           LocData(13, "Region 2"),        # event location
    "Serpent Lock 3":           LocData(14, "Region 2"),        # event location
    "Silver Shard Puzzle 4":    LocData(15, "Region 2"),
    "Silver Shard Puzzle 5":    LocData(16, "Region 2"),
    "Silver Shard Puzzle 6":    LocData(17, "Region 2"),
    "Silver Shard Puzzle 7":    LocData(18, "Region 2"),
    "Silver Shard Puzzle 8":    LocData(19, "Region 2"),
    "Silver Shard Puzzle 9":    LocData(20, "Region 2"),
    "Silver Shard Puzzle 15":   LocData(21, "Region 2"),
    "Smile Token Puzzle 1":     LocData(22, "Region 2"),
    "Smile Token Puzzle 6":     LocData(23, "Region 2"),
    "Smile Token Puzzle 10":    LocData(24, "Region 2"),
    "Master Puzzle 1":          LocData(25, "Region 2"),
    "Defeat Gilded Serpent":    LocData(26, "Region 2"),        # event location
    "Grapple Pickup":           LocData(27, "Region 2"),
    "Green Stone Trial":        LocData(28, "Region 3"),
    "Blue Stone Trial":         LocData(29, "Region 3"),
    "Red Stone Trial":          LocData(30, "Region 3"),
    "Silver Shard Puzzle 10":   LocData(31, "Region 3"),
    "Silver Shard Puzzle 11":   LocData(32, "Region 3"),
    "Silver Shard Puzzle 12":   LocData(33, "Region 3"),
    "Silver Shard Puzzle 13":   LocData(34, "Region 3"),
    "Silver Shard Puzzle 14":   LocData(35, "Region 3"),
    "Smile Token Puzzle 2":     LocData(36, "Region 3"),
    "Smile Token Puzzle 7":     LocData(37, "Region 3"),
    "Master Puzzle 3":          LocData(38, "Region 3"),
    "Collapse Unlock":          LocData(39, "Region 3"),        # event location
}

extra_locations = {
    "ml7's house": LocData(20050102, "Sibiu"),
}

# Like in Items.py, breaking up the different locations to help with organization and if something special needs to happen to them
event_locations = {
    "Beat Final Boss": LocData(20050110, "Big Hole in the Floor")
}

# Also like in Items.py, this collects all the dictionaries together
# Its important to note that locations MUST be bigger than progressive item count and should be bigger than total item count
# Its not here because this is an example and im not funny enough to think of more locations
# But important to note
location_table = {
    **glyphs_locations,
    **extra_locations,
    **event_locations
}