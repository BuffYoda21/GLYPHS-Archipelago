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
    "Master Puzzle 2":                      LocData(10, "Region 1 - Central"),

    # Region 2
    "Silver Shard Puzzle 4":                LocData(11, "Region 2 - Central"),
    "Silver Shard Puzzle 5":                LocData(12, "Region 2 - Central"),
    "Silver Shard Puzzle 6":                LocData(13, "Region 2 - Sector 1"),
    "Silver Shard Puzzle 7":                LocData(14, "Region 2 - Sector 2"),
    "Silver Shard Puzzle 8":                LocData(15, "Region 2 - Lower"),
    "Silver Shard Puzzle 9":                LocData(16, "Region 2 - Lower"),
    "Silver Shard Puzzle 15":               LocData(17, "Region 2 - Serpent Upper"),
    "Smile Token Puzzle 1":                 LocData(18, "Region 2 - Sector 2"),
    "Smile Token Puzzle 6":                 LocData(19, "Region 2 - Serpent Upper"),
    "Smile Token Puzzle 8":                 LocData(20, "Region 2 - Sector 1"),
    "Smile Token Puzzle 10":                LocData(21, "Region 2 - Shadow Chase"),
    "Gilded Serpent Reward":                LocData(22, "Region 2 - Serpent Lower"),
    "Cameo Room Pickup":                    LocData(23, "Region 2 - Sector 1"),
    "Car Hall Pickup":                      LocData(24, "Region 2 - Sector 2"),
    "Near Shooters Pickup":                 LocData(25, "Region 2 - Sector 1"),
    "Collapsed Tunnel Pickup":              LocData(26, "Region 2 - Sector 4"),
    "Nest Room Pickup":                     LocData(27, "Region 2 - Left"),
    "Serpent Boss Room Pickup":             LocData(28, "Region 2 - Serpent Lower"),
    "Shadow Chase Reward":                  LocData(29, "Region 2 - Shadow Chase"),
    "Water Room Pickup":                    LocData(30, "Region 2 - Sector 4 End"),
    "George Reward":                        LocData(31, "Region 2 - Left"),
    "Shadow Chase Pickup":                  LocData(32, "Region 2 - Shadow Chase"),
    "Master Puzzle 1":                      LocData(33, "Region 2 - Sector 2"),

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

    # Region 4
    "Spearman Reward":                      LocData(45, "Region 4 - Upper"),
    "Multiparry Gold Shard Puzzle":         LocData(46, "Region 4 - Central"),
    "Platforming Gold Shard Room":          LocData(47, "Region 4 - Central"),
    "Flower Puzzle Reward":                 LocData(48, "Region 4 - Central"),
    "Smile Token Puzzle 4":                 LocData(49, "Region 4 - Central"),
    "Smile Token Puzzle 5":                 LocData(50, "Region 4 - Entrance"),
    "On top of the Rosetta Stone Pickup":   LocData(51, "Region 4 - Central"),
    "Long Parry Platforming Room Pickup":   LocData(52, "Region 4 - Lower"),

    # Dark Region
    "Secret Room Pickup":                   LocData(53, "Dark Region"),
    "Large Room Pickup in the Corner":      LocData(54, "Dark Region"),

    # Smile Shop
    "Smile Shop Item 1":                    LocData(55, "Smile Shop"),
    "Smile Shop Item 2":                    LocData(56, "Smile Shop"),
    "Smile Shop Item 3":                    LocData(57, "Smile Shop"),
    "Smile Shop Item 4":                    LocData(58, "Smile Shop"),
    "Dash Puzzle Reward":                   LocData(59, "Smile Shop"),

    # The Between
    "Between Reward":                       LocData(60, "The Between"),

    # Collapse
    "Escape Normal Sequence Pickup":        LocData(61, "Collapse"),

    # Act 1
    "Void Gate Shard Location 1":           LocData(62, "Act 1"),
    "Void Gate Shard Location 2":           LocData(63, "Act 1"),
    "Void Gate Shard Location 3":           LocData(64, "Act 1"),
    "Void Gate Shard Location 4":           LocData(65, "Act 1"),
    "Void Gate Shard Location 5":           LocData(66, "Act 1"),
    "Void Gate Shard Location 6":           LocData(67, "Act 1"),
    "Void Gate Shard Location 7":           LocData(68, "Act 1"),
    "John Room Pickup":                     LocData(69, "Act 1"),
    
    # Act 2
    "Boss Rush Heal 1":                     LocData(70, "Act 2"),
    "Boss Rush Heal 2":                     LocData(71, "Act 2"),
    "Boss Rush Heal 3":                     LocData(72, "Act 2"),
    "Boss Rush Heal 4":                     LocData(73, "Act 2"),
    "Pink Bow Pickup":                      LocData(74, "Act 2"),
}

glyphs_unreasonable_locations = {
    # Smile Shop
    "Respawn Reward":                       LocData(75, "Smile Shop"),
}

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
    **glyphs_locations,
    **glyphs_unreasonable_locations,
    **event_locations
}