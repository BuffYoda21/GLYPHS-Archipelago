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

def get_total_locations(world: "GlyphsWorld") -> int:
    total = 0
    for name in location_table:
        if is_valid_location(world, name):
            total += 1

    return total

def get_location_names() -> Dict[str, int]:
    names = {name: data.ap_code for name, data in location_table.items()}
    return names

def is_valid_location(world: "GlyphsWorld", name) -> bool:
    if name in event_locations:
        return True
    if world.options.UnreasonableLocations.value and name in glyphs_unreasonable_locations:
        return True
    if world.options.Shopsanity.value and name in glyphs_shopsanity_locations:
        return True
    if location_pool_type == LocationPoolType.FalseEnding(world) and not name in glyphs_false_ending_locations:
        return False
    if location_pool_type == LocationPoolType.GoodEnding(world) and not name in glyphs_good_ending_locations and not name in glyphs_false_ending_locations:
        return False
    if location_pool_type == LocationPoolType.FullTomb(world) and not name in glyphs_full_tomb_locations and not name in glyphs_good_ending_locations and not name in glyphs_false_ending_locations:
        return False
    if location_pool_type == LocationPoolType.OuterVoid(world) and not name in glyphs_outer_void_locations and not name in glyphs_full_tomb_locations and not name in glyphs_good_ending_locations and not name in glyphs_false_ending_locations:
        return False
    return True

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
    "Color Cypher Room Pickup":             LocData(9,  "Region 1 - Upper Right"),

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
}

glyphs_good_ending_locations = {
    # Region 2
    "Smile Token Puzzle 10":                LocData(38, "Region 2 - Shadow Chase"),
    "Shadow Chase Reward":                  LocData(39, "Region 2 - Shadow Chase"),
    "Water Room Pickup":                    LocData(40, "Region 2 - Sector 4 End"),
    "George Reward":                        LocData(41, "Region 2 - Left"),
    "Shadow Chase Pickup":                  LocData(42, "Region 2 - Shadow Chase"),

    # Region 4
    "Spearman Reward":                      LocData(43, "Region 4 - Upper"),
    "Multiparry Gold Shard Puzzle":         LocData(44, "Region 4 - Central"),
    "Platforming Gold Shard Room":          LocData(45, "Region 4 - Central"),
    "Flower Puzzle Reward":                 LocData(46, "Region 4 - Central"),
    "Smile Token Puzzle 4":                 LocData(47, "Region 4 - Central"),
    "Smile Token Puzzle 5":                 LocData(48, "Region 4 - Entrance"),
    "On top of the Rosetta Stone Pickup":   LocData(49, "Region 4 - Central"),
    "Long Parry Platforming Room Pickup":   LocData(50, "Region 4 - Lower"),

    # Dark Region
    "Secret Room Pickup":                   LocData(51, "Dark Region"),
    "Large Room Pickup in the Corner":      LocData(52, "Dark Region"),
}

glyphs_full_tomb_locations = {
    # Region 1
    "Master Puzzle 2":                      LocData(53, "Region 1 - Central"),

    # Region 2
    "Master Puzzle 1":                      LocData(54, "Region 2 - Sector 2"),

    # Region 3
    "Master Puzzle 3":                      LocData(55, "Region 3"),

    # Smile Shop
    "Dash Puzzle Reward":                   LocData(56, "Smile Shop"),

    # The Between
    "Between Reward":                       LocData(57, "The Between"),
}

glyphs_outer_void_locations = {
    # Act 1
    "Void Gate Shard Location 1":           LocData(58, "Act 1"),
    "Void Gate Shard Location 2":           LocData(59, "Act 1"),
    "Void Gate Shard Location 3":           LocData(60, "Act 1"),
    "Void Gate Shard Location 4":           LocData(61, "Act 1"),
    "Void Gate Shard Location 5":           LocData(62, "Act 1"),
    "Void Gate Shard Location 6":           LocData(63, "Act 1"),
    "Void Gate Shard Location 7":           LocData(64, "Act 1"),
    "John Room Pickup":                     LocData(65, "Act 1"),
    
    # Act 2
    "Boss Rush Heal 1":                     LocData(66, "Act 2"),
    "Boss Rush Heal 2":                     LocData(67, "Act 2"),
    "Boss Rush Heal 3":                     LocData(68, "Act 2"),
    "Boss Rush Heal 4":                     LocData(69, "Act 2"),
    "Pink Bow Pickup":                      LocData(70, "Act 2"),
}

glyphs_unreasonable_locations = {
    # Smile Shop
    "Respawn Reward":                       LocData(71, "Smile Shop"),
}

glyphs_shopsanity_locations = {
    # Smile Shop
    "Smile Shop Item 1":                    LocData(72, "Smile Shop"),
    "Smile Shop Item 2":                    LocData(73, "Smile Shop"),
    "Smile Shop Item 3":                    LocData(74, "Smile Shop"),
    "Smile Shop Item 4":                    LocData(75, "Smile Shop"),
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
    "Good Ending":                          LocData(87, "Region 4 - Lower"),
    "Last Fracture":                        LocData(88, "Region 4 - Lower"),
    "False Ending":                         LocData(89, "Collapse"),
    "Smilemask Ending":                     LocData(90, "Smile Shop"),
    "Defeat Null":                          LocData(91, "Dark Region"),
    "Clarity":                              LocData(92, "Dark Region"),
    "Perfect Clarity":                      LocData(93, "Dark Region"),
    "Omnipotence Ending":                   LocData(94, "Act 1"),
    "Clear Act 1":                          LocData(95, "Act 1"),
    "Clear Act 2":                          LocData(96, "Act 2"),
    "True Ending":                          LocData(97, "Act 3"),
    "Clear Epilogue":                       LocData(98, "Epilogue"),
}

location_table = {
    **glyphs_false_ending_locations,
    **glyphs_good_ending_locations,
    **glyphs_full_tomb_locations,
    **glyphs_outer_void_locations,
    **glyphs_unreasonable_locations,
    **glyphs_shopsanity_locations,
    **event_locations
}