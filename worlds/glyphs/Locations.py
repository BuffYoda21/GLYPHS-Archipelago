# Look at init or Items.py for more information on imports
from enum import IntEnum
from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData
from .Options import LocationPool

if TYPE_CHECKING:
    from . import GlyphsWorld

class LocationPoolType(IntEnum):
    FalseEnding = 1
    GoodEnding = 2
    FullTomb = 3
    OuterVoid = 4

def location_pool_type(world: "GlyphsWorld") -> LocationPoolType:
    if world.options.LocationPool == LocationPoolType.FalseEnding:
        return LocationPoolType.FalseEnding
    elif world.options.LocationPool == LocationPoolType.GoodEnding:
        return LocationPoolType.GoodEnding
    elif world.options.LocationPool == LocationPoolType.FullTomb:
        return LocationPoolType.FullTomb
    elif world.options.LocationPool == LocationPoolType.OuterVoid:
        return LocationPoolType.OuterVoid
    return LocationPoolType.FalseEnding

# This is used by ap and in Items.py
# Theres a multitude of reasons to need to grab how many locations there are
def get_total_locations(world: "GlyphsWorld") -> int:
    # This is the total that we'll keep updating as we count how many locations there are
    total = 0
    for name in location_table:
        # If we did not turn on extra locations (see how readable it is with that thing from the top)
        # AND the name of it is found in our extra locations table, then that means we dont want to count it
        # So continue moves onto the next name in the table
        if not location_pool_type == LocationPoolType.FalseEnding(world) and not name in glyphs_false_ending_locations:
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
    if not location_pool_type == LocationPoolType.FalseEnding(world) and not name in glyphs_false_ending_locations:
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

glyphs_false_ending_locations = {
    # Region 1
    "Sword Pedestal":                       LocData(1,  "Region 1 - Central"),
    "Runic Construct Reward":               LocData(2,  "Region 1 - Central"),
    "Map Pedestal":                         LocData(3,  "Region 1 - Left"),
    "Silver Shard Puzzle 1":                LocData(4,  "Region 1 - Left"),
    "Silver Shard Puzzle 2":                LocData(5,  "Region 1 - Upper Right"),
    "Silver Shard Puzzle 3":                LocData(6,  "Region 1 - Upper Right"),
    "Smile Token Puzzle 3":                 LocData(7,  "Region 1 - Central"),
    "Smile Token Puzzle 9":                 LocData(8,  "Region 1 - Left"),
    "Color Cypher Room Pickup":             LocData(9, "Region 1 - Upper Right"),

    # Region 2
    "Silver Shard Puzzle 4":                LocData(10, "Region 2 - Central"),
    "Silver Shard Puzzle 5":                LocData(11, "Region 2 - Central"),
    "Silver Shard Puzzle 6":                LocData(12, "Region 2 - Sector 1"),
    "Silver Shard Puzzle 7":                LocData(13, "Region 2 - Sector 2"),
    "Silver Shard Puzzle 8":                LocData(14, "Region 2 - Lower"),
    "Silver Shard Puzzle 9":                LocData(15, "Region 2 - Lower"),
    "Silver Shard Puzzle 15":               LocData(16, "Region 2 - Serpent Upper"),
    "Smile Token Puzzle 1":                 LocData(17, "Region 2 - Sector 2"),
    "Smile Token Puzzle 6":                 LocData(18, "Region 2 - Serpent Upper"),
    "Smile Token Puzzle 8":                 LocData(19, "Region 2 - Sector 1"),
    "Gilded Serpent Reward":                LocData(20, "Region 2 - Serpent Lower"),
    "Cameo Room Pickup":                    LocData(21, "Region 2 - Sector 1"),
    "Car Hall Pickup":                      LocData(22, "Region 2 - Sector 2"),
    "Near Shooters Pickup":                 LocData(23, "Region 2 - Sector 1"),
    "Collapsed Tunnel Pickup":              LocData(24, "Region 2 - Sector 4"),
    "Nest Room Pickup":                     LocData(25, "Region 2 - Left"),
    "Serpent Boss Room Pickup":             LocData(26, "Region 2 - Serpent Lower"),

    # Region 3
    "Green Stone Trial":                    LocData(27, "Region 3"),
    "Blue Stone Trial":                     LocData(28, "Region 3"),
    "Red Stone Trial":                      LocData(29, "Region 3"),
    "Silver Shard Puzzle 10":               LocData(30, "Region 3"),
    "Silver Shard Puzzle 11":               LocData(31, "Region 3"),
    "Silver Shard Puzzle 12":               LocData(32, "Region 3"),
    "Silver Shard Puzzle 13":               LocData(33, "Region 3"),
    "Silver Shard Puzzle 14":               LocData(34, "Region 3"),
    "Smile Token Puzzle 2":                 LocData(35, "Region 3"),
    "Smile Token Puzzle 7":                 LocData(36, "Region 3"),

    # Collapse
    "Escape Normal Sequence Pickup":        LocData(37, "Collapse"),

    # Smile Shop
    "Smile Shop Item 1":                    LocData(38, "Smile Shop"),
    "Smile Shop Item 2":                    LocData(39, "Smile Shop"),
    "Smile Shop Item 3":                    LocData(40, "Smile Shop"),
    "Smile Shop Item 4":                    LocData(41, "Smile Shop"),
    "Dash Puzzle Reward":                   LocData(42, "Smile Shop"),
    "Respawn Reward":                       LocData(43, "Smile Shop"),
}

glyphs_good_ending_locations = {
    # Region 2
    "Smile Token Puzzle 10":                LocData(44, "Region 2 - Shadow Chase"),
    "Shadow Chase Reward":                  LocData(45, "Region 2 - Shadow Chase"),
    "Water Room Pickup":                    LocData(46, "Region 2 - Sector 4 End"),
    "George Reward":                        LocData(47, "Region 2 - Left"),
    "Shadow Chase Pickup":                  LocData(48, "Region 2 - Shadow Chase"),

    # Region 4
    "Spearman Reward":                      LocData(49, "Region 4 - Upper"),
    "Multiparry Gold Shard Puzzle":         LocData(50, "Region 4 - Central"),
    "Platforming Gold Shard Room":          LocData(51, "Region 4 - Central"),
    "Flower Puzzle Reward":                 LocData(52, "Region 4 - Central"),
    "Smile Token Puzzle 4":                 LocData(53, "Region 4 - Central"),
    "Smile Token Puzzle 5":                 LocData(54, "Region 4 - Entrance"),
    "On top of the Rosetta Stone Pickup":   LocData(55, "Region 4 - Central"),
    "Long Parry Platforming Room Pickup":   LocData(56, "Region 4 - Lower"),

    # Dark Region
    "Secret Room Pickup":                   LocData(57, "Dark Region"),
    "Large Room Pickup in the Corner":      LocData(58, "Dark Region"),
}

glyphs_full_tomb_locations = {
    # Region 1
    "Master Puzzle 2":                      LocData(59,  "Region 1 - Central"),

    # Region 2
    "Master Puzzle 1":                      LocData(60, "Region 2 - Sector 2"),

    # Region 3
    "Master Puzzle 3":                      LocData(61, "Region 3"),

    # The Between
    "Between Reward":                       LocData(62, "The Between"),
}

glyphs_outer_void_locations = {
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

# Like in Items.py, breaking up the different locations to help with organization and if something special needs to happen to them
event_locations = {
    "Defeat Runic Construct":               LocData(76, "Region 1 - Central"),
    "Stalker Sigil 1":                      LocData(77, "Region 1 - Central"),
    "Serpent Lock 1":                       LocData(78, "Region 2 - Sector 1"),
    "Serpent Lock 2":                       LocData(79, "Region 2 - Sector 2"),
    "Serpent Lock 3":                       LocData(80, "Region 2 - Sector 4 End"),
    "Defeat Gilded Serpent":                LocData(81, "Region 2 - Serpent Upper"),
    "Stalker Sigil 2":                      LocData(82, "Region 2 - Serpent Lower"),
    "Stalker Sigil 3":                      LocData(83, "Region 2 - Sector 4"),
    "Solve Flower Puzzle":                  LocData(84, "Region 2 - Sector 4 End"),
    "Collapse Unlock":                      LocData(85, "Region 3"),
    "Defeat Spearman":                      LocData(86, "Region 4 - Entrance"),
    "Defeat Wraith":                        LocData(87, "Region 4 - Lower"),
    "Defeat Vessel":                        LocData(88, "Region 4 - Lower"),
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
    **glyphs_false_ending_locations,
    **glyphs_good_ending_locations,
    **glyphs_full_tomb_locations,
    **glyphs_outer_void_locations,
    **event_locations
}