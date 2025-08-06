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
# You can take a peak at Types.py for more information but,
    # LocData is code, region in this instance
    # Regions will be explained more in Regions.py
    # But just know that it's mostly about organization
    # Place locations together based on where they are in the game and what is needed to get there
glyphs_locations = {
    # Region 1
    "Sword Pedestal":                       LocData(1,  "Region 1"),
    "Defeat Runic Construct":               LocData(2,  "Region 1"),        # event location
    "Runic Construct Reward":               LocData(3,  "Region 1"),
    "Stalker Sigil 1":                      LocData(4,  "Region 1"),        # event location
    "Map Pedestal":                         LocData(5,  "Region 1"),
    "Silver Shard Puzzle 1":                LocData(6,  "Region 1"),
    "Silver Shard Puzzle 2":                LocData(7,  "Region 1"),
    "Silver Shard Puzzle 3":                LocData(8,  "Region 1"),
    "Smile Token Puzzle 3":                 LocData(9,  "Region 1"),
    "Smile Token Puzzle 9":                 LocData(10,  "Region 1"),
    "Master Puzzle 2":                      LocData(11, "Region 1"),
    "Color Cypher Room Pickup":             LocData(12, "Region 1"),

    # Region 2
    "Serpent Lock 1":                       LocData(13, "Region 2"),        # event location
    "Serpent Lock 2":                       LocData(14, "Region 2"),        # event location
    "Serpent Lock 3":                       LocData(15, "Region 2"),        # event location
    "Silver Shard Puzzle 4":                LocData(16, "Region 2"),
    "Silver Shard Puzzle 5":                LocData(17, "Region 2"),
    "Silver Shard Puzzle 6":                LocData(18, "Region 2"),
    "Silver Shard Puzzle 7":                LocData(19, "Region 2"),
    "Silver Shard Puzzle 8":                LocData(20, "Region 2"),
    "Silver Shard Puzzle 9":                LocData(21, "Region 2"),
    "Silver Shard Puzzle 15":               LocData(22, "Region 2"),
    "Smile Token Puzzle 1":                 LocData(23, "Region 2"),
    "Smile Token Puzzle 6":                 LocData(24, "Region 2"),
    "Smile Token Puzzle 8":                 LocData(25, "Region 2"),
    "Smile Token Puzzle 10":                LocData(26, "Region 2"),
    "Master Puzzle 1":                      LocData(27, "Region 2"),
    "Defeat Gilded Serpent":                LocData(28, "Region 2"),        # event location
    "Gilded Serpent Reward":                LocData(29, "Region 2"),
    "Stalker Sigil 2":                      LocData(30, "Region 2"),        # event location
    "Stalker Sigil 3":                      LocData(31, "Region 2"),        # event location
    "Shadow Chase Reward":                  LocData(32, "Region 2"),
    "Water Room Pickup":                    LocData(33, "Region 2"),
    "Cameo Room Pickup":                    LocData(34, "Region 2"),
    "George Reward":                        LocData(35, "Region 2"),
    "Car Hall Pickup":                      LocData(36, "Region 2"),
    "Sector 1 Below Serpent Lock  Pickup":  LocData(37, "Region 2"),
    "Collapsed Tunnel Pickup":              LocData(38, "Region 2"),
    "Shadow Chase Pickup":                  LocData(39, "Region 2"),
    "Nest Room Pickup":                     LocData(40, "Region 2"),
    "Serpent Boss Room Pickup":             LocData(41, "Region 2"),

    # Region 3
    "Green Stone Trial":                    LocData(42, "Region 3"),
    "Blue Stone Trial":                     LocData(43, "Region 3"),
    "Red Stone Trial":                      LocData(44, "Region 3"),
    "Silver Shard Puzzle 10":               LocData(45, "Region 3"),
    "Silver Shard Puzzle 11":               LocData(46, "Region 3"),
    "Silver Shard Puzzle 12":               LocData(47, "Region 3"),
    "Silver Shard Puzzle 13":               LocData(48, "Region 3"),
    "Silver Shard Puzzle 14":               LocData(49, "Region 3"),
    "Smile Token Puzzle 2":                 LocData(50, "Region 3"),
    "Smile Token Puzzle 7":                 LocData(51, "Region 3"),
    "Master Puzzle 3":                      LocData(52, "Region 3"),
    "Collapse Unlock":                      LocData(53, "Region 3"),        # event location
    "Sector 2 Below Serpent Lock Pickup":   LocData(54, "Region 3"),

    # Region 4
    "Defeat Spearman":                      LocData(55, "Region 4"),        # event location
    "Spearman Reward":                      LocData(56, "Region 4"),
    "Multiparry Gold Shard Puzzle":         LocData(57, "Region 4"),
    "Platforming Gold Shard Room":          LocData(58, "Region 4"),
    "Flower Puzzle Reward":                 LocData(59, "Region 4"),
    "Smile Token Puzzle 4":                 LocData(60, "Region 4"),
    "Smile Token Puzzle 5":                 LocData(61, "Region 4"),
    "On top of the Rosetta Stone":          LocData(62, "Region 4"),
    "Long Parry Platforming Room Pickup":   LocData(63, "Region 4"),
    "Defeat Wraith":                        LocData(64, "Region 4"),        # event location
    "Defeat Vessel":                        LocData(65, "Region 4"),        # event location

    # Collapse
    "Escape Normal Sequence Pickup":        LocData(66, "Collapse"),
    "False Ending":                         LocData(67, "Collapse"),        # event location

    # Smile Shop
    "Smile Shop Item 1":                    LocData(68, "Smile Shop"),
    "Smile Shop Item 2":                    LocData(69, "Smile Shop"),
    "Smile Shop Item 3":                    LocData(70, "Smile Shop"),
    "Smile Shop Item 4":                    LocData(71, "Smile Shop"),
    "Dash Puzzle Reward":                   LocData(72, "Smile Shop"),
    "Respawn Reward":                       LocData(73, "Smile Shop"),
    "Smilemask Ending":                     LocData(74, "Smile Shop"),      # event location

    # Dark Region
    "Defeat Null":                          LocData(75, "Dark Region"),     # event location
    "Clarity":                              LocData(76, "Dark Region"),     # event location
    "Secret Room Pickup":                   LocData(77, "Dark Region"),
    "Large Room Pickup in the Corner":      LocData(78, "Dark Region"),
    
    # Act 1
    "Void Gate Shard Location 1":           LocData(79, "Act 1"),
    "Void Gate Shard Location 2":           LocData(80, "Act 1"),
    "Void Gate Shard Location 3":           LocData(81, "Act 1"),
    "Void Gate Shard Location 4":           LocData(82, "Act 1"),
    "Void Gate Shard Location 5":           LocData(83, "Act 1"),
    "Void Gate Shard Location 6":           LocData(84, "Act 1"),
    "Void Gate Shard Location 7":           LocData(85, "Act 1"),
    "John Room Pickup":                     LocData(86, "Act 1"),
    "Omnipotence Ending":                   LocData(87, "Act 1"),           # event location
    "Clear Act 1":                          LocData(88, "Act 1"),           # event location

    # Act 2
    "Boss Rush Heal 1":                     LocData(89, "Act 2"),
    "Boss Rush Heal 2":                     LocData(90, "Act 2"),
    "Boss Rush Heal 3":                     LocData(91, "Act 2"),
    "Boss Rush Heal 4":                     LocData(92, "Act 2"),
    "Pink Bow Pickup":                      LocData(93, "Act 2"),
    "Clear Act 2":                          LocData(94, "Act 2"),           # event location

    # Act 3
    "Defeat Wraith Prime":                  LocData(95, "Act 3"),           # event location

    # Epilogue
    "Clear Epilogue":                       LocData(96, "Epilogue"),        # event location
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