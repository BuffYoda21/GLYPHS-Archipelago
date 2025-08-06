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
    "Runic Construct Reward":               LocData(2,  "Region 1"),
    "Map Pedestal":                         LocData(3,  "Region 1"),
    "Silver Shard Puzzle 1":                LocData(4,  "Region 1"),
    "Silver Shard Puzzle 2":                LocData(5,  "Region 1"),
    "Silver Shard Puzzle 3":                LocData(6,  "Region 1"),
    "Smile Token Puzzle 3":                 LocData(7,  "Region 1"),
    "Smile Token Puzzle 9":                 LocData(8,  "Region 1"),
    "Master Puzzle 2":                      LocData(9,  "Region 1"),
    "Color Cypher Room Pickup":             LocData(10, "Region 1"),

    # Region 2
    "Silver Shard Puzzle 4":                LocData(11, "Region 2"),
    "Silver Shard Puzzle 5":                LocData(12, "Region 2"),
    "Silver Shard Puzzle 6":                LocData(13, "Region 2"),
    "Silver Shard Puzzle 7":                LocData(14, "Region 2"),
    "Silver Shard Puzzle 8":                LocData(15, "Region 2"),
    "Silver Shard Puzzle 9":                LocData(16, "Region 2"),
    "Silver Shard Puzzle 15":               LocData(17, "Region 2"),
    "Smile Token Puzzle 1":                 LocData(18, "Region 2"),
    "Smile Token Puzzle 6":                 LocData(19, "Region 2"),
    "Smile Token Puzzle 8":                 LocData(20, "Region 2"),
    "Smile Token Puzzle 10":                LocData(21, "Region 2"),
    "Master Puzzle 1":                      LocData(22, "Region 2"),
    "Gilded Serpent Reward":                LocData(23, "Region 2"),
    "Shadow Chase Reward":                  LocData(24, "Region 2"),
    "Water Room Pickup":                    LocData(25, "Region 2"),
    "Cameo Room Pickup":                    LocData(26, "Region 2"),
    "George Reward":                        LocData(27, "Region 2"),
    "Car Hall Pickup":                      LocData(28, "Region 2"),
    "Sector 1 Below Serpent Lock  Pickup":  LocData(29, "Region 2"),
    "Collapsed Tunnel Pickup":              LocData(30, "Region 2"),
    "Shadow Chase Pickup":                  LocData(31, "Region 2"),
    "Nest Room Pickup":                     LocData(32, "Region 2"),
    "Serpent Boss Room Pickup":             LocData(33, "Region 2"),

    # Region 3
    "Green Stone Trial":                    LocData(34, "Region 3"),
    "Blue Stone Trial":                     LocData(35, "Region 3"),
    "Red Stone Trial":                      LocData(36, "Region 3"),
    "Silver Shard Puzzle 10":               LocData(37, "Region 3"),
    "Silver Shard Puzzle 11":               LocData(38, "Region 3"),
    "Silver Shard Puzzle 12":               LocData(39, "Region 3"),
    "Silver Shard Puzzle 13":               LocData(40, "Region 3"),
    "Silver Shard Puzzle 14":               LocData(41, "Region 3"),
    "Smile Token Puzzle 2":                 LocData(42, "Region 3"),
    "Smile Token Puzzle 7":                 LocData(43, "Region 3"),
    "Master Puzzle 3":                      LocData(44, "Region 3"),
    "Sector 2 Below Serpent Lock Pickup":   LocData(45, "Region 3"),

    # Region 4
    "Spearman Reward":                      LocData(46, "Region 4"),
    "Multiparry Gold Shard Puzzle":         LocData(47, "Region 4"),
    "Platforming Gold Shard Room":          LocData(48, "Region 4"),
    "Flower Puzzle Reward":                 LocData(49, "Region 4"),
    "Smile Token Puzzle 4":                 LocData(50, "Region 4"),
    "Smile Token Puzzle 5":                 LocData(51, "Region 4"),
    "On top of the Rosetta Stone":          LocData(52, "Region 4"),
    "Long Parry Platforming Room Pickup":   LocData(53, "Region 4"),

    # Collapse
    "Escape Normal Sequence Pickup":        LocData(54, "Collapse"),

    # Smile Shop
    "Smile Shop Item 1":                    LocData(55, "Smile Shop"),
    "Smile Shop Item 2":                    LocData(56, "Smile Shop"),
    "Smile Shop Item 3":                    LocData(57, "Smile Shop"),
    "Smile Shop Item 4":                    LocData(58, "Smile Shop"),
    "Dash Puzzle Reward":                   LocData(59, "Smile Shop"),
    "Respawn Reward":                       LocData(60, "Smile Shop"),

    # Dark Region
    "Secret Room Pickup":                   LocData(61, "Dark Region"),
    "Large Room Pickup in the Corner":      LocData(62, "Dark Region"),
    
    # Act 1
    "Void Gate Shard Location 1":           LocData(63, "Act 1"),
    "Void Gate Shard Location 2":           LocData(64, "Act 1"),
    "Void Gate Shard Location 3":           LocData(65, "Act 1"),
    "Void Gate Shard Location 4":           LocData(66, "Act 1"),
    "Void Gate Shard Location 5":           LocData(67, "Act 1"),
    "Void Gate Shard Location 6":           LocData(68, "Act 1"),
    "Void Gate Shard Location 7":           LocData(69, "Act 1"),
    "John Room Pickup":                     LocData(70, "Act 1"),
    
    # Act 2
    "Boss Rush Heal 1":                     LocData(71, "Act 2"),
    "Boss Rush Heal 2":                     LocData(72, "Act 2"),
    "Boss Rush Heal 3":                     LocData(73, "Act 2"),
    "Boss Rush Heal 4":                     LocData(74, "Act 2"),
    "Pink Bow Pickup":                      LocData(75, "Act 2"),
}

extra_locations = {
    "ml7's house": LocData(20050102, "Sibiu"),
}

# Like in Items.py, breaking up the different locations to help with organization and if something special needs to happen to them
event_locations = {
    "Defeat Runic Construct":               LocData(76,  "Region 1"),
    "Stalker Sigil 1":                      LocData(77,  "Region 1"),
    "Serpent Lock 1":                       LocData(78, "Region 2"),
    "Serpent Lock 2":                       LocData(79, "Region 2"),
    "Serpent Lock 3":                       LocData(80, "Region 2"),
    "Defeat Gilded Serpent":                LocData(81, "Region 2"),
    "Stalker Sigil 2":                      LocData(82, "Region 2"),
    "Stalker Sigil 3":                      LocData(83, "Region 2"),
    "Solve Flower Puzzle":                  LocData(84, "Region 2"),
    "Collapse Unlock":                      LocData(85, "Region 3"),
    "Defeat Spearman":                      LocData(86, "Region 4"),
    "Defeat Wraith":                        LocData(87, "Region 4"),
    "Defeat Vessel":                        LocData(88, "Region 4"),
    "False Ending":                         LocData(89, "Collapse"),
    "Smilemask Ending":                     LocData(90, "Smile Shop"),
    "Defeat Null":                          LocData(91, "Dark Region"),
    "Clarity":                              LocData(92, "Dark Region"),
    "Omnipotence Ending":                   LocData(93, "Act 1"),
    "Clear Act 1":                          LocData(94, "Act 1"),
    "Clear Act 2":                          LocData(95, "Act 2"),
    "Defeat Wraith Prime":                  LocData(96, "Act 3"),
    "Clear Epilogue":                       LocData(97, "Epilogue"),
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