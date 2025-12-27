from enum import IntEnum
from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData

if TYPE_CHECKING:
    from . import GlyphsWorld

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
    if not world.options.UnreasonableLocations.value and name in glyphs_unreasonable_locations:
        return False
    return True

glyphs_locations = {
    # Starting Item
    "Starting Item":                        LocData(1,  "Menu"),                        # Temporary location to make logic less restrictive.

    # Region 1
    "Sword Pedestal":                       LocData(2,  "Region 1 - Central"),
    "Runic Construct Reward":               LocData(3,  "Region 1 - Central"),
    "Map Pedestal":                         LocData(4,  "Region 1 - Left"),
    "Silver Shard Puzzle 1":                LocData(5,  "Region 1 - Left"),
    "Silver Shard Puzzle 2":                LocData(6,  "Region 1 - Upper Right"),
    "Silver Shard Puzzle 3":                LocData(7,  "Region 1 - Upper Right"),
    "Smile Token Puzzle 1":                 LocData(8,  "Region 1 - Central"),
    "Smile Token Puzzle 9":                 LocData(9,  "Region 1 - Left"),
    "Color Cypher Room Pickup":             LocData(10, "Region 1 - Upper Right"),
    "Master Puzzle 2":                      LocData(11, "Region 1 - Central"),

    # Region 2
    "Silver Shard Puzzle 4":                LocData(12, "Region 2 - Central"),
    "Silver Shard Puzzle 5":                LocData(13, "Region 2 - Central"),
    "Silver Shard Puzzle 6":                LocData(14, "Region 2 - Sector 1"),
    "Silver Shard Puzzle 7":                LocData(15, "Region 2 - Sector 2"),
    "Silver Shard Puzzle 8":                LocData(16, "Region 2 - Lower"),
    "Silver Shard Puzzle 9":                LocData(17, "Region 2 - Lower"),
    "Silver Shard Puzzle 15":               LocData(18, "Region 2 - Serpent Upper"),
    "Smile Token Puzzle 3":                 LocData(19, "Region 2 - Sector 2"),
    "Smile Token Puzzle 6":                 LocData(20, "Region 2 - Serpent Upper"),
    "Smile Token Puzzle 8":                 LocData(21, "Region 2 - Sector 1"),
    "Smile Token Puzzle 10":                LocData(22, "Region 2 - Shadow Chase"),
    "Gilded Serpent Reward":                LocData(23, "Region 2 - Serpent Lower"),
    "Cameo Room Pickup":                    LocData(24, "Region 2 - Sector 1"),
    "Car Hall Pickup":                      LocData(25, "Region 2 - Sector 2"),
    "Near Shooters Pickup":                 LocData(26, "Region 2 - Sector 1"),
    "Collapsed Tunnel Pickup":              LocData(27, "Region 2 - Sector 4"),
    "Nest Room Pickup":                     LocData(28, "Region 2 - Left"),
    "Serpent Boss Room Pickup":             LocData(29, "Region 2 - Serpent Lower"),
    "Shadow Chase Reward":                  LocData(30, "Region 2 - Shadow Chase"),
    "Water Room Pickup":                    LocData(31, "Region 2 - Sector 4 End"),
    "George Reward 1":                      LocData(32, "Region 2 - Left"),
    "George Reward 2":                      LocData(33, "Region 2 - Left"),
    "Shadow Chase Pickup":                  LocData(34, "Region 2 - Shadow Chase"),
    "Master Puzzle 1":                      LocData(35, "Region 2 - Sector 2"),

    # Region 3
    "Green Stone Trial":                    LocData(36, "Region 3"),
    "Blue Stone Trial":                     LocData(37, "Region 3"),
    "Red Stone Trial":                      LocData(38, "Region 3"),
    "Silver Shard Puzzle 10":               LocData(39, "Region 3"),
    "Silver Shard Puzzle 11":               LocData(40, "Region 3"),
    "Silver Shard Puzzle 12":               LocData(41, "Region 3"),
    "Silver Shard Puzzle 13":               LocData(42, "Region 3"),
    "Silver Shard Puzzle 14":               LocData(43, "Region 3"),
    "Smile Token Puzzle 2":                 LocData(44, "Region 3"),
    "Smile Token Puzzle 7":                 LocData(45, "Region 3"),
    "Wizard Reward":                        LocData(46, "Region 3"),
    "Room Below Wizard Pickup":             LocData(47, "Region 3"),
    "Master Puzzle 3":                      LocData(48, "Region 3"),

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
    "Null Reward":                          LocData(59, "Dark Region"),

    # Smile Shop
    "Smile Shop Item 1":                    LocData(60, "Smile Shop"),
    "Smile Shop Item 2":                    LocData(61, "Smile Shop"),
    "Smile Shop Item 3":                    LocData(62, "Smile Shop"),
    "Smile Shop Item 4":                    LocData(63, "Smile Shop"),
    "Dash Puzzle Reward":                   LocData(64, "Smile Shop"),

    # The Between
    "Between Construct":                    LocData(65, "The Between"),
    "Between Serpent":                      LocData(66, "The Between"),
    "Between Wizard":                       LocData(67, "The Between"),
    "Hot Spring":                           LocData(68, "The Between"),
    "Between Reward 1":                     LocData(69, "The Between"),
    "Between Reward 2":                     LocData(70, "The Between"),

    # Collapse
    "Escape Normal Sequence Pickup":        LocData(71, "Collapse"),

    # Act 1
    "Enter Void Reward":                    LocData(72, "Act 1"),
    "Void Gate Shard Location 1":           LocData(73, "Act 1"),
    "Void Gate Shard Location 2":           LocData(74, "Act 1"),
    "Void Gate Shard Location 3":           LocData(75, "Act 1"),
    "Void Gate Shard Location 4":           LocData(76, "Act 1"),
    "Void Gate Shard Location 5":           LocData(77, "Act 1"),
    "Void Gate Shard Location 6":           LocData(78, "Act 1"),
    "Void Gate Shard Location 7":           LocData(79, "Act 1"),
    "John Room Pickup":                     LocData(80, "Act 1"),
    
    # Act 2
    "Free Item":                            LocData(81, "Act 2"),
    "Boss Rush Heal 1":                     LocData(82, "Act 2"),
    "Boss Rush Heal 2":                     LocData(83, "Act 2"),
    "Boss Rush Heal 3":                     LocData(84, "Act 2"),
    "Boss Rush Heal 4":                     LocData(85, "Act 2"),
    "Pink Bow Pickup":                      LocData(86, "Act 2"),

    # Act 3
    "Preminition Reward":                   LocData(87, "Act 3"),
}

glyphs_unreasonable_locations = {
    # Smile Shop
    "Respawn Reward":                       LocData(88, "Smile Shop"),
}

location_table = {
    **glyphs_locations,
    **glyphs_unreasonable_locations,
}
